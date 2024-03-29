from django.shortcuts import render, HttpResponse
import requests
import pandas as pd


def home(request):
    return render(request, "home.html")


def download(request):
    url = 'https://www.fundsexplorer.com.br/wp-json/funds/v1/get-ranking'
    headers = {
        'authority': 'www.fundsexplorer.com.br',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'cookie': 'suno_checkout_userid=99063ed5-9640-49b8-9174-57ade01d34bf; colunas_ranking=Fundos%2CSetor%2CPre%C3%A7o%20Atual%20(R$)%2CLiquidez%20Di%C3%A1ria%20(R$)%2CP/VP%2CDividend%20Yield%2CVaria%C3%A7%C3%A3o%20Pre%C3%A7o%2CPatrim%C3%B4nio%20L%C3%ADquido%2CNum.%20Cotistas; popup=popup-funds.com; cf_clearance=3IQD6NoiXV1qXmFTWhzLW9l1bAbaOBBO0LpSeOjU3OU-1711666139-1.0.1.1-3lhYm.3z0uYtoivzTAbDiNQ_WOepIa5_il9Qga0Nt3.5NdP6hYGIYdMWarG7HTWT3DQiUTwIuG0ZMJHNkKpdqA',
        'referer': 'https://www.fundsexplorer.com.br/ranking',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Opera";v="106"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 OPR/106.0.0.0',
        'x-funds-nonce': '61495f60b533cc40ad822e054998a3190ea9bca0d94791a1da'
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            df = pd.read_json(data)
            df.to_csv('fundos.csv')

            # Gerar a resposta HTTP com o arquivo CSV
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename=fundos.csv'
            with open('fundos.csv', 'rb') as f:
                response.write(f.read())

            return response
        else:
            raise Exception(f'Falha ao baixar dados: {response.status_code}')

    except Exception as e:
        print(f'Erro ao baixar dados: {e}')
        return render(request, 'error.html', {'error_message': str(e)})

