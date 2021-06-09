from typing import List

from starlette.requests import Request

# from data.package import Package
# from services import package_service, user_service
from viewmodels.shared.viewmodel import ViewModelBase


class IndexViewModel(ViewModelBase):
    def __init__(self, request: Request):
        super().__init__(request)

        # constructor ^ cannot be async, so have to init these with something
        self.release_count: int = 0
        self.user_count: int = 0
        self.package_count: int = 0
        self.packages: List = []

    async def load(self):
        pass
        # todo: add these back
        # self.release_count: int = await package_service.release_count()
        # self.user_count: int = await user_service.user_count()
        # self.package_count: int = await package_service.package_count()
        # self.packages: List[Package] = await package_service.latest_packages(limit=7)
