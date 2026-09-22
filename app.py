from flask import Flask, jsonify
import requests
import zipfile
import io
from datetime import datetime, timedelta

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

    ticker = ticker.upper()

    ano_atual = datetime.now().year

    url = f"https://bvmf.bmfbovespa.com.br/InstDados/SerHist/COTAHIST_A{ano_atual}.ZIP"

    resposta = requests.get(url, timeout=60)

    if resposta.status_code != 200:
        return jsonify({
            "status": "erro",
            "mensagem": "Não foi possível baixar o arquivo histórico da B3",
            "codigo_http": resposta.status_code
        }), 500

    arquivo_zip = zipfile.ZipFile(io.BytesIO(resposta.content))

    arquivos = arquivo_zip.namelist()

    return jsonify({
        "status": "ok",
        "ticker": ticker,
        "ano": ano_atual,
        "arquivo_b3": arquivos
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
