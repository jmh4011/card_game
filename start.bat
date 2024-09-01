@echo off

REM 첫 번째 명령 프롬프트 창 - 서버 실행
start cmd /k "cd /d %~dp0server && .\venv\Scripts\activate && uvicorn main:app --reload"

REM 두 번째 명령 프롬프트 창 - 클라이언트 실행
start cmd /k "cd /d %~dp0client && npm start"
