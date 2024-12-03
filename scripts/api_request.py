import requests

class APIRequests:
    @staticmethod
    def save_score(player_name, score):
        try:
            url = "http://127.0.0.1:8000/api/scores/"  # URL da API Django
            data = {"name": player_name, "score": score}
            response = requests.post(url, data=data)
            if response.status_code == 201:
                print("Pontuação salva com sucesso!")
            else:
                print(f"Erro ao salvar pontuação: {response.text}")
        except Exception as e:
            print(f"Erro ao conectar ao servidor: {e}")

    @staticmethod
    def get_ranking():
        try:
            url = "http://127.0.0.1:8000/api/scores/"
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()  # Retorna o ranking como JSON
            else:
                print(f"Erro ao buscar ranking: {response.text}")
                return []
        except Exception as e:
            print(f"Erro ao conectar ao servidor: {e}")
            return []
