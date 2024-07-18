from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
from contextlib import asynccontextmanager
from database import Base, engine
from routers import decks, players,cards
import logging
import asyncio
from starlette.middleware.base import BaseHTTPMiddleware

app = FastAPI()


logging.getLogger('sqlalchemy.engine.Engine').setLevel(logging.ERROR)
logging.getLogger('sqlalchemy').setLevel(logging.ERROR)
logging.getLogger('sqlalchemy.pool').setLevel(logging.ERROR)
logging.basicConfig(level=logging.INFO)

# 클라이언트별 큐 저장소
client_queues: dict[str, asyncio.Queue] = {}

# 로깅 설정
logger = logging.getLogger(__name__)

class QueueMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            # 클라이언트 IP 추출
            client_ip = request.client.host
            if client_ip in ('127.0.0.1', 'localhost', None):
                client_ip = request.headers.get('X-Forwarded-For', client_ip)

            logger.info(f"Received request from {client_ip}")

            if client_ip not in client_queues:
                client_queues[client_ip] = asyncio.Queue()

            queue = client_queues[client_ip]

            await queue.put(request)
            response = Response("Too many requests", status_code=429)
            if queue.qsize() == 1:  # 첫 번째 요청인 경우 처리 시작
                logger.info(f"Starting to process queue for client {client_ip}")
                try:
                    while not queue.empty():
                        req = await queue.get()
                        logger.info(f"Processing request for client {client_ip}")
                        response = await call_next(req)
                        await asyncio.sleep(0)  # 작업 대기 시뮬레이션
                        logger.info(f"Finished processing request for client {client_ip}")
                finally:
                    if client_ip in client_queues:
                        del client_queues[client_ip]
                    logger.info(f"Finished processing all requests for client {client_ip}")
            return response
        except Exception as e:
            logger.error(f"Error processing request: {e}")
            return Response("Internal Server Error", status_code=500)

# app.add_middleware(QueueMiddleware)

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


app.mount("/static", StaticFiles(directory="static"), name="static")

# 라우터 추가
app.include_router(players.router)
app.include_router(decks.router)
app.include_router(cards.router)

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
