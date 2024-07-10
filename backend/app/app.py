from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def get_post():
    return {"message":"fastapi is working"}