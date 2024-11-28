from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import os
import secrets
import uvicorn
import logging
from typing import Dict

# Настройка логирования
logging.basicConfig(
    filename='D:/Project/Soft/goodNight/server.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

app = FastAPI(title="Power Control API")
security = HTTPBasic()

# Логируем запуск
logging.info("Starting server...")

# Используйте сложный пароль в продакшене!
VALID_USERNAME = "Remart"
VALID_PASSWORD = "Felix&Karamelka18121990"

def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    is_username_correct = secrets.compare_digest(credentials.username, VALID_USERNAME)
    is_password_correct = secrets.compare_digest(credentials.password, VALID_PASSWORD)

    if not (is_username_correct and is_password_correct):
        raise HTTPException(
            status_code=401,
            detail="Неверные учетные данные",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials

@app.get("/sleep", response_model=Dict[str, str])
async def put_to_sleep(credentials: HTTPBasicCredentials = Depends(authenticate)):
    os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
    return {"status": "Компьютер переходит в спящий режим"}

@app.get("/shutdown", response_model=Dict[str, str])
async def shutdown_pc(credentials: HTTPBasicCredentials = Depends(authenticate)):
    os.system("shutdown /s /t 0")
    return {"status": "Компьютер выключается"}

@app.get("/restart", response_model=Dict[str, str])
async def restart_pc(credentials: HTTPBasicCredentials = Depends(authenticate)):
    os.system("shutdown /r /t 0")
    return {"status": "Компьютер перезагружается"}

@app.get("/hibernate", response_model=Dict[str, str])
async def hibernate_pc(credentials: HTTPBasicCredentials = Depends(authenticate)):
    os.system("rundll32.exe powrprof.dll,SetSuspendState 1,1,0")
    return {"status": "Компьютер переходит в режим гибернации"}

if __name__ == "__main__":
    try:
        logging.info("Attempting to start server on port 50000")
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=50000,
            log_config=None
        )
    except Exception as e:
        logging.error(f"Failed to start server: {str(e)}")
