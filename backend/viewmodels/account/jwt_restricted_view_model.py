from typing import Optional, List
from infrastructure import cookie_auth
from starlette.requests import Request

from viewmodels.shared.viewmodel import ViewModelBase


class JwtRestrictedViewModel(ViewModelBase):
    def __init__(self, request: Request):
        super().__init__(request)

        # is logged in (oauth)
        self.jwt_user_id: Optional[int] = None
        self.jwt_is_logged_in = None

    async def load(self):
        self.jwt_user_id: Optional[int] = await cookie_auth.get_user_id_via_jwt_cookie(self.request)
        self.jwt_is_logged_in = self.jwt_user_id is not None
