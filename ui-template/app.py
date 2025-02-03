from flask import Flask, render_template, jsonify, request
import requests
from datetime import datetime

app = Flask(__name__)

API_URL = "https://p6i3sfv2ff.execute-api.us-east-1.amazonaws.com"

@app.route('/')
def index():
    data = requests.get(f"{API_URL}/Prod/todos").json()
    return render_template('index.html', data=data)

@app.template_filter('format_date')
def format_date(timestamp):
    try:
        # Convertir el timestamp a un objeto datetime
        dt_object = datetime.fromtimestamp(float(timestamp))
        # Formatear la fecha en el formato deseado
        return dt_object.strftime('%d/%m/%Y %H:%M')
    except (ValueError, OSError):
        return "Fecha inválida"


@app.route('/api/todos/<todo_id>', methods=['PUT'])
def update_todo(todo_id):
    # Obtener los datos del cuerpo de la solicitud
    data = request.get_json()
    # Hacer la solicitud a la API de AWS
    response = requests.put(f"{API_URL}/Prod/todos/{todo_id}", json=data)
    # Devolver la respuesta de la API de AWS
    return jsonify(response.json()), response.status_code

@app.route('/api/todos/delete/<todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    response = requests.delete(f"{API_URL}/Prod/todos/{todo_id}")
    # Verificar el código de estado
    if response.status_code == 200:
        return jsonify({"message": "Todo eliminado correctamente."}), 204

@app.route('/api/todos/create', methods=['POST'])
def create_todo():
    data = request.get_json()
    response = requests.post(f"{API_URL}/Prod/todos/", json=data)
    return jsonify(response.json()), response.status_code

if __name__ == '__main__':
    app.run(debug=True)