from typing import List
from fastapi import APIRouter, Depends, HTTPException
from app.users.models import User
from app.products.models import ProductModel
from app.products.schemas import ProductSchema  # Assuming this is the updated schema
from app.core.auth import current_user

router = APIRouter(
    tags=["Products"],
    responses={404: {"description": "Not found"}}
)


@router.post("/products/", response_model=ProductSchema)
async def create_product(product: ProductSchema, current_user: User = Depends(current_user)):
    product_dict = product.dict()
    product_dict["seller"] = current_user
    print("#######")
    print(product_dict)
    product_obj = await ProductModel.create(**product_dict)
    return ProductSchema.from_orm(product_obj)

@router.get("/products/", response_model=List[ProductSchema])
async def read_products():
    product_objs = await ProductModel.all().prefetch_related("seller")
    return [ProductSchema.from_orm(product) for product in product_objs]


@router.get("/products/{product_id}", response_model=ProductSchema)
async def read_product(product_id: int):
    product_obj = await ProductModel.get(id=product_id)
    if not product_obj:
        raise HTTPException(status_code=404, detail="Product not found")
    return ProductSchema.from_orm(product_obj)

@router.put("/products/{product_id}", response_model=ProductSchema)
async def update_product(product_id: int, product_data: ProductSchema, current_user: User = Depends(current_user)):
    existing_product = await ProductModel.get(id=product_id)
    if not existing_product:
        raise HTTPException(status_code=404, detail="Product not found")
    if existing_product.seller.id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this product")
    
    product_update_dict = product_data.dict(exclude_unset=True)
    product_update_dict.pop("seller_id", None)  # Exclude seller_id from update
    
    await existing_product.update_from_dict(product_update_dict).save()
    return ProductSchema.from_orm(existing_product)

@router.delete("/products/{product_id}", response_model=ProductSchema)
async def delete_product(product_id: int, current_user: User = Depends(current_user)):
    product = await ProductModel.get(id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if product.seller.id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this product")
    
    await product.delete()
    return {"message": "Product deleted successfully"}
