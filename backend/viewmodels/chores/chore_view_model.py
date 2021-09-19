from typing import Optional, List

from starlette.requests import Request

from data.models.chore import Chore

from services import chore_service
from viewmodels.shared.viewmodel import ViewModelBase


class ChoreViewModel(ViewModelBase):
    def __init__(self, request: Request):
        super().__init__(request)
        self.chores: List[Chore] = []
        self.chore_id: Optional[int] = None

        # form input properties
        self.chore_name: Optional[str] = None
        self.category: Optional[str] = None
        self.type: Optional[str] = None
        self.alert_days: Optional[int] = None

    async def load(self, chore_id: Optional[int] = False):
        self.chores = \
            await chore_service.get_user_chores(
                    user_id=self.user_id,
                    chore_id=chore_id
                )

        print(f"# User ID...{self.user_id}")
        if not chore_id:
            # to avoid this error:
            #  TypeError: object of type 'Chore' has no len()
            print(f"# Chores Saved...{len(self.chores)}")

            if len(self.chores) == 0:
                self.error = "You have no chores saved yet."

        print(f"Chores:{self.chores}")
        if not self.chores:
            self.error = "You have no chores saved yet."

    async def add_chore(self):
        form = await self.request.form()
        self.chore_name: str = form.get("name")
        self.category: str = form.get("category")
        self.type: str = form.get("type")
        self.alert_days: Optional[int] = form.get("alert_days")

        if not self.chore_name:
            self.error = "You must name your chore"

        elif not self.category:
            self.error = "You must choose a chore category"

        elif not self.type:
            self.error = "You must specify what type of chore"

        elif not self.alert_days:
            self.error = "You must choose an alert # of days"

