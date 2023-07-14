import os
import uvicorn
import saveNewUser
import multiprocessing

if __name__ == "__main__":
    os.chdir(r"C:\Python\fastapiprobui")  
    uvicorn_process = multiprocessing.Process(target=uvicorn.run, args=("main:app",), kwargs={"host": "0.0.0.0", "port": 8000, "reload": True})
    save_new_user_process = multiprocessing.Process(target=saveNewUser.run_user_saver)
    uvicorn_process.start()
    save_new_user_process.start()
    uvicorn_process.join()
    save_new_user_process.join()
