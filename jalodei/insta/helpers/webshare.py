import requests
from django.conf import settings
from typing import List


def webshare_list_ip_authorizations():
    response = requests.get(
        "https://proxy.webshare.io/api/v2/proxy/ipauthorization/",
        headers={"Authorization": settings.WEBSHARE_API_KEY}
    )

    ip_list = []
    id_list = []

    for ip in response.json().get('results'):
        ip_list.append(ip.get('ip_address'))
        id_list.append(ip.get('id'))

    return ip_list, id_list


def webshare_list_proxies() -> List[str]:
    response = requests.get(
        "https://proxy.webshare.io/api/v2/proxy/list/?mode=direct&page=1&page_size=25",
        headers={f"Authorization": settings.WEBSHARE_API_KEY}
    )

    proxy_list = []

    for proxy in response.json().get('results'):
        proxy_list.append(f"{proxy.get('proxy_address')}:{str(proxy.get('port'))}")

    return proxy_list


def webshare_authorize_proxy(proxy_ip):
    response = requests.post(
        "https://proxy.webshare.io/api/v2/proxy/ipauthorization/",
        json={"ip_address": proxy_ip},
        headers={"Authorization": settings.WEBSHARE_API_KEY})

    return response.json()


def webshare_get_my_ip():
    response = requests.get(
        "https://proxy.webshare.io/api/v2/proxy/ipauthorization/whatsmyip/",
        headers={"Authorization": settings.WEBSHARE_API_KEY}
    )

    return response.json().get('ip_address')


def webshare_delete_ip_authorization(auth_id):
    response = requests.delete(
        f"https://proxy.webshare.io/api/v2/proxy/ipauthorization/{auth_id}/",
        headers={"Authorization": settings.WEBSHARE_API_KEY}
    )

