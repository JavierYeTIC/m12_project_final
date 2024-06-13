from fastapi import FastAPI, UploadFile, Request, HTTPException, Depends, Body
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from typing import List
from fastapi_login import LoginManager
import datetime
from db import clientPS, productDB, userDB
from model.Product import Product
from model.User import User, LoginRequest
from schema import jsonPro, jsonProAll, jsonProId

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/img", StaticFiles(directory="img"), name="img")

SECRET = "my-super-secure-secret-key"
manager = LoginManager(SECRET, token_url="/login", use_cookie=True)

try:
    conn = clientPS.client()
except Exception as e:
    print(f"Error connecting to the database: {e}")

#(1, 'informatica', current_timestamp, current_timestamp);
# uvicorn main:app --reload

# Cargar usuarios desde la base de datos
usersMemo = userDB.load_users_from_db()

# Definir la función user_loader
@manager.user_loader
def load_user(email: str):
    # Implementación para cargar el usuario desde donde sea que esté almacenado en tu aplicación
    # Aquí deberías cargar el usuario basado en el email u otro identificador único
    return {"email": email, "username": "username"}

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/me")
def get_me(user: dict = Depends(manager)):
    try:
        if user is not None:
            return user
        else:
            raise HTTPException(status_code=401, detail="User not authenticated")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/indexLogin", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("indexLogin.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/registra", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse("registra.html", {"request": request})

@app.get("/crud", response_class=HTMLResponse)
def crud_page(request: Request):
    return templates.TemplateResponse("crud.html", {"request": request})

@app.get("/inserta", response_class=HTMLResponse)
def inserta_page(request: Request):
    return templates.TemplateResponse("inserta.html", {"request": request})

@app.get("/edit", response_class=HTMLResponse)
def edit_page(request: Request):
    return templates.TemplateResponse("edit.html", {"request": request})

@app.post("/users/", response_model=User)
def create_user(user: User):
    try:
        userDB.registra(user)
        return user
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

@app.post("/login")
def login(credentials: LoginRequest = Body(...)):
    email = credentials.email
    password = credentials.password

    if userDB.comprova(email, password):
       return {"message": "Login successful", "email": email}
    else:
        raise HTTPException(status_code=401, detail="Invalid email or password")

@app.get("/products")
def get_all_products():
    data = productDB.consulta()
    datajson = jsonPro.product_schema(data)
    return datajson

@app.get("/product/{product_id}")
def get_product_by_id(product_id: int):
    product = productDB.consultaiD(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.post("/product/")
def create_product(prod: Product):
    productDB.inserta(prod)
    return {"message": "S'ha afegit correctament"}

@app.put("/product/{id}")
def update_product_by_id(id: int, prod: Product):
    success = productDB.edit(id, prod)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product updated successfully"}

@app.delete("/delete/{id}")
def delete_product_by_id(id: int):
    success = productDB.borrar(id)
    if success:
        return {"message": f"Product with ID {id} deleted successfully!"}
    else:
        raise HTTPException(status_code=404, detail="Product not found")

@app.get("/productAll/")
def all_products():
    data = productDB.productAll()
    datajson = jsonProAll.product_schema(data)
    return datajson

@app.post("/loadProducts")
async def create_upload_file(file: UploadFile):
    csvProducts = productDB.pujarCSV(file)
    return csvProducts
