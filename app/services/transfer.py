import requests

def transfer():
    url = 'https://run.mocky.io/v3/5794d450-d2e2-4412-8131-73d0293ac1cc'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data.get('message') == 'Autorizado':
            return True
        else:
            return False
    else:
        return False