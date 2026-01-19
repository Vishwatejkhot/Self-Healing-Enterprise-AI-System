import hashlib

def fingerprint_docs(docs):
    h = hashlib.sha256()
    for d in docs:
        h.update(d.page_content.encode())
    return h.hexdigest()
