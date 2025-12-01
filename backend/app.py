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

Base.metadata.create_all(bind=engine)

# simple test endpoint to see if backend running


@app.get("/api/ping")
def ping():
    return jsonify({"message": "medoracare api ok"})


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

# batch check endpoint. frontend sends batch_code and i search batches table
# ref: https://docs.sqlalchemy.org/en/20/orm/queryguide/select.html#selecting-orm-entities


@app.get("/api/auth/check")
def check_batch():
    code = request.args.get("batch_code", "").strip()

    if not code:
        # bad request if user didnt send anything
        return jsonify({"authentic": False, "error": "batch_code missing"}), 400

    session = get_session()
    try:
        batch = (
            session.query(models.Batch)
            .filter(models.Batch.batch_code == code)
            .first()
        )

        # if no batch found → mark as not authentic
        if batch is None:
            return jsonify({"authentic": False}), 200

        shade = session.query(models.Shade).get(batch.shade_id)
        product = (
            session.query(models.Product).get(
                shade.product_id) if shade else None
        )

        # shape of response matches what my frontend app.js expects
        return jsonify(
            {
                "authentic": True,
                "status": batch.status,
                "product_name": product.name if product else None,
                "batch_info": {
                    "id": batch.id,
                    "shade_id": batch.shade_id,
                    "batch_code": batch.batch_code,
                    "mfg_date": batch.mfg_date,
                    "expiry_date": batch.expiry_date,
                    "status": batch.status,
                },
                "shade_info": {
                    "id": shade.id if shade else None,
                    "product_id": shade.product_id if shade else None,
                    "product_name": product.name if product else None,
                    "shade_code": shade.shade_code if shade else None,
                    "shade_name": shade.shade_name if shade else None,
                    "finish": shade.finish if shade else None,
                    "color_family": shade.color_family if shade else None,
                    "msrp": shade.msrp if shade else None,
                },
            }
        )
    finally:
        session.close()

# small api to list all wishlist rows so later my frontend can show them from real db
# source: used basic sqlalchemy query pattern from https://docs.sqlalchemy.org/en/20/orm/quickstart.html#simple-select


@app.get("/api/wishlist")
def get_wishlist():
    session = get_session()
    try:
        # join wishlist with shades so i can show shade_code + name
        rows = (
            session
            .query(models.WishlistItem, models.Shade)
            .join(models.Shade, models.WishlistItem.shade_id == models.Shade.id)
            .all()
        )

        result = []
        for item, shade in rows:
            result.append(
                {
                    "id": item.id,
                    "email": item.email,
                    "note": item.note,
                    "shade_id": item.shade_id,
                    "shade_code": shade.shade_code,
                    "shade_name": shade.shade_name,
                }
            )
        return jsonify(result)
    finally:
        session.close()

# this api takes email + shade_id + note from frontend and creates a new wishlist row
# source: followed flask json pattern from https://flask.palletsprojects.com/en/3.0.x/api/#flask.Request.get_json


@app.post("/api/wishlist")
def create_wishlist_item():
    data = request.get_json(silent=True) or {}

    email = (data.get("email") or "").strip()
    shade_id = data.get("shade_id")
    note = (data.get("note") or "").strip()

    # tiny validation so db does not get junk
    if not email or not shade_id:
        return jsonify({"error": "email and shade_id are required"}), 400

    session = get_session()
    try:
        # make sure shade exists before saving
        shade = session.query(models.Shade).get(shade_id)
        if shade is None:
            return jsonify({"error": "shade not found"}), 404

        item = models.WishlistItem(
            email=email,
            shade_id=shade_id,
            note=note or None,
        )
        session.add(item)
        session.commit()

        return jsonify(
            {
                "id": item.id,
                "email": item.email,
                "shade_id": item.shade_id,
                "note": item.note,
            }
        ), 201
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


# explanation: this endpoint returns all reviews filtered by shade_id so frontend can show feedback for each shade
# source: used SQLAlchemy basic filter pattern from docs https://docs.sqlalchemy.org/en/20/orm/queryguide/select.html
# commit msg: add GET api for listing reviews by shade_id

@app.get("/api/reviews")
def list_reviews():
    shade_id = request.args.get("shade_id")
    session = get_session()
    try:
        q = session.query(models.Review)

        if shade_id:
            q = q.filter(models.Review.shade_id == int(shade_id))

        rows = q.all()
        return jsonify([
            {
                "id": r.id,
                "shade_id": r.shade_id,
                "email": r.email,
                "rating": r.rating,
                "comment": r.comment,
            }
            for r in rows
        ])
    finally:
        session.close()


# this endpoint allows frontend to POST a new review so users can give rating and feedback for any shade
# source: used Flask request.json pattern from docs https://flask.palletsprojects.com/en/3.0.x/quickstart/#json

@app.post("/api/reviews")
def create_review():
    data = request.json or {}
    email = data.get("email")
    shade_id = data.get("shade_id")
    rating = data.get("rating")
    comment = data.get("comment", "")

    # simple validation
    if not email or not shade_id or not rating:
        return jsonify({"error": "missing fields"}), 400

    session = get_session()
    try:
        new_review = models.Review(
            email=email,
            shade_id=int(shade_id),
            rating=int(rating),
            comment=comment
        )

        session.add(new_review)
        session.commit()

        return jsonify({
            "id": new_review.id,
            "email": new_review.email,
            "shade_id": new_review.shade_id,
            "rating": new_review.rating,
            "comment": new_review.comment
        }), 201
    finally:
        session.close()


# this only runs if i do: python app.py (optional)
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001)
