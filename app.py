from flask import Flask, request, jsonify, render_template_string

from rag.vectorstore import load_store
from rag.retriever import retrieve

from agents.answer_agent import answer
from agents.critic_agent import should_fail
from agents.policy_agent import policy_check
from agents.root_cause_agent import diagnose

from healing.self_heal import heal
from monitoring.metrics import log_query, log_failure
from monitoring.audit_log import audit

app = Flask(__name__)
db = load_store()


BASE_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>AegisAI</title>

    {% raw %}
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto;
            background: #f5f7fb;
            margin: 0;
            padding: 0;
        }

        .container {
            max-width: 900px;
            margin: 50px auto;
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.08);
        }

        h1 {
            margin-top: 0;
            color: #2c3e50;
        }

        .subtitle {
            color: #666;
            margin-bottom: 30px;
        }

        input[type=text] {
            width: 100%;
            padding: 12px;
            font-size: 16px;
            border-radius: 6px;
            border: 1px solid #ccc;
        }

        button {
            margin-top: 15px;
            padding: 12px 20px;
            background: #4f46e5;
            color: white;
            border: none;
            border-radius: 6px;
            font-size: 16px;
            cursor: pointer;
        }

        button:hover {
            background: #4338ca;
        }

        .card {
            margin-top: 25px;
            padding: 20px;
            border-radius: 8px;
            background: #f9fafb;
            border-left: 5px solid #4f46e5;
        }

        .label {
            font-weight: 600;
            color: #333;
        }

        .confidence {
            margin-top: 10px;
            font-weight: bold;
        }

        .good { color: #16a34a; }
        .medium { color: #ca8a04; }
        .bad { color: #dc2626; }

        .warning {
            margin-top: 15px;
            padding: 10px;
            background: #fff7ed;
            border-left: 4px solid #f97316;
            color: #92400e;
            border-radius: 6px;
        }

        .footer {
            margin-top: 40px;
            font-size: 14px;
            color: #777;
            text-align: center;
        }

        a {
            color: #4f46e5;
            text-decoration: none;
            font-weight: 500;
        }
    </style>
    {% endraw %}
</head>
<body>
    <div class="container">
    {{ body | safe }}
    </div>

</body>
</html>
"""


@app.route("/", methods=["GET"])
def home():
    body = """
    <h1>AegisAI</h1>
    <p class="subtitle">Self-Healing Enterprise AI System</p>

    <form action="/ask-ui" method="post">
        <input type="text" name="query"
               placeholder="Ask a question (e.g. Is remote work allowed?)"
               required />
        <button type="submit">Ask</button>
    </form>

    <div class="footer">
        API: <code>POST /ask</code> · <a href="/metrics">Metrics</a>
    </div>
    """
    return render_template_string(BASE_HTML, body=body)


@app.route("/ask-ui", methods=["POST"])
def ask_ui():
    log_query()
    query = request.form["query"]

    context, confidence = retrieve(db, query)
    ans = answer(query, context)

    # Policy enforcement (blocking)
    if policy_check(ans):
        audit("policy_violation", {"query": query})
        body = """
        <h1>Blocked</h1>
        <div class="card">
            <p>This answer violates enterprise policy.</p>
        </div>
        <br>
        <a href="/">Ask another question</a>
        """
        return render_template_string(BASE_HTML, body=body)

    # Non-blocking self-healing
    needs_healing = should_fail(
        hallucinated=("I don't know" in ans or len(ans.strip()) < 10),
        confidence=confidence
    )

    if needs_healing:
        log_failure()
        reason = diagnose(query, confidence)
        heal(reason)
        audit("self_heal", {"reason": reason})
    else:
        audit("success", {"query": query})

    # Confidence color
    if confidence >= 0.7:
        conf_class = "good"
    elif confidence >= 0.4:
        conf_class = "medium"
    else:
        conf_class = "bad"

    body = f"""
    <h1>Answer</h1>

    <div class="card">
        <p class="label">Question</p>
        <p>{query}</p>
    </div>

    <div class="card">
        <p class="label">Answer</p>
        <p>{ans}</p>
        <p class="confidence {conf_class}">
            Retrieval confidence: {round(confidence, 2)}
        </p>
    </div>
    """

    if needs_healing:
        body += """
        <div class="warning">
            ⚠ System detected uncertainty and self-healed in the background.
        </div>
        """

    body += """
    <br>
    <a href="/">Ask another question</a>
    """

    return render_template_string(BASE_HTML, body=body)



# API ENDPOINT
@app.route("/ask", methods=["POST"])
def ask_api():
    log_query()
    data = request.get_json()

    if not data or "query" not in data:
        return jsonify({"error": "Missing query"}), 400

    query = data["query"]
    context, confidence = retrieve(db, query)
    ans = answer(query, context)

    if policy_check(ans):
        audit("policy_violation", {"query": query})
        return jsonify({"status": "blocked"})

    if should_fail("I don't know" in ans, confidence):
        log_failure()
        reason = diagnose(query, confidence)
        heal(reason)
        audit("self_heal", {"reason": reason})

    audit("success", {"query": query})

    return jsonify({
        "answer": ans,
        "confidence": round(confidence, 2)
    })


# METRICS
@app.route("/metrics", methods=["GET"])
def metrics():
    from monitoring.metrics import metrics
    return jsonify(metrics)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
