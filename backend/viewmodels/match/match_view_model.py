from typing import Optional, List

from starlette.requests import Request
from services import user_service, match_service
from viewmodels.shared.viewmodel import ViewModelBase


class MatchViewModel(ViewModelBase):
    def __init__(self, request: Request):
        super().__init__(request)

        # self.ticker_search = Optional[str] = None
        self.ticker: Optional[str] = None
        self.pattern: Optional[str] = None
        self.page: Optional[int] = 0
        self.candidates: List = []
        self.warning: str = ""

    async def receive(
            self,
            ticker: Optional[str] = None,
            pattern: Optional[str] = None,
            page: Optional[int] = 0
    ):

        print("VM: receive...")
        print(f"PARAM: ticker: {ticker}")
        # print(f"PARAM: ticker is not None: {ticker != None}")
        print(f"PARAM: pattern: {pattern}")
        # print(f"PARAM: pattern is not None: {pattern != None}")
        # print(f"PARAM: pattern str of None: {pattern == 'None'}")
        print(f"PARAM: page: {page}")

        self.ticker = ticker
        self.pattern = pattern
        self.page = page

        ret = \
            await match_service.pull_candidates(
                ticker=ticker,
                pattern=pattern,
                page=page
            )

        self.candidates: List = ret[0]
        self.warning: str = ret[1]

        if len(self.candidates) == 0:
            self.error = "Your query returned no results"
        elif self.warning != "":
            self.error = self.warning

    async def load(self):
        form = await self.request.form()
        # self.ticker = form.get('ticker_search')
        # print(type(Form(form.get('ticker'))))
        # print(Form(form.get('ticker')))
        self.ticker = form.get('ticker')
        self.pattern = form.get('pattern')
        self.page: Optional[int] = 0

        print("VM: load...")
        print(f"PARAM: ticker: {self.ticker}")
        # print(f"PARAM: ticker is not None: {self.ticker != None}")
        print(f"PARAM: pattern: {self.pattern}")
        # print(f"PARAM: pattern is not None: {self.pattern != None}")
        # print(f"PARAM: pattern str of None: {self.pattern == 'None'}")
        print(f"PARAM: page: {self.page}")

        # print(self.ticker)
        # print(self.pattern)
        # print(self.candidates)

        # self.error = "......................................"
        #
        if not self.ticker and not self.pattern:
            self.error = "You must select a filter"
        elif (self.ticker == 'Any' or not self.ticker) and self.pattern == 'Any':
            self.error = "You must select a filter"
        elif not self.ticker:
            self.ticker = "Any"
