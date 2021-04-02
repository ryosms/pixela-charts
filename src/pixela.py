from datetime import date
from typing import Optional, Tuple

from requests import Session

GraphDefResult = Tuple[Optional[dict], Optional[str]]
PixelsResult = Tuple[Optional[list], Optional[str]]


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

    def load_graph_definitions(self) -> GraphDefResult:
        res = self._get('')
        if res.ok:
            graph_defs = {}
            graph_list: list = res.json()['graphs']
            for g in graph_list:
                graph_defs[g['id']] = g
            return graph_defs, None
        return None, res.text

    def load_pixels(self, graph_id: str, from_date: date, to_date: date) -> PixelsResult:
        params = {'from': f"{from_date:%Y%m%d}",
                  'to': f"{to_date:%Y%m%d}",
                  'withBody': 'true'}
        res = self._get(f"/{graph_id}/pixels", params)
        if res.ok:
            return res.json()['pixels'], None
        return None, res.text

    def _get(self, path: str, params: Optional[dict] = None):
        session = Session()
        session.headers = self.headers
        if params:
            session.params = params
        res = session.get(f"{self.base_endpoint}{path}")
        session.close()
        return res
