import sys
import time
from pathlib import Path

# Add src folder to sys.path to ensure correct imports
SRC_DIR = Path(__file__).resolve().parent
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from flask import Flask, request, jsonify
from risk_scorer import calculate_risk

app = Flask(__name__)

# In-memory IP registry database
# Maps client IP -> {
#   "status": "clean" | "flagged" | "blocked",
#   "suspicious_attempts": int,
#   "last_suspicious_time": float,
#   "blocked_at": float | None
# }
ip_registry = {}

# Security events logs list
security_events = []

def get_client_ip():
    # Retrieve client IP, falling back to X-Forwarded-For if behind a proxy
    if request.headers.getlist("X-Forwarded-For"):
        ip = request.headers.getlist("X-Forwarded-For")[0].split(',')[0].strip()
    else:
        ip = request.remote_addr
    return ip

@app.after_request
def add_cors_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

@app.route("/api/analyze", methods=["POST", "OPTIONS"])
def analyze():
    if request.method == 'OPTIONS':
        return '', 200

    data = request.get_json() or {}
    prompt = data.get("prompt", "").strip()
    
    # Real IP address extraction only - no simulation input spoofing allowed
    ip = get_client_ip()

    if not prompt:
        return jsonify({"error": "Prompt cannot be empty"}), 400

    current_time = time.time()

    # Initialize IP if not registered
    if ip not in ip_registry:
        ip_registry[ip] = {
            "status": "clean",
            "suspicious_attempts": 0,
            "last_suspicious_time": 0.0,
            "blocked_at": None
        }

    ip_info = ip_registry[ip]

    # Rule 1: Check if IP is permanently blocked
    if ip_info["status"] == "blocked":
        return jsonify({
            "error": "Access Denied",
            "message": "This IP address has been permanently blocked due to repeated suspicious activity.",
            "ip_status": "blocked",
            "ip": ip
        }), 403

    # Rule 2: Check if IP is in 30-second cooldown
    if ip_info["status"] == "flagged":
        time_elapsed = current_time - ip_info["last_suspicious_time"]
        if time_elapsed < 30.0:
            remaining_cooldown = int(30.0 - time_elapsed)
            return jsonify({
                "error": "Rate Limit Exceeded",
                "message": f"This IP address is temporarily suspended due to flagged security threats. Cooldown active for another {remaining_cooldown} seconds.",
                "ip_status": "flagged",
                "remaining_cooldown": remaining_cooldown,
                "ip": ip
            }), 429
        else:
            # Cooldown period has expired, reset state back to clean
            ip_info["status"] = "clean"

    # Run analysis
    try:
        result = calculate_risk(prompt)
    except Exception as e:
        return jsonify({"error": f"Error running risk analysis: {str(e)}"}), 500

    is_malicious = result["is_malicious"]
    mitigation_triggered = "none"

    if is_malicious:
        ip_info["suspicious_attempts"] += 1
        ip_info["last_suspicious_time"] = current_time

        if ip_info["suspicious_attempts"] >= 3:
            ip_info["status"] = "blocked"
            ip_info["blocked_at"] = current_time
            mitigation_triggered = "blocked"
        else:
            ip_info["status"] = "flagged"
            mitigation_triggered = "cooldown"

        # Log security alert event
        event = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(current_time)),
            "ip": ip,
            "prompt": prompt,
            "risk_score": result["risk_score"],
            "risk_level": result["risk_level"],
            "is_malicious": result["is_malicious"],
            "ml_probability": result["ml_probability"],
            "regex_rules_triggered": result["regex_rules_triggered"],
            "detected_categories": result["detected_categories"],
            "mitigation_triggered": mitigation_triggered
        }
        security_events.append(event)

    return jsonify({
        "analysis": {
            "risk_score": result["risk_score"],
            "risk_level": result["risk_level"],
            "is_malicious": result["is_malicious"],
            "ml_probability": result["ml_probability"],
            "regex_rules_triggered": result["regex_rules_triggered"],
            "detected_categories": result["detected_categories"],
        },
        "ip_mitigation": {
            "ip": ip,
            "status": ip_info["status"],
            "suspicious_attempts": ip_info["suspicious_attempts"],
            "remaining_cooldown": 30 if mitigation_triggered == "cooldown" else 0,
            "mitigation_triggered": mitigation_triggered
        }
    })

@app.route("/api/alerts", methods=["GET", "OPTIONS"])
def get_alerts():
    if request.method == 'OPTIONS':
        return '', 200
    # Return events list (reverse sorted by timestamp to show newest first)
    return jsonify(security_events[::-1])

@app.route("/api/ips", methods=["GET", "OPTIONS"])
def get_ips():
    if request.method == 'OPTIONS':
        return '', 200
    
    # Format and return the tracked IP registry list
    ips_list = []
    current_time = time.time()
    for ip, info in ip_registry.items():
        remaining = 0
        if info["status"] == "flagged":
            time_elapsed = current_time - info["last_suspicious_time"]
            if time_elapsed < 30.0:
                remaining = int(30.0 - time_elapsed)
        
        ips_list.append({
            "ip": ip,
            "status": info["status"],
            "suspicious_attempts": info["suspicious_attempts"],
            "last_suspicious_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(info["last_suspicious_time"])) if info["last_suspicious_time"] > 0 else "N/A",
            "blocked_at": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(info["blocked_at"])) if info["blocked_at"] else None,
            "remaining_cooldown": remaining
        })
    return jsonify(ips_list)

@app.route("/api/ip/reset", methods=["POST", "OPTIONS"])
def reset_ip():
    if request.method == 'OPTIONS':
        return '', 200

    data = request.get_json() or {}
    ip = data.get("ip", "").strip()
    if not ip or ip not in ip_registry:
        return jsonify({"error": "IP address not found in registry"}), 404
    
    # Completely reset tracking state
    ip_registry[ip] = {
        "status": "clean",
        "suspicious_attempts": 0,
        "last_suspicious_time": 0.0,
        "blocked_at": None
    }
    return jsonify({"success": True, "message": f"IP address {ip} has been reset to clean status."})

if __name__ == "__main__":
    print("=" * 60)
    print("PROMPTSHIELD AI SECURITY GATEWAY STARTED (Port 5001)")
    print("Monitoring real client IPs at: http://127.0.0.1:5001/")
    print("=" * 60)
    app.run(host="127.0.0.1", port=5001, debug=True)
