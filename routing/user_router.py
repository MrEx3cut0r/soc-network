from fastapi import APIRouter, Depends
from services.user_service import ret_user_service
from services.posts_service import ret_post_service
from services.subscribing_service import ret_subscribing_service


"""
TODO:
add endpoint /subscribe
add endpoint /unsubscribe

"""
router = APIRouter(prefix='/users')

@router.get('/{id}')
def get_user(id: int, post_service: ret_post_service = Depends(), subscribing_service: ret_subscribing_service = Depends()):
	posts = post_service.findById(id)
	
	if posts == False or posts == None:
		return "user not found"
	subscribes = subscribing_service.get(posts.username)
	if subscribes == None:
		subscribes = []
	else:
		subscribes = subscribes.subscribes

	form = f"user: {posts.username}\n{posts}\nsubscribes: {len(subscribes)}"
	return form
