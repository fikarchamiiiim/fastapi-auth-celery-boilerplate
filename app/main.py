from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import authenticate_user, create_access_token, get_current_user
from app.celery_worker import background_task
from app.crud import create_user

app = FastAPI()

@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/users/")
async def create_new_user(username: str, password: str, db: Session = Depends(get_db)):
    return create_user(db, username, password)

@app.get("/protected/")
async def read_protected_data(current_user: dict = Depends(get_current_user)):
    return {"user": current_user.username}

@app.post("/background-task/")
async def run_background_task(data: str):
    task = background_task.delay(data)
    return {"task_id": task.id}
