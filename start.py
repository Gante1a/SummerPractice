import os
import uvicorn
from saveNewUser import UserSaver
import multiprocessing
import asyncio

async def main():
    os.chdir(r"C:\Python\fastapiprobui")
    # Запуск сервера с FastAPI
    uvicorn_process = multiprocessing.Process(target=uvicorn.run, args=("main:app",), kwargs={"host": "0.0.0.0", "port": 8000, "reload": True})
    uvicorn_process.start()
    # Запуск асинхронного цикла UserSaver
    await UserSaver().run()

if __name__ == "__main__":
    asyncio.run(main())
