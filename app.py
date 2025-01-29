import requests

def get_aircraft_info(flight_number):
    url = f"https://www.airnavradar.com/data/flights/info?type=flights&query={flight_number}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return {"error": f"Erro HTTP {response.status_code}"}

    data = response.json()

    # 🛩️ Extraindo os dados corretos
    tail_number = data.get("acr", "Não encontrado")
    aircraft_model = data.get("acd", "Não encontrado")

    return {"tail_number": tail_number, "model": aircraft_model}

# ✅ Teste com um voo real
print(get_aircraft_info)
