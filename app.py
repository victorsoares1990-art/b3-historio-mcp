from flask import Flask, jsonify
import requests

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


@app.route("/teste-b3")
def teste_b3():

    url = "https://bvmf.bmfbovespa.com.br/InstDados/SerHist/COTAHIST_M092026.ZIP"

    try:
        resposta = requests.head(url, timeout=15)

        return jsonify({
            "status": "ok",
            "codigo_http": resposta.status_code,
            "tamanho": resposta.headers.get("Content-Length")
        })

    except Exception as erro:

        return jsonify({
            "status": "erro",
            "mensagem": str(erro)
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
