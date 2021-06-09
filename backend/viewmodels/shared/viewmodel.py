from typing import Optional

from starlette.requests import Request

from infrastructure import cookie_auth


class ViewModelBase:

    def __init__(self, request: Request):
        self.request: Request = request
        self.error: Optional[str] = None
        self.user_id: Optional[int] = cookie_auth.get_user_id_via_auth_cookie(self.request)
        self.is_logged_in = self.user_id is not None

        # self.ticker: Optional[str] = None
        # self.pattern: Optional[str] = None

    def to_dict(self) -> dict:
        return self.__dict__
