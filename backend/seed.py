# small helper script to create tables and insert sample medora data
# ref: https://docs.sqlalchemy.org/en/20/orm/session_basics.html#adding-and-updating-objects

from .db import engine, Base, get_session
from . import models


def seed():
    # make sure tables exist (safe to call again)
    Base.metadata.create_all(bind=engine)

    session = get_session()
    try:
        # if products already there, i dont want to duplicate them
        if session.query(models.Product).count() > 0:
            print("MedoraCare seed: products already exist, skip seeding.")
            return

        # --- products ---
        foundation = models.Product(
            name="Medora Foundation",
            category="foundation",
        )
        lipstick = models.Product(
            name="Medora Lipstick",
            category="lipstick",
        )
        session.add_all([foundation, lipstick])
        session.flush()  # get ids before creating shades

        # --- shades (3 for each product) ---
        shades = [
            # lipstick shades
            models.Shade(
                product_id=lipstick.id,
                shade_code="21",
                shade_name="Cherry",
                finish="Matte",
                color_family="Red",
                msrp=450,
            ),
            models.Shade(
                product_id=lipstick.id,
                shade_code="22",
                shade_name="Rose",
                finish="Glowy",
                color_family="Pink",
                msrp=450,
            ),
            models.Shade(
                product_id=lipstick.id,
                shade_code="23",
                shade_name="Rust",
                finish="Matte",
                color_family="Brown",
                msrp=450,
            ),
            # foundation shades
            models.Shade(
                product_id=foundation.id,
                shade_code="11",
                shade_name="Ivory",
                finish="Matte",
                color_family="Light",
                msrp=1200,
            ),
            models.Shade(
                product_id=foundation.id,
                shade_code="14",
                shade_name="Honey",
                finish="Glowy",
                color_family="Medium",
                msrp=1200,
            ),
            models.Shade(
                product_id=foundation.id,
                shade_code="16",
                shade_name="Cocoa",
                finish="Glowy",
                color_family="Dark",
                msrp=1200,
            ),
        ]
        session.add_all(shades)
        session.flush()

        # adds seed data for wishlist + reviews tables
        # reference: i followed SQLAlchemy "add objects" example (https://docs.sqlalchemy.org/en/20/orm/session_basics.html#adding-and-updating-objects)

        # --- wishlist demo entries ---
        wishlist = [
            models.WishlistItem(
                shade_id=code_to_shade["21"].id,
                email="test1@example.com",
                note="for eid look",
            ),
            models.WishlistItem(
                shade_id=code_to_shade["11"].id,
                email="test2@example.com",
                note="my daily shade",
            ),
        ]
        session.add_all(wishlist)

        # --- review demo entries ---
        reviews = [
            models.Review(
                shade_id=code_to_shade["21"].id,
                email="reviewer1@example.com",
                rating=5,
                comment="very smooth and nice texture!",
            ),
            models.Review(
                shade_id=code_to_shade["14"].id,
                email="reviewer2@example.com",
                rating=4,
                comment="good match for warm skin tone",
            ),
        ]
        session.add_all(reviews)

        session.commit()
        print("MedoraCare seed: database filled with sample products, shades, batches.")
    except Exception as e:
        session.rollback()
        print("MedoraCare seed failed:", e)
        raise
    finally:
        session.close()


# This allow me to run seeding easily with `python -m backend.seed`
# ref: https://docs.python.org/3/library/__main__.html
if __name__ == "__main__":
    seed()
