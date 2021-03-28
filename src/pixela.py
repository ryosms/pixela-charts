from typing import Optional

from requests import Session, HTTPError


class Pixela:
    def __init__(self, username, token):
        self.username = username
        self.base_endpoint = f'https://pixe.la/v1/users/{username}/graphs'
        self.headers = {
            'X-USER-TOKEN': token,
            'User-Agent': 'pixela-chart (https://github.com/ryosms/pixela-charts)',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        self.last_error = ""

    def last_error(self):
        return self.last_error

    def load_graph_definitions(self) -> Optional[dict]:
        res = self._get('')
        if res.ok:
            graph_defs = {}
            graph_list: list = res.json()['graphs']
            for g in graph_list:
                graph_defs[g['id']] = g
            return graph_defs
        self.last_error = res.content

        return None

    def _get(self, path: str):
        try:
            session = Session()
            session.headers = self.headers
            res = session.get(f"{self.base_endpoint}{path}")
            session.close()
            return res
        except HTTPError as e:
            self.last_error = e.strerror
