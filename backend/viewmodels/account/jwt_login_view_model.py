from typing import Optional, List
from infrastructure import cookie_auth
from starlette.requests import Request

from viewmodels.shared.viewmodel import ViewModelBase


class JwtLoginViewModel(ViewModelBase):
    def __init__(self, request: Request):
        super().__init__(request)

        # form input properties
        self.email: Optional[str] = None
        self.password: Optional[str] = None

    async def load(self):
        form = await self.request.form()
        self.email: str = form.get("email")
        self.password: str = form.get("password")

        if not self.email:
            self.error = "You must give an email"

        elif not self.password:
            self.error = "You must give a password"
