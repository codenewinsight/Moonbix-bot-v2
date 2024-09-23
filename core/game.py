import requests
import time

from smart_airdrop_claimer import base
from core.headers import headers
from core.info import get_info


def start_game(token, proxies=None):
    url = "https://www.binance.com/bapi/growth/v1/friendly/growth-paas/mini-app-activity/third-party/game/start"
    payload = {"resourceId": 2056}

    try:
        response = requests.post(
            url=url,
            headers=headers(token=token),
            json=payload,
            proxies=proxies,
            timeout=20,
        )
        data = response.json()
        return data
    except:
        return None


def play_game(start_game_data, proxies=None):
    url = "https://moonbix-server-9r08ifrt4-scriptvips-projects.vercel.app/moonbix/api/v1/play"
    payload = {"game_response": start_game_data}

    try:
        response = requests.get(
            url=url,
            json=payload,
            proxies=proxies,
            timeout=20,
        )
        data = response.json()
        payload = data["game"]["payload"]
        point = data["game"]["log"]
        return payload, point
    except:
        return None, None


def complete_game(token, payload, point, proxies=None):
    url = "https://www.binance.com/bapi/growth/v1/friendly/growth-paas/mini-app-activity/third-party/game/complete"
    payload = {
        "resourceId": 2056,
        "payload": payload,
        "log": point,
    }

    try:
        response = requests.post(
            url=url,
            headers=headers(token=token),
            json=payload,
            proxies=proxies,
            timeout=20,
        )
        data = response.json()
        status = data["success"]
        return status
    except:
        return None


def process_play_game(token, proxies=None):
    while True:
        start_game_data = start_game(token=token, proxies=proxies)
        start_game_code = start_game_data["code"]

        if start_game_code == "000000":
            payload, point = play_game(start_game_data=start_game_data, proxies=proxies)
            if payload:
                base.log(f"{base.yellow}Playing for 45 seconds...")
                time.sleep(45)
                complete_game_status = complete_game(
                    token=token, payload=payload, point=point, proxies=proxies
                )
                if complete_game_status:
                    base.log(
                        f"{base.white}Auto Play Game: {base.green}Success | Added {point} points"
                    )
                    get_info(token=token, proxies=proxies)
                    time.sleep(1)
                else:
                    base.log(f"{base.white}Auto Play Game: {base.red}Fail")
                    break
            else:
                base.log(f"{base.white}Auto Play Game: {base.red}Fail")
                break
        elif start_game_code == "116002":
            base.log(f"{base.white}Auto Play Game: {base.red}No attempt to play")
            break
        else:
            error_message = start_game_data["messageDetail"]
            base.log(f"{base.white}Auto Play Game: {base.red}Error - {error_message}")
            break
