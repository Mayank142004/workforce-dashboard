import requests
from config import ERP_BASE_URL, ERP_API_KEY, ERP_API_SECRET

HEADERS = {
    "Authorization": f"token {ERP_API_KEY}:{ERP_API_SECRET}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}


def erp_get(endpoint, params=None):
    url = ERP_BASE_URL + endpoint
    r = requests.get(url, headers=HEADERS, params=params, timeout=20)
    r.raise_for_status()
    return r.json()


def erp_post(endpoint, payload):
    url = ERP_BASE_URL + endpoint
    r = requests.post(url, headers=HEADERS, json=payload, timeout=20)
    r.raise_for_status()
    return r.json()


def erp_put(endpoint, payload):
    url = ERP_BASE_URL + endpoint
    r = requests.put(url, headers=HEADERS, json=payload, timeout=20)
    r.raise_for_status()
    return r.json()
