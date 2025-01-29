from flask import Flask, request, jsonify
import requests
import re
import time

app = Flask(__name__)

def get_aircraft_info(flight_number):
    url = f"https://www.flightradar24.com/data/flights/{flight_number}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    time.sleep(3)  # Evita erro 429
    response = requests.get(url, headers=headers)

    if response.status_code == 429:
        return {"error": "Muitas requisições - tente mais tarde"}
    
    if response.status_code != 200:
        return {"error": f"Erro HTTP {response.status_code}"}

    html = response.text

    # Extrai Tail Number
    tail_match = re.search(r'/data/aircraft/([\w-]+)', html)
    tail_number = tail_match.group(1) if tail_match else "Não encontrado"

    # Extrai Modelo
    model_match = re.search(r'title="([^"]+)"\s*>F-', html)
    aircraft_model = model_match.group(1) if model_match else "Não encontrado"

    return {"tail_number": tail_number, "model": aircraft_model}

@app.route('/get_aircraft', methods=['GET'])
def get_aircraft():
    flight_number = request.args.get('flight')
    if not flight_number:
        return jsonify({"error": "Número de voo ausente"}), 400

    result = get_aircraft_info(flight_number)
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
