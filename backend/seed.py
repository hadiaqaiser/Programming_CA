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

        # --- shades (3 for each product, same idea as my CA1 mockShades) ---
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

        # helper to find shade by code quickly
        code_to_shade = {s.shade_code: s for s in shades}

        # --- batches (at least one per shade, special one for MED-LIP-21-2307) ---
        batches = [
            models.Batch(
                shade_id=code_to_shade["21"].id,
                batch_code="MED-LIP-21-2307",
                mfg_date="2023-07-22",
                expiry_date="2026-07-22",
                status="Passed",
            ),
            models.Batch(
                shade_id=code_to_shade["22"].id,
                batch_code="MED-LIP-22-2308",
                mfg_date="2023-08-10",
                expiry_date="2026-08-10",
                status="Passed",
            ),
            models.Batch(
                shade_id=code_to_shade["23"].id,
                batch_code="MED-LIP-23-2310",
                mfg_date="2023-10-01",
                expiry_date="2026-10-01",
                status="Passed",
            ),
            models.Batch(
                shade_id=code_to_shade["11"].id,
                batch_code="MED-FDT-11-2307",
                mfg_date="2023-07-05",
                expiry_date="2026-07-05",
                status="Passed",
            ),
            models.Batch(
                shade_id=code_to_shade["14"].id,
                batch_code="MED-FDT-14-2311",
                mfg_date="2023-11-02",
                expiry_date="2026-11-02",
                status="Passed",
            ),
            models.Batch(
                shade_id=code_to_shade["16"].id,
                batch_code="MED-FDT-16-2203",
                mfg_date="2022-03-15",
                expiry_date="2025-03-15",
                status="Expired",
            ),
        ]
        session.add_all(batches)

        session.commit()
        print("MedoraCare seed: database filled with sample products, shades, batches.")
    except Exception as e:
        session.rollback()
        print("MedoraCare seed failed:", e)
        raise
    finally:
        session.close()
