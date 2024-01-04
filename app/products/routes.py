from typing import List
from fastapi import APIRouter, Depends, HTTPException
from app.users.models import User
from app.products.models import ProductModel, Product_Pydantic, ProductIn_Pydantic
from app.core.auth import current_user

router = APIRouter(
        tags=["Products"],
        responses={404: {"description": "Not found"}}
    )

@router.post("/products/", response_model=Product_Pydantic)
async def create_product(product: ProductIn_Pydantic, current_user: User = Depends(current_user)):
    product_obj = await ProductModel.create(**product.dict(), seller=current_user)
    return await Product_Pydantic.from_tortoise_orm(product_obj)

@router.get("/products/", response_model=List[Product_Pydantic])
async def read_products():
    return await Product_Pydantic.from_queryset(ProductModel.all())

@router.get("/products/{product_id}", response_model=Product_Pydantic)
async def read_product(product_id: int):
    return await Product_Pydantic.from_queryset_single(ProductModel.get(id=product_id))

@router.put("/products/{product_id}", response_model=Product_Pydantic)
async def update_product(product_id: int, product: ProductIn_Pydantic, current_user: User = Depends(current_user)):
    existing_product = await ProductModel.get(id=product_id)
    if not existing_product or existing_product.seller.id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this product")
    await existing_product.update_from_dict(product.dict(exclude_unset=True)).save()
    return await Product_Pydantic.from_tortoise_orm(existing_product)

@router.delete("/products/{product_id}", response_model=Product_Pydantic)
async def delete_product(product_id: int, current_user: User = Depends(current_user)):
    product = await ProductModel.get(id=product_id)
    if not product or product.seller.id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this product")
    await product.delete()
    return {"message": "Product deleted successfully"}
