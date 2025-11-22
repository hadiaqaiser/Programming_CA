# fix python path so this test can see backend package
# source: i used chatgpt for this sys.path line bcz i dont remember the join logic

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# test that product model is wired correctly (tablename + fields)
from backend.models import Product

def test_product_tablename_and_fields():
    # check table name is correct
    assert Product.__tablename__ == "products"

    # check main columns exist on the model class
    assert hasattr(Product, "id")
    assert hasattr(Product, "name")
    assert hasattr(Product, "category")