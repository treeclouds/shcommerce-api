from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator
from app.products.schemas import ProductCondition

class ProductModel(models.Model):
    id = fields.IntField(pk=True)
    images = fields.JSONField()
    category = fields.CharField(max_length=100)
    title = fields.CharField(max_length=255)
    description = fields.TextField()
    condition = fields.CharEnumField(ProductCondition)
    price = fields.DecimalField(max_digits=10, decimal_places=2)
    dimensions_width = fields.FloatField()
    dimensions_height = fields.FloatField()
    dimensions_length = fields.FloatField()
    dimensions_weight = fields.FloatField()
    brand = fields.CharField(max_length=100, null=True)
    material = fields.CharField(max_length=100, null=True)
    stock = fields.IntField()
    sku = fields.CharField(max_length=100)
    tags = fields.JSONField()  # Storing tags as a JSON list
    seller = fields.ForeignKeyField('models.User', related_name='products')

    class Meta:
        table = "products"

# Pydantic model creator for ProductModel
Product_Pydantic = pydantic_model_creator(ProductModel)
ProductIn_Pydantic = pydantic_model_creator(ProductModel, exclude_readonly=True)