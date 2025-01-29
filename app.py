from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

def get_aircraft_info(flight_number):
    url = f"https://www.airnavradar.com/data/flights/info?type=flights&query={flight_number}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json",
        "Referer": "https://www.airnavradar.com/",
        "Origin": "https://www.airnavradar.com"
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return {"error": f"Erro {response.status_code}"}

        data = response.json()
        return {
            "tail_number": data.get("acr", "Não encontrado"),
            "aircraft_model": data.get("acd", "Não encontrado")
        }
    except Exception as e:
        return {"error": str(e)}

@app.route("/get_aircraft", methods=["GET"])
def get_aircraft():
    flight_number = request.args.get("flight")
    if not flight_number:
        return jsonify({"error": "Parâmetro 'flight' ausente"}), 400

    data = get_aircraft_info(flight_number)
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
