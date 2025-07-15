from fastapi import FastAPI
from dotenv import load_dotenv

from routers.users import router as UsersRouter
from routers.posts import router as PostsRouter

load_dotenv()

app = FastAPI(title="Blog")


@app.get("/", status_code=200)
def health_check():
    return "OK"


app.include_router(UsersRouter)
app.include_router(PostsRouter)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8888)
