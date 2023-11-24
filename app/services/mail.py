import requests
from flask import flash


def simulate_email_notification(receiver_email):
    url = 'https://run.mocky.io/v3/54dc2cf1-3add-45b5-b5a9-6bf7e7f1f4a6'
    payload = {
        "receiver_email": receiver_email,
        "message": "Simulação de e-mail de notificação de transferência"
    }

    response = requests.post(url, json=payload)

    if response.status_code == 200:
        flash("E-mail de transferência enviado com sucesso.")
    else:
        flash("Falha ao enviar e-mail de transferência.")
