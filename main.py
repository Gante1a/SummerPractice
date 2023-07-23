from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sendMessage import MessageSender
from databaseOperations import getUsersInfo, insert_key, delete_user, getKeysInfo, delete_key, getMessagesInfo

app = FastAPI()

templates = Jinja2Templates(directory="")
    
''''кнопка отправки сообщения, добавления ключа'''    
@app.post("/", response_class=HTMLResponse)
async def process_form(chat_id: str = Form(None), message: str = Form(None), key: str = Form(None), official_name: str = Form(None)):
    try:
        if chat_id and message:
            await MessageSender(chat_id, message).send_message()
        elif key and official_name:
            insert_key(key, official_name)
        return RedirectResponse(url="/", status_code=303)
    except Exception as e:
        error_message = str(e)
        if "Ключ уже существует" in error_message:  
            return JSONResponse(content={"error_message": error_message}, status_code=400)  
        else:
            return JSONResponse(content={"error_message": f"Error: {error_message}"}, status_code=500)
'''кнопка удаления пользователя'''   
@app.post("/delete", response_class=HTMLResponse)
async def delete_user_by_chat_id(chat_id: str = Form(...)):
    try:
        delete_user(chat_id)
        return RedirectResponse(url="/", status_code=303)
    except Exception as e:
        return JSONResponse(content={"error_message": f"Error: {str(e)}"}, status_code=500)
 
'''вывод таблицы о пользователях и таблицы о ключах'''
@app.get("/", response_class=HTMLResponse)
async def show_form_and_data(request: Request):
    try:
        users_data = getUsersInfo()
        keys_data = getKeysInfo()
        return templates.TemplateResponse("form.html", {"request": request, "combined_user_data": users_data, "keys_data": keys_data})
    except Exception as e:
        return JSONResponse(content={"error_message": f"Error: {str(e)}"}, status_code=500)
    
'''кнопка удаления ключа'''    
@app.post("/delete-key", response_class=HTMLResponse)
async def delete_key_by_key(key: str = Form(...)):
    try:
        delete_key(key)
        return RedirectResponse(url="/", status_code=303)
    except Exception as e:
        return JSONResponse(content={"error_message": f"Error: {str(e)}"}, status_code=500) 
      
'''вывод таблицы с сообщениями по новой ссылке'''     
@app.get("/messages", response_class=HTMLResponse)
async def show_messages(request: Request):
    try:
        messages_data = getMessagesInfo()
        return templates.TemplateResponse("messages.html", {"request": request, "messages_data": messages_data})
    except Exception as e:
        return JSONResponse(content={"error_message": f"Error: {str(e)}"}, status_code=500)    