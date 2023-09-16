import sqlalchemy
from datetime import datetime
from sqlalchemy import create_engine, ForeignKey
from pydantic import BaseModel, Field
import databases

DATABASE_URL = 'sqlite:///mydatabase.db'
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
db = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()
default_date = datetime.now


class Users(BaseModel):
    user_id: int
    last_name: str = Field(title="Фамилия", min_length=2, max_length=20)
    first_name: str = Field(title="Имя", min_length=2, max_length=20)
    email: str = Field(title="Электронная почта", max_length=128)
    password: str = Field(title="Пароль", max_length=128)


class Items(BaseModel):
    item_id: int
    title: str = Field(title="Назавание", min_length=2, max_length=50)
    slug: str = Field(slug="URL", min_length=2, max_length=50)
    description: str = Field(title="Описание", max_length=256)
    price: float = Field(title="Цена", default=0)


class Orders(BaseModel):
    order_id: int
    user_id: int
    item_id: int
    order_date: str = Field(title="Дата заказа")
    status: bool


users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("user_id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("last_name", sqlalchemy.String(20)),
    sqlalchemy.Column("first_name", sqlalchemy.String(20)),
    sqlalchemy.Column("email", sqlalchemy.String(128)),
    sqlalchemy.Column("password", sqlalchemy.String(128)),
)

items = sqlalchemy.Table(
    "items",
    metadata,
    sqlalchemy.Column("item_id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("title", sqlalchemy.String(50)),
    sqlalchemy.Column("slug", sqlalchemy.String(50)),
    sqlalchemy.Column("description", sqlalchemy.String(256)),
    sqlalchemy.Column("price", sqlalchemy.Integer),
)

orders = sqlalchemy.Table(
    "orders",
    metadata,
    sqlalchemy.Column("order_id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("user_id", sqlalchemy.Integer, ForeignKey('users.user_id')),
    sqlalchemy.Column("item_id", sqlalchemy.Integer, ForeignKey('items.item_id')),
    sqlalchemy.Column("order_date", sqlalchemy.String(128), default=default_date),
    sqlalchemy.Column("status", sqlalchemy.Boolean),
)