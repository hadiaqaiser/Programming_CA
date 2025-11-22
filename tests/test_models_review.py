# test that review model has right table name and important fields exist
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.models import Review


def test_review_tablename_and_fields():
    assert Review.__tablename__ == "reviews"

    for attr in ["id", "shade_id", "email", "rating", "comment"]:
        assert hasattr(Review, attr)