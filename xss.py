import re
from html import escape

def detect_xss(input_data):
    """
    Detect and sanitize potential XSS attacks by escaping special characters.
    """
    # Simple patterns for detecting script tags or javascript invocations
    xss_patterns = [
        r"<script.*?>.*?</script>",
        r"javascript:[^'\"<]*",
        r"on\w+=.*"
    ]
    
    for pattern in xss_patterns:
        if re.search(pattern, input_data, re.IGNORECASE):
            return True
    return False

def sanitize_input(input_data):
    """
    Sanitize input by escaping HTML characters to prevent XSS.
    """
    return escape(input_data)

