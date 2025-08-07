from database.session import session, connection
from database.redis_enter import client
from repositories.redis_repository import redis_repository
from dtos.user import user
from dtos.subscribe import subscribe
from tables.subscribers_table import subscribers_table
from tables.user_table import user_table
from typing import Optional


class subscribing_repository:
	def __init__(self, session) -> None:
		self.session = session
		self.redisClient = redis_repository(client)

	@connection
	def create_profile(self, username: str) -> None:
		new_user = subscribers_table(username=username, subscribers=[])
		self.session.add(new_user)
		self.session.commit()

	@connection
	def subscribe(self, to: str, current: str) -> Optional[subscribe]:
		profile = self.session.query(subscribers_table).filter_by(username=to).first()
		if profile:
			profile.subscribers.append(current)
			self.redisClient.set(profile.username, profile)
			self.session.add(profile)
			self.session.commit()
			return profile
		return None

	@connection
	def unsubscribe(self, to: str, current: str) -> Optional[bool]:
		profile = self.session.query(subscribers_table).filter_by(username=to).first()
		if profile:
			if current in profile.subscribers:
				profile.subscribers.remove(current)
				self.redisClient.set(profile.username, profile)
				self.session.commit()
				return True
			return False
		return None

	@connection
	def get(self, user: str) -> Optional[list]:
		found = self.redisClient.get(user)
		if not found:
			found = self.session.query(user_table).filter_by(username=user).first()
		if not found:
			return None
		return self.session.query(subscribers_table).filter_by(username=found.username).first()
		
def ret_subscribing_repository() -> subscribing_repository:
	return subscribing_repository(session)