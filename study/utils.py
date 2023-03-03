import requests


def check_status(payment_id=2423967522):
    return requests.get(f'localhost:8000/study/payment_status/{2423967522}/')



