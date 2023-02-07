import json
import requests
import google.auth
import google.auth.transport.requests


class ApiManager:
    def __init__(self):
        self._timeout: int = 60
        self._token = None

    def request_post(
            self,
            endpoint: str,
            data_instances: dict
    ) -> requests.Response:
        if self._token is None:
            self._token = self.get_auth_token()

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self._token}"}

        res = requests.post(
            url=endpoint,
            data=json.dumps(data_instances),
            timeout=self._timeout,
            headers=headers)
        return res

    def control_expired_token(
            self,
            response: requests.Response,
            endpoint: str,
            data: dict
    ):
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            self._token = self.get_auth_token()
            r = self.request_post(
                endpoint=endpoint,
                data_instances=data)
            r.raise_for_status()

    def get_auth_token(self) -> object:
        creds, project = google.auth.default()

        auth_req = google.auth.transport.requests.Request()
        creds.refresh(auth_req)

        return creds.token
