from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

products = [
    {"id": 1, "code": "SP001", "name": "Keyboard", "price": 500000, "stock": 10},
    {"id": 2, "code": "SP002", "name": "Mouse", "price": 300000, "stock": 5}
]


class ProductUpdate(BaseModel):
    code: str
    name: str = Field(..., min_length=1)
    price: float = Field(..., gt=0)
    stock: int = Field(..., ge=0)


@app.put("/products/{product_id}")
def update_product(product_id: int, product_update: ProductUpdate):
    selected_product = None

    for product in products:
        if product["id"] == product_id:
            selected_product = product
            break

    if selected_product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    for product in products:
        if product["code"] == product_update.code and product["id"] != product_id:
            raise HTTPException(
                status_code=400,
                detail="Product code already exists"
            )

    selected_product["code"] = product_update.code
    selected_product["name"] = product_update.name
    selected_product["price"] = product_update.price
    selected_product["stock"] = product_update.stock

    return {
        "message": "Update product successfully",
        "data": selected_product
    }