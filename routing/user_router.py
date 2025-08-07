from fastapi import APIRouter, Depends, Request
from services.user_service import ret_user_service
from services.posts_service import ret_post_service
from services.subscribing_service import ret_subscribing_service


"""
TODO:
add endpoint /subscribe
add endpoint /unsubscribe

"""
router = APIRouter(prefix='/users')

@router.get('/{username}')
def get_user(username: str, post_service: ret_post_service = Depends(), subscribing_service: ret_subscribing_service = Depends()):
	posts = post_service.findByUsername(username)
	if posts == None:
		return "user not found"
	subscribes = subscribing_service.get(username)
	if subscribes == None:
		return "user not found"
	return {"username": username, "publications": posts, "subscribers": subscribes}

@router.post('/subscribe')
def subscribe(username: str, request: Request, subscribing_service: ret_subscribing_service = Depends()):
	if username == request.state.user:
		return "you cant subscribe on yourself!"
	return subscribing_service.subscribe(username, request.state.user)

@router.post('/unsubscribe')
def unsubscribe(username: str, request: Request, subscribing_service: ret_subscribing_service = Depends()):
	if username == request.state.user:
		return "you cant do this!"
	sub = subscribing_service.unsubscribe(username, request.state.user)
	if sub == None:
		return "user not found"

	return sub