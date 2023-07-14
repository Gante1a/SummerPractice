from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from sendMessage import MessageSender
from databaseOperations import getInfo

app = FastAPI()
templates = Jinja2Templates(directory="templates")

class MessageInput(BaseModel):
    chat_id: str
    message: str

@app.get("/", response_class=HTMLResponse)
async def show_form_and_data(request: Request):
    combined_user_data = getInfo()
    return templates.TemplateResponse("form.html", {"request": request, "combined_user_data": combined_user_data})

@app.post("/", response_class=HTMLResponse)
async def process_form(request: Request, chat_id: str = Form(...), message: str = Form(...)):
    message_input = MessageInput(chat_id=chat_id, message=message)
    sender = MessageSender(message_input.chat_id, message_input.message)
    await sender.send_message()

    javascript_code = """
        <script>
            setTimeout(function() {
                window.location.href = "/";
            }, 2000);
        </script>
    """

    combined_user_data = getInfo()

    return templates.TemplateResponse("form.html", {"request": request, "combined_user_data": combined_user_data, "javascript_code": javascript_code})

    


