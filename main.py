from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sendMessage import MessageSender
from databaseOperations import getInfo, insert_key, DatabaseError

app = FastAPI()

templates = Jinja2Templates(directory="")

@app.get("/", response_class=HTMLResponse)
async def show_form_and_data(request: Request):
    try:
        # Обработка вывода данных о пользователях
        users_data = getInfo()
        return templates.TemplateResponse("form.html", {"request": request, "combined_user_data": users_data})
    except DatabaseError as e:
        return templates.TemplateResponse("error.html", {"request": request, "error_message": str(e)})

@app.post("/", response_class=HTMLResponse)
async def process_form(request: Request, chat_id: str = Form(None), message: str = Form(None), key: str = Form(None), official_name: str = Form(None)):
    try:
        if chat_id and message:
            '''Обработка отправки сообщения с помощью sendMessage.py'''
            await MessageSender(chat_id, message).send_message()
        elif key and official_name:
            # Обработка добавления ключа в базу данных
            insert_key(key, official_name)
        return RedirectResponse(url="/", status_code=303)
    except DatabaseError as e:
        return templates.TemplateResponse("error.html", {"request": request, "error_message": str(e)})
    except Exception as e:
        return templates.TemplateResponse("error.html", {"request": request, "error_message": "Произошла ошибка"})
