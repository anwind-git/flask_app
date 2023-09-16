from starlette.templating import Jinja2Templates
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from models import *
from werkzeug.security import generate_password_hash, check_password_hash
import utils

metadata.create_all(engine)

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/users/")
async def read_users():
    query = users.select()
    return await db.fetch_all(query)


@app.get("/users/{user_id}", response_model=Users)
async def read_user(user_id: int):
    query = users.select().where(users.c.user_id == user_id)
    return await db.fetch_one(query)


@app.post('/login')
async def login(request: Request):
    if request.method == 'POST':
        form_data = await request.form()
        query = users.select().where(users.c.email == form_data['authorizationEmail'])
        user = await db.fetch_all(query)
        selected_field = [item.password for item in user]
        result = ''.join(selected_field)
        if user and check_password_hash(result, form_data['authorizationPassword']):
            return user
        else:
            return "Неверный email или пароль"


@app.post("/users/", response_model=Users)
async def create_user(user: Users):
    query = users.insert().values(user_id=user.user_id, last_name=user.last_name, first_name=user.first_name,
                                  email=user.email,
                                  password=generate_password_hash(user.password))
    last_record_id = await db.execute(query)
    return {**user.model_dump(), "id": last_record_id}


@app.put("/users/{user_id}", response_model=Users)
async def update_user(user_id: int, new_user: Users):
    query = users.update().where(users.c.user_id == user_id).values(user_id=new_user.user_id, last_name=new_user.last_name,
                                                                    first_name=new_user.first_name, email=new_user.email,
                                                                    password=generate_password_hash(new_user.password))
    await db.execute(query)
    return {**new_user.model_dump(), "id": user_id}


@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    query = users.delete().where(users.c.user_id == user_id)
    await db.execute(query)
    return {'message': 'User deleted'}


@app.get("/")
async def index(request: Request):
    query = items.select()
    item = await db.fetch_all(query)
    return templates.TemplateResponse("index.html", {"request": request, "items": item,
                                                     'title': utils.menu_header[0]['title'],
                                                     'settings': utils})


@app.get("/items/{slug}", response_model=Items)
async def read_item(request: Request, slug: str):
    query = items.select().where(items.c.slug == slug)
    item = await db.fetch_all(query)
    for link in utils.categories:
        if link['slug'] == slug:
            cat = link['name'].lower()
    return templates.TemplateResponse("index.html", {"request": request, "title": cat,
                                                     "slug": slug, "items": item, 'settings': utils})


@app.post("/items/", response_model=Items)
async def create_item(item: Items):
    query = items.insert().values(item_id=item.item_id, title=item.title, slug=item.slug, description=item.description,
                                  price=item.price)
    last_record_id = await db.execute(query)
    return {**item.model_dump(), "id": last_record_id}


@app.put("/items/{item_id}", response_model=Items)
async def update_item(item_id: int, new_item: Items):
    query = items.update().where(items.c.item_id == item_id).values(item_id=new_item.item_id, title=new_item.title,
                                                                    slug=new_item.slug,
                                                                    description=new_item.description, price=new_item.price)
    await db.execute(query)
    return {**new_item.model_dump(), "id": item_id}


@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    query = items.delete().where(items.c.item_id == item_id)
    await db.execute(query)
    return {'message': 'Item deleted'}


@app.get("/orders/")
async def read_orders():
    query = orders.select()
    return await db.fetch_all(query)


@app.get("/orders/{order_id}", response_model=Orders)
async def read_order(order_id: int):
    query = orders.select().where(orders.c.order_id == order_id)
    return await db.fetch_one(query)


@app.post("/orders/", response_model=Orders)
async def create_order(order: Orders):
    query = orders.insert().values(order_id=order.order_id, user_id=order.user_id, item_id=order.item_id,
                                   order_date=order.order_date, status=order.status)
    last_record_id = await db.execute(query)
    return {**order.model_dump(), "id": last_record_id}


@app.put("/orders/{order_id}", response_model=Orders)
async def update_order(order_id: int, new_order: Orders):
    query = orders.update().where(orders.c.order_id == order_id).values(order_id=new_order.order_id,
                                                                        user_id=new_order.user_id,
                                                                        item_id=new_order.item_id,
                                                                        order_date=new_order.order_date,
                                                                        status=new_order.status)
    await db.execute(query)
    return {**new_order.model_dump(), "id": order_id}


@app.delete("/orders/{order_id}")
async def delete_order(order_id: int):
    query = orders.delete().where(orders.c.order_id == order_id)
    await db.execute(query)
    return {'message': 'Order deleted'}