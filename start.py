import os
import uvicorn
from saveNewUser import UserSaver
import multiprocessing
import asyncio

async def main():
    '''Запуск сервера fastapi и асинхронного цикла UserSaver.py одновременно'''
    try:
        # Запуск серевра fastapi
        os.chdir(r"C:\Python\fastapiprobui")
    except FileNotFoundError:
        raise Exception("Ошибка: Указанная директория не существует или путь некорректен.")
    uvicorn_process = multiprocessing.Process(target=uvicorn.run, args=("main:app",), kwargs={"host": "0.0.0.0", "port": 8000, "reload": True})
    uvicorn_process.start()

    try:
        # Запуск асинхронного цикла UserSaver.py
        await UserSaver().run()
    except RuntimeError as e:
        raise Exception(f"Ошибка выполнения асинхронного цикла UserSaver: {str(e)}")
    except Exception as e:
        raise Exception(f"Ошибка в асинхронном цикле UserSaver: {str(e)}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Программа остановлена вручную")
    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")
