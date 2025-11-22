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
    
# create shade table model linked to product using product_id and store basic shade info
class Shade(Base):
    __tablename__ = "shades"

    id = Column(Integer, primary_key=True, index=True)
    # link to product (1 product can have many shades)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)

    shade_code = Column(String(10), nullable=False)
    shade_name = Column(String(50), nullable=False)
    finish = Column(String(20), nullable=False)        # Matte / Glowy
    color_family = Column(String(20), nullable=False)  # Light / Medium / Dark / Red / Pink / Brown
    msrp = Column(Integer, nullable=False)             # simple int price for now

    def __repr__(self) -> str:
        return f"<Shade id={self.id} code={self.shade_code!r} name={self.shade_name!r}>"