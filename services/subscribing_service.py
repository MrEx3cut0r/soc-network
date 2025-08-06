from repositories.subscribing_repository import subscribing_repository, ret_subscribing_repository
from dtos.user import user
from dtos.subscribe import subscribe
from typing import Optional
class subscribing_service:
	def __init__(self, repository: subscribing_repository) -> None:
		self.repository = repository

	def subscribe(self, to: str, current: str) -> Optional[subscribe]:
		return self.repository.subscribe(to, current)

	def unsubscribe(self, to: str, current: str) -> Optional[bool]:
		return self.repository.unsubscribe(to, current)

	def get(self, user: str) -> Optional[list]:
		return self.repository.get(user)

def ret_subscribing_service() -> subscribing_service:
	repository = ret_subscribing_repository()
	return subscribing_service(repository)
