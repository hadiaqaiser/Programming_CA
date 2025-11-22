# extend imports so i can define more fields (like foreign key and price) for shade table
from sqlalchemy import Column, Integer, String, ForeignKey
from backend.db import Base

# create product table model with id name and category for medora products
# source: i asked chatgpt for the column types + __tablename__ pattern, rest idea is mine
class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    category = Column(String(50), nullable=False)

    def __repr__(self) -> str:
        # small helper so if i print(product) it look nice
        return f"<Product id={self.id} name={self.name!r} category={self.category!r}>"
    
