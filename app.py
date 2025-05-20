from flask import Flask, request, render_template, jsonify
import joblib
from sqli import detect_sql_injection
from xss import detect_xss, sanitize_input
from csrf import generate_csrf_token, validate_csrf_token
from utils import log_attack
from config import WAF_ENABLED

# Load the pre-trained anomaly detection model
model = joblib.load('anomaly_detector.joblib')

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Flask session key

def extract_features(request):
    """
    Extract features from the HTTP request, ensuring we return exactly 6 features.
    """
    features = []

    # Feature 1: Number of form parameters
    features.append(len(request.form))

    # Feature 2: Number of query parameters
    features.append(len(request.args))

    # Feature 3: Total length of all form parameter values combined
    total_form_length = sum(len(value) for value in request.form.values())
    features.append(total_form_length)

    # Feature 4: Total length of all query parameter values combined
    total_query_length = sum(len(value) for value in request.args.values())
    features.append(total_query_length)

    # Feature 5: Presence of SQL keywords (number of occurrences in the form/query data)
    sql_keywords = ["SELECT", "INSERT", "UPDATE", "DELETE", "DROP", "UNION"]
    sql_count = sum(1 for value in request.form.values() if any(kw in value.upper() for kw in sql_keywords))
    sql_count += sum(1 for value in request.args.values() if any(kw in value.upper() for kw in sql_keywords))
    features.append(sql_count)

    # Feature 6: Presence of XSS patterns (number of occurrences in the form/query data)
    xss_patterns = ["<script>", "</script>", "javascript:"]
    xss_count = sum(1 for value in request.form.values() if any(kw in value.lower() for kw in xss_patterns))
    xss_count += sum(1 for value in request.args.values() if any(kw in value.lower() for kw in xss_patterns))
    features.append(xss_count)

    return features

@app.before_request
def check_for_attacks():
    """
    Check for SQL injection, XSS, CSRF attacks, and anomalous behavior
    before processing the request.
    """
    if WAF_ENABLED:
        detected_attacks = []
        sql_injection_ml_detected = False

        # Check for SQL injection
        if any(detect_sql_injection(value) for value in request.form.values()) or any(detect_sql_injection(value) for value in request.args.values()):
            log_attack('SQL Injection', request.form)
            detected_attacks.append("SQL Injection detected")

        # Check for XSS
        if any(detect_xss(value) for value in request.form.values()) or any(detect_xss(value) for value in request.args.values()):
            log_attack('XSS', request.form)
            detected_attacks.append("XSS attack detected")

        # CSRF Token validation
        csrf_token = request.headers.get('X-CSRF-TOKEN')
        if csrf_token and not validate_csrf_token(csrf_token):
            log_attack('CSRF', request.form)
            detected_attacks.append("CSRF attack detected")

        # Anomaly detection for SQL injection
        features = extract_features(request)
        if len(features) == model.n_features_in_:
            is_anomalous = model.predict([features])[0] == -1  # -1 indicates anomaly
            if is_anomalous:
                sql_injection_ml_detected = True
                log_attack("SQL Injection detected by ML", request.form)
                detected_attacks.append("SQL Injection detected by ML")
        else:
            detected_attacks.append("Feature mismatch error in anomaly detection")

        # If any attacks were detected, display on the frontend
        if detected_attacks:
            return render_template('attack_alert.html', detected_attacks=detected_attacks, sql_injection_ml_detected=sql_injection_ml_detected)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    # Simulate form submission and processing
    user_input = request.form.get('user_input')
    
    # Sanitize XSS before processing
    sanitized_input = sanitize_input(user_input)
    
    # Further processing...

    return jsonify({"message": "Form submitted successfully!"})

@app.route('/get_csrf_token', methods=['GET'])
def get_csrf_token():
    csrf_token = generate_csrf_token()
    return jsonify({"csrf_token": csrf_token})

if __name__ == '__main__':
    app.run(debug=True)