from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import models
from database import engine, get_db

# Эта строчка сама создаст таблицы в базе при запуске
models.Base.metadata.create_all(bind=engine)

app = FastAPI()
templates = Jinja2Templates(directory="templates")

CHECKUPS = {
    "female": {
        "18-30": ["измерение веса", "измерение окружности талии", "измерение артериального давления", "общий анализ крови", "общий анализ мочи", "АСТ", "АЛТ", "ЛПВП", "ЛПНП", "железо", "витамин Д", "Прием у гинеколога", "Пап-тест", "УЗИ органов малого таза"],
        "31-50": ["измерение веса", "измерение окружности талии", "измерение артериального давления", "общий анализ крови", "общий анализ мочи", "АСТ", "АЛТ", "ЛПВП", "ЛПНП", "железо", "глюкоза", "ТТГ", "Т3", "Т4", "витамин Д", "Прием у гинеколога", "Пап-тест", "УЗИ органов малого таза", "УЗИ молочной железы", "УЗИ органов брюшной полости", "УЗИ щитовидной железы", "ЭКГ"],
        "51-100": ["измерение веса", "измерение окружности талии", "измерение артериального давления", "общий анализ крови", "общий анализ мочи", "АСТ", "АЛТ", "ЛПВП", "ЛПНП", "железо", "глюкоза", "ТТГ", "Т3", "Т4", "витамин Д", "Прием у гинеколога", "Пап-тест", "УЗИ органов малого таза", "мамография", "УЗИ органов брюшной полости", "УЗИ щитовидной железы", "прием у кардиолога", "УЗИ сердца", "ЭКГ"]
    },
    "male": {
        "18-30": ["измерение веса", "измерение окружности талии", "измерение артериального давления", "общий анализ крови", "общий анализ мочи", "АСТ", "АЛТ", "ЛПВП", "ЛПНП", "железо", "витамин Д"],
        "31-50": ["измерение веса", "измерение окружности талии", "измерение артериального давления", "общий анализ крови", "общий анализ мочи", "АСТ", "АЛТ", "ЛПВП", "ЛПНП", "железо", "глюкоза", "ТТГ", "Т3", "Т4", "витамин Д", "УЗИ органов брюшной полости", "УЗИ щитовидной железы", "ЭКГ"],
        "51-100": ["измерение веса", "измерение окружности талии", "измерение артериального давления", "общий анализ крови", "общий анализ мочи", "АСТ", "АЛТ", "ЛПВП", "ЛПНП", "железо", "глюкоза", "ТТГ", "Т3", "Т4", "витамин Д", "УЗИ органов брюшной полости", "УЗИ щитовидной железы", "прием у кардиолога", "УЗИ сердца", "ЭКГ"]
    }
}

@app.post("/register")
def register_user(
    username: str = Form(...),
    full_name: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    # Простая проверка: нет ли уже такого пользователя
    existing_user = db.query(models.User).filter(models.User.username == username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Логин уже занят")
    
    # Пока сохраняем пароль как есть (в идеале нужно хешировать)
    new_user = models.User(
        username=username,
        full_name=full_name,
        hashed_password=password 
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "Пользователь успешно создан!", "user": new_user.username}

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/form", response_class=HTMLResponse)
async def get_form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

@app.post("/result", response_class=HTMLResponse)
async def post_result(request: Request, gender: str = Form(...), age: int = Form(...)):
    # Определяем возрастную группу
    if 18 <= age <= 30:
        group = "18-30"
    elif 31 <= age <= 50:
        group = "31-50"
    else:
        group = "51-100"
    
    recommendations = CHECKUPS[gender][group]
    gender_text = "Женщина" if gender == "female" else "Мужчина"
    
    return templates.TemplateResponse("result.html", {
        "request": request,
        "age": age,
        "gender": gender_text,
        "recommendations": recommendations
    })

@app.get("/register", response_class=HTMLResponse)
def get_register_form():
    with open("templates/register.html", "r", encoding="utf-8") as f:
        return f.read()