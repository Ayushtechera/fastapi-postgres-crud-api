
from fastapi import FastAPI,Depends
from fastapi.middleware.cors import CORSMiddleware
from models import Product
from database import session
import database_models
from sqlalchemy.orm import Session

from database import session,engine

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"]
)

database_models.Base.metadata.create_all(bind=engine)

@app.get("/")
def greet():
    return "Welcome New Yorker"

products = [
    Product(id=1,name="phone",description="Budget phone",price=99, quantity=10),
    Product(id=2,name="laptop",description="Budget laptop",price=999, quantity=15),
    Product(id=3,name="tablet",description="Budget tablet",price=997, quantity=18),
    Product(id=4,name="Playstation",description="Budget Playstation",price=994, quantity=1)
]


def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()


def init_db():
    db = session()
    count = db.query(database_models.Product).count()
    if count == 0:
        for product in products:
            '''
            model_dump will return the list but we want the key value pairs.
            So, to convert dictionary to key value we do unpacking byt using (**)
            (product.model_dump) -> this will return the dictionary
            (**product.model_dump) -> this will return the key-value
            '''
            db.add(database_models.Product(**product.model_dump()))
        db.commit()

init_db()


@app.get("/products")
def get_all_products(db:Session = Depends(get_db)):
    db_products = db.query(database_models.Product).all()
    return db_products

@app.get("/products/{id}")
def get_product_by_id(id:int, db:Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        return db_product
    return "Product not found"


@app.post("/products")
def add_product(product:Product,db:Session = Depends(get_db)):
    db.add(database_models.Product(**product.model_dump()))
    db.commit()
    return product

@app.put("/products")
def update_product(id:int, product:Product,db:Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        db_product.name = product.name
        db_product.description = product.description
        db_product.price = product.price
        db_product.quantity = product.quantity
        db.commit()

        return "Product Added Successfully"
    else:
        return "No product found"


@app.delete("/products")
def delete_product(id: int,db:Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return "Product Deleted"
    else:
        return "Product not found"
            
    
            