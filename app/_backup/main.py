from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
    return {"Data": "Welcome to SQUAD2"}
