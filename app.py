from flask import Flask, jsonify

app = Flask(__name__)

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

@app.route("/historico/<ticker>")
def historico(ticker):
    return jsonify({
        "ticker": ticker.upper(),
        "status": "ok",
        "mensagem": "Endpoint histórico funcionando"
    })

if _name_ == "__main__":
    app.run(host="0.0.0.0", port=10000)
