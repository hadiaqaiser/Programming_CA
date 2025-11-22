# test that product model is wired correctly (tablename + fields)
from backend.models import Product

def test_product_tablename_and_fields():
    # check table name is correct
    assert Product.__tablename__ == "products"

    # check main columns exist on the model class
    assert hasattr(Product, "id")
    assert hasattr(Product, "name")
    assert hasattr(Product, "category")