from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def get_aircraft_info_flightradar(flight_number):
    """Obtém o tail number e o modelo do avião no FlightRadar24"""
    url = f"https://www.flightradar24.com/data/flights/{flight_number}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return {"error": f"Falha ao obter os dados (Status {response.status_code})"}

    soup = BeautifulSoup(response.text, "html.parser")

    # Encontra o link que contém o tail number
    aircraft_tag = soup.find("a", class_="fbold", href=lambda x: x and "/data/aircraft/" in x)

    if aircraft_tag:
        tail_number = aircraft_tag.text.strip()  # Ex: "F-HNCO"
        model = aircraft_tag.get("title", "Desconhecido")  # Ex: "Airbus A321-251NX"

        return {
            "tail_number": tail_number,
            "model": model
        }
    
    return {"error": "Não foi possível encontrar os dados da aeronave"}

@app.route("/get_aircraft", methods=["GET"])
def get_aircraft():
    flight_number = request.args.get("flight")
    if not flight_number:
        return jsonify({"error": "Parâmetro 'flight' ausente"}), 400

    data = get_aircraft_info_flightradar(flight_number)
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)

