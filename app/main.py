from fastapi import FastAPI, status, HTTPException
from app.database import Base, engine
from app.users.routes import router as user_router

app = FastAPI()


Base.metadata.create_all(bind=engine)
app.include_router(user_router)  # Already has prefix="/users" in routes.py


@app.get("/", status_code=status.HTTP_200_OK)
def health_check():
    return {"message": "Success", "status_code": status.HTTP_200_OK}