import requests
import pandas as pd
import time

def buscar_precos_binance(simbolos):
    """
    Busca os preços das criptomoedas usando a API da Binance.
    """
    url = "https://api.binance.com/api/v3/ticker/24hr"
    dados = []
    
    for simbolo in simbolos:
        try:
            resposta = requests.get(url, params={"symbol": simbolo})
            if resposta.status_code == 200:
                dados.append(resposta.json())
            else:
                print(f"Erro ao buscar o par {simbolo}. Código: {resposta.status_code}")
        except Exception as e:
            print(f"Erro ao processar {simbolo}: {e}")
    
    # Transformar em DataFrame
    if len(dados) > 0:
        df = pd.DataFrame(dados)
        df = df[["symbol", "lastPrice", "priceChangePercent", "volume"]]
        df.columns = ["Par Cripto", "Último Preço (USDT)", "Variação 24h (%)", "Volume 24h"]
        
        # Formatar os dados
        df["Último Preço (USDT)"] = df["Último Preço (USDT)"].astype(float).round(4)
        df["Variação 24h (%)"] = df["Variação 24h (%)"].astype(float).round(2)
        df["Volume 24h"] = df["Volume 24h"].astype(float).round(2)
        
        return df
    else:
        return pd.DataFrame()

# Programa principal
if __name__ == "__main__":
    pares_cripto = ["BTCUSDT", "ETHUSDT", "XLMUSDT", "SHIBUSDT", "DOGEUSDT"]
    
    while True:
        print("\nBuscando preços de criptomoedas na Binance...")
        tabela = buscar_precos_binance(pares_cripto)
        
        if not tabela.empty:
            print(tabela)
        else:
            print("Não foi possível obter os dados.")
        
        print("\n--- Atualização a cada 60 segundos ---")
        time.sleep(60)
