from flask import Flask, request, jsonify
from flask_cors import CORS
from pipeline import answer_question

app = Flask(__name__)
CORS(app)


@app.route("/api/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/api/query", methods=["POST"])
def query():
    body = request.get_json(silent=True) or {}
    question = (body.get("question") or "").strip()

    if not question:
        return jsonify({"ok": False, "error": "Please enter a question."}), 400

    result = answer_question(question)
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, port=5000)