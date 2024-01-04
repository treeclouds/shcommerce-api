import factory
from factory import fuzzy
from app.products.models import ProductModel
from app.users.models import UserModel

class UserFactory(factory.Factory):
    class Meta:
        model = UserModel

    id = factory.Faker('uuid4')
    username = factory.Faker('user_name')
    email = factory.Faker('email')

class ProductFactory(factory.Factory):
    class Meta:
        model = ProductModel

    id = factory.Sequence(lambda n: n)
    image = factory.Faker('image_url')
    category = fuzzy.FuzzyChoice(["Electronics", "Books", "Clothing", "Home"])
    title = factory.Faker('sentence', nb_words=4)
    description = factory.Faker('text')
    condition = fuzzy.FuzzyChoice([choice.value for choice in ProductModel.condition.type_])
    price = fuzzy.FuzzyDecimal(10.0, 100.0)
    dimensions_width = fuzzy.FuzzyFloat(1.0, 5.0)
    dimensions_height = fuzzy.FuzzyFloat(1.0, 5.0)
    dimensions_length = fuzzy.FuzzyFloat(1.0, 5.0)
    dimensions_weight = fuzzy.FuzzyFloat(1.0, 5.0)
    brand = factory.Faker('company')
    material = factory.Faker('word')
    stock = fuzzy.FuzzyInteger(1, 100)
    sku = factory.Faker('ean')
    tags = factory.LazyFunction(lambda: ["tag1", "tag2"])
    seller = factory.SubFactory(UserFactory)
