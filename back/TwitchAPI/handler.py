import requests
from typing import List, Dict


class TwitchAPIHandler:
    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.base_url = "https://api.twitch.tv/helix"
        self.access_token = self._get_access_token()
        self.headers = {
            "Client-ID": self.client_id,
            "Authorization": f"Bearer {self.access_token}"
        }

    def _get_access_token(self) -> str:
        auth_url = "https://id.twitch.tv/oauth2/token"
        params = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "client_credentials"
        }
        response = requests.post(auth_url, params=params)
        return response.json().get("access_token")

    def get_users_data(self, logins: List[str]) -> List[Dict]:
        users_data = []
        for i in range(0, len(logins), 100):
            batch = logins[i:i + 100]
            params = [("login", login) for login in batch]

            response = requests.get(
                f"{self.base_url}/users",
                headers=self.headers,
                params=params
            )

            if response.status_code != 200:
                print(f"Ошибка запроса: {response.text}")
                continue

            data = response.json()
            users_data.extend(data.get("data", []))

        return users_data