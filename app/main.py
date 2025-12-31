from fastapi import FastAPI, status, HTTPException

app = FastAPI()

@app.get("/", status_code=status.HTTP_200_OK)
def health_check():
    return {"message": "Success", "status_code": status.HTTP_200_OK}