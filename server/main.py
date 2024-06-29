from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
from contextlib import asynccontextmanager
from .db.database import Base, engine
from .db.routers import cards, decks, players

app = FastAPI()

# CORS 설정
origins = [
    "http://localhost:3000",  # React 개발 서버
    "http://127.0.0.1:3000",  # React 개발 서버
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="server/static"), name="static")

# 라우터 추가
app.include_router(cards.router)
app.include_router(players.router)
app.include_router(decks.router)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Card Game API"}

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 애플리케이션 시작 시 실행되는 코드
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # 애플리케이션 종료 시 실행되는 코드
    await engine.dispose()

app.router.lifespan_context = lifespan

if __name__ == "__main__":
    uvicorn.run("server.main:app", host="127.0.0.1", port=8000, reload=True)
