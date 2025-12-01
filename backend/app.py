# main flask api file for medoracare. here i wire cors, db and all endpoints
# ref: https://flask.palletsprojects.com/en/3.0.x/quickstart/

from flask import Flask, jsonify, request
from flask_cors import CORS

# import my shared db things (engine + Base) and models so tables can be created once
from .db import engine, Base, get_session
from . import models

# creating all tables in medora.db if not exist yet (products, shades, batches, wishlist_items, reviews)
# ref: Base.metadata.create_all usage from SQLAlchemy docs https://docs.sqlalchemy.org/en/20/core/metadata.html#create-all-database-objects and chatgpt
Base.metadata.create_all(bind=engine)

# create main flask application
app = Flask(__name__)
CORS(app)

# shade search endpoint. frontend calls this with category/color/finish filters
# ref: https://flask.palletsprojects.com/en/3.0.x/quickstart/#accessing-request-data


@app.get("/api/shades")
def list_shades():
    # read query params from url, e.g. ?category=foundation&color_family=Light
    category = request.args.get("category")
    color_family = request.args.get("color_family")
    finish = request.args.get("finish")

    session = get_session()
    try:
        # build base query joining shades with products so i can send product_name out
        q = (
            session
            .query(models.Shade, models.Product)
            .join(models.Product, models.Shade.product_id == models.Product.id)
        )

        # optional filters (only apply if user picked something)
        if category:
            q = q.filter(models.Product.category == category)
        if color_family:
            q = q.filter(models.Shade.color_family == color_family)
        if finish:
            q = q.filter(models.Shade.finish == finish)

        rows = q.all()

        result = []
        for shade, product in rows:
            result.append(
                {
                    "id": shade.id,
                    "product_id": shade.product_id,
                    "product_name": product.name,
                    "shade_name": shade.shade_name,
                    "shade_code": shade.shade_code,
                    "finish": shade.finish,
                    "color_family": shade.color_family,
                    "msrp": shade.msrp,
                }
            )

        return jsonify(result)
    finally:
        session.close()


# this only runs if i do: python app.py (optional)
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001)
