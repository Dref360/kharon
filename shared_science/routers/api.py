from fastapi import APIRouter

api = APIRouter()


@api.get('/protected')
def test2(current_email: str):
    return {'message': 'protected api_app endpoint', 'current_email': current_email}
