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
    

# create batch table model to store batch code mfg expiry and quality status for each shade
# source: i used chatgpt for choosing string length and nullable flags but idea comes from my project design

class Batch(Base):
    __tablename__ = "batches"

    id = Column(Integer, primary_key=True, index=True)
    # each batch belongs to one shade
    shade_id = Column(Integer, ForeignKey("shades.id"), nullable=False)

    batch_code = Column(String(50), nullable=False)
    mfg_date = Column(String(10), nullable=False)      # e.g. "2023-07-05"
    expiry_date = Column(String(10), nullable=False)   # e.g. "2026-07-05"
    status = Column(String(20), nullable=False)        # e.g. "Passed", "Failed", "Expired"

    def __repr__(self) -> str:
        return f"<Batch id={self.id} code={self.batch_code!r} status={self.status!r}>"
    
# create wishlist table so user can save shades they like with email and note

class WishlistItem(Base):
    __tablename__ = "wishlist_items"

    id = Column(Integer, primary_key=True, index=True)
    # which shade user liked
    shade_id = Column(Integer, ForeignKey("shades.id"), nullable=False)

    # who saved it (no auth, just email text for now)
    email = Column(String(120), nullable=False)
    # small note like "for eid look"
    note = Column(String(255), nullable=True)

    def __repr__(self) -> str:
        return f"<WishlistItem id={self.id} shade_id={self.shade_id} email={self.email!r}>"