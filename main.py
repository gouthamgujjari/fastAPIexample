from fastapi import FastAPI
from database import SessionLocal, engine, Base
from models import ProductDB
from schemas import ProductBase

app = FastAPI()

Base.metadata.create_all(bind=engine)

#post
@app.post("/products/")
def create_product(product: ProductBase):
    db = SessionLocal()

    new_product = ProductDB(**product.dict())

    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    db.close()

    return "Product created successfully",

#get
@app.get("/products/")
def get_products():
    db = SessionLocal()
    products = db.query(ProductDB).all()
    db.close()
    return products


#put

@app.put("/products/{product_id}")
def update_product(product_id: int, product_data: ProductBase):
    db = SessionLocal()
    product = db.query(ProductDB).filter(ProductDB.id == product_id).first()

    if product:
        for key, value in product_data.dict().items():
            setattr(product, key, value)

        db.commit()
        db.refresh(product)
        db.close()

        return "Product updated successfully",
            
        
    else:
        db.close()
        return "Product not found"


#delete
@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    db = SessionLocal()
    product = db.query(ProductDB).filter(ProductDB.id == product_id).first()

    if product:
        db.delete(product)
        db.commit()
        db.close()
        return "Product deleted successfully"
    else:
        db.close()
        return "Product not found"
