from flask import Flask, render_template, request, jsonify
import threading
from automation import executar_autopilot
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/iniciar', methods=['POST'])
def iniciar():
    data = request.json
    ra = data.get('ra')
    senha = data.get('senha')
    tempo = int(data.get('tempo', 45))

    if not ra or not senha:
        return jsonify({"status": "erro", "mensagem": "RA e senha obrigatórios"})

    # Executa em background
    thread = threading.Thread(
        target=executar_autopilot, 
        args=(ra, senha, tempo),
        daemon=True
    )
    thread.start()

    return jsonify({
        "status": "sucesso", 
        "mensagem": f"Autopilot iniciado para RA {ra} por {tempo} minutos."
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)