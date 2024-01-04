import pytest
from httpx import AsyncClient
from main import app  # Import your FastAPI app
from factories import UserFactory, ProductFactory

@pytest.mark.asyncio
async def test_create_product():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        user = UserFactory()  # Create a test user
        product_data = ProductFactory.build()  # Build product data without saving to DB
        response = await ac.post("/products/", json=product_data.dict())
    assert response.status_code == 200
    assert response.json()['title'] == product_data.title

@pytest.mark.asyncio
async def test_read_products():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/products/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_update_product():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Assume product_id is the ID of an existing product
        product_id = 1
        updated_data = {"title": "Updated Product Title"}
        response = await ac.put(f"/products/{product_id}", json=updated_data)
    assert response.status_code == 200
    assert response.json()['title'] == updated_data['title']

@pytest.mark.asyncio
async def test_delete_product():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Assume product_id is the ID of an existing product
        product_id = 1
        response = await ac.delete(f"/products/{product_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Product deleted successfully"}
