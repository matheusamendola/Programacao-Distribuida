import requests
from rich import print

key = "7b229feabe44cf5326591114"

# Taxa de Cambio

def get_cambio(moeda):
    r = requests.get(f"https://v6.exchangerate-api.com/v6/{key}/pair/USD/{moeda}")
    print(r.json())
    return r.json()


Taxas = ["BRL", "EUR", "JPY"]

for cambio in range(len(Taxas)):
    resultado = get_cambio(Taxas[cambio])
    print(f"A taxa de [bold]{Taxas[cambio]}[/bold] para USD é de: {resultado['conversion_rate']}")