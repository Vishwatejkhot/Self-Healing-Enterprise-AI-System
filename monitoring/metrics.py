metrics = {
    "queries": 0,
    "failures": 0,
}

def log_query():
    metrics["queries"] += 1

def log_failure():
    metrics["failures"] += 1
