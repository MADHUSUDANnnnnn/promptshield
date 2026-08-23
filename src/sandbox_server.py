import sys
from pathlib import Path

# Add src folder to sys.path to ensure correct imports
SRC_DIR = Path(__file__).resolve().parent
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from flask import Flask, render_template

app = Flask(
    __name__,
    template_folder=str(SRC_DIR / "templates"),
    static_folder=str(SRC_DIR / "static")
)

@app.route("/")
def sandbox():
    return render_template("sandbox.html")

if __name__ == "__main__":
    print("=" * 60)
    print("PROMPTSHIELD THREAT SANDBOX SERVER STARTED (Port 5002)")
    print("Access the sandbox UI at: http://127.0.0.1:5002/")
    print("=" * 60)
    app.run(host="127.0.0.1", port=5002, debug=True)
