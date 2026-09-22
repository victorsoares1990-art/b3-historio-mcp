from flask import Flask, jsonify
import requests
import zipfile
import io
from datetime import datetime

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

    ano = datetime.now().year

    url = f"https://bvmf.bmfbovespa.com.br/InstDados/SerHist/COTAHIST_A{ano}.ZIP"

    try:

        resposta = requests.get(
            url,
            timeout=120
        )

        if resposta.status_code != 200:
            return jsonify({
                "status": "erro",
                "mensagem": "Não foi possível baixar o arquivo da B3",
                "codigo_http": resposta.status_code
            }), 500

        arquivo_zip = zipfile.ZipFile(
            io.BytesIO(resposta.content)
        )

        nome_txt = arquivo_zip.namelist()[0]

        dados = []

        with arquivo_zip.open(nome_txt) as arquivo:

            for linha in arquivo:

                linha = linha.decode(
                    "latin-1",
                    errors="ignore"
                ).rstrip("\r\n")

                if len(linha) < 245:
                    continue

                if linha[0:2] != "01":
                    continue

                codigo = linha[12:24].strip()

                if codigo != ticker:
                    continue

                data = linha[2:10]

                abertura = int(linha[56:69]) / 100
                maxima = int(linha[69:82]) / 100
                minima = int(linha[82:95]) / 100
                medio = int(linha[95:108]) / 100
                fechamento = int(linha[108:121]) / 100

                negocios = int(linha[147:152])

                quantidade = int(linha[152:170])

                volume = int(linha[170:188]) / 100

                dados.append({
                    "data": data,
                    "abertura": abertura,
                    "maxima": maxima,
                    "minima": minima,
                    "medio": medio,
                    "fechamento": fechamento,
                    "negocios": negocios,
                    "quantidade": quantidade,
                    "volume": volume
                })

        return jsonify({
            "status": "ok",
            "ticker": ticker,
            "ano": ano,
            "quantidade_registros": len(dados),
            "dados": dados
        })

    except Exception as erro:

        return jsonify({
            "status": "erro",
            "mensagem": str(erro)
        }), 500


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=10000
    )
