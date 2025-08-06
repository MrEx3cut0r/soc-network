from database.session import session, connection
from database.redis_enter import client
from repositories.redis_repository import redis_repository
from dtos.user import user
from dtos.subscribe import subscribe
from tables.subscribers_table import subscribers_table
from tables.user_table import user_table
from typing import Optional


# bad code, i will fix it later

class subscribing_repository:
	def __init__(self, session) -> None:
		self.session = session
		self.redisClient = redis_repository(client)

	@connection
	def subscribe(self, to: str, current: str) -> Optional[subscribe]:
		user = self.redisClient.get(to)
		current_user = self.redisClient.get(current)
		if not current_user:
			current_user = self.session.query(user_table).filter_by(username=current).first()
		if not user:
			user = self.session.query(user_table).filter_by(username=to).first()
		if not user or not current_user:
			return None
		profile = self.session.query(subscribers_table).filter_by(username=to).first()
		if profile:
			profile.subcribers = profile.subscribers + current
		else:
			profile = subscribe(username=to.username, subcribers=[current])
		self.session.add(profile)
		self.session.commit()
		return profile


	@connection
	def unsubscribe(self, to: str, current: str) -> Optional[bool]:
		user = self.redisClient.get(to)
		current_user = self.redisClient.get(current)
		if not current_user:
			current_user = self.session.query(user_table).filter_by(username=current).first()
		if not user:
			user = self.session.query(user_table).filter_by(username=to).first()
		if not user or not current_user:
			return None
		profile = self.session.query(subscribers_table).filter_by(username=to).first()
		if profile:
			profile.subcribers.remove(current)
			return True
		return False

	@connection
	def get(self, user: str) -> Optional[list]:
		found = self.redisClient.get(user)
		if not found:
			found = self.session.query(user_table).filter_by(username=user).first()
		if not found:
			return None
		return self.session.query(subscribers_table).filter_by(username=found.username).first()
	
	# P.S. variables 'to' and 'current' is usernames
	
def ret_subscribing_repository() -> subscribing_repository:
	return subscribing_repository(session)