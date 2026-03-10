from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register")
def register():
    return {"result" : "registered user"}

@router.post("/login")
def login():
    return {"token" : "12345"}

@router.post("/logout")
def logout():
    return {"result" : "logout user"}

