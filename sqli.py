import re

# Define a list of common SQL injection patterns
SQL_INJECTION_PATTERNS = [
    r"(?i)\b(select|insert|update|delete|drop|union|into|from)\b",
    r"(?i)(--|#|\b(and|or)\b.*\b\d+)\b",
    r"(?i)\b(exec|cmd)\b",
    r"(?i)\b'|\b--|\b#"
]

def detect_sql_injection(input_data):
    """
    Detect potential SQL Injection attempts in the input data.
    """
    for pattern in SQL_INJECTION_PATTERNS:
        if re.search(pattern, input_data):
            return True
    return False
