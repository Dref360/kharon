from fastapi import APIRouter

api = APIRouter()


@api.get("/")
def test():
    return {"message": "unprotected api_app endpoint"}
