import requests

def encurtar_url(url):
    # Endpoint da API do is.gd para encurtar URLs
    isgd_api_url = f'https://is.gd/create.php?format=json&url={url}'

    # Enviar a requisição para encurtar a URL
    response = requests.get(isgd_api_url)

    # Obter o link encurtado da resposta da API
    if response.status_code == 200:
        shortened_link = response.json()['shorturl']
        return shortened_link
    else:
        return None

