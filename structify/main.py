from fastapi import FastAPI

app = FastAPI()


@app.get("/health")
async def check_health(url: str):
    return {"status": "I am alive!"}
