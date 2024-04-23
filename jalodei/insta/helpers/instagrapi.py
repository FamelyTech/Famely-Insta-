from instagrapi import Client
from .webshare import *


def instagrapi_set_proxy(proxy) -> Client:
    my_ip = webshare_get_my_ip()

    authorized_ips, authorized_ids = webshare_list_ip_authorizations()

    if my_ip not in authorized_ips:
        for auth_id in authorized_ids:
            webshare_delete_ip_authorization(auth_id)
        webshare_authorize_proxy(my_ip)

    cl = Client()

    if proxy in webshare_list_proxies():
        cl.set_proxy(f"{proxy}")

    return cl


def instagrapi_login_client(cl: Client, username: str, password: str, new_session: bool = True) -> Client:
    try:
        cl.load_settings("session.json")
        cl.login(username, password)
    except Exception as e:
        cl.login(username, password)
        cl.dump_settings("session.json")

    return cl


def instagrapi_error_context(e):
    error_type = type(e).__name__
    recommendation = ''
    if error_type == "RetryError":
        recommendation = "Confirm that you can access your Instagram account on your phone."

    context = {'error': type(e).__name__,
               'recommendation': recommendation}

    return context
