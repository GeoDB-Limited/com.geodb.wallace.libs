import json
import requests
import google.auth
import google.auth.transport.requests


class ApiManager:
    def __init__(self):
        self.timeout: int = 60

    def request_post(
            self,
            endpoint: str,
            token: object,
            data_instances: dict
    ) -> requests.Response:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"}
        res = requests.post(
            url=endpoint,
            data=json.dumps(data_instances),
            timeout=self.timeout,
            headers=headers)
        return res

    def control_expired_token(
            self,
            response: requests.Response,
            endpoint: str,
            data: dict,
            token: object
    ) -> object:
        try:
            response.raise_for_status()
            return token
        except requests.exceptions.HTTPError as e:
            token: object = self.get_auth_token()
            r = self.request_post(
                endpoint=endpoint,
                token=self.get_auth_token(),
                data_instances=data)
            r.raise_for_status()
            return token

    def get_auth_token(self) -> object:
        creds, project = google.auth.default()

        auth_req = google.auth.transport.requests.Request()
        creds.refresh(auth_req)

        return creds.token
