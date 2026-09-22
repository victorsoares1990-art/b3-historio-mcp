from flask import Flask, jsonify

app = Flask(_name_)

@app.route("/")
def home():
    return jsonify({
        "status": "ok",
        "projeto": "B3 Histórico MCP",
        "mensagem": "Servidor funcionando"
    })

@app.route("/health")
def health():
    return jsonify({
        "status": "healthy"
    })

if _name_ == "_main_":
    app.run(host="0.0.0.0", port=10000)
