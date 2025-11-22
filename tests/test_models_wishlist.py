# test that wishlist model has correct table name and main fields
# source: i used chatgpt pattern for using hasattr loop instead of querying real db

import sys, os
# fix path so test can import backend package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.models import WishlistItem


def test_wishlist_tablename_and_fields():
    assert WishlistItem.__tablename__ == "wishlist_items"

    for attr in ["id", "shade_id", "email", "note"]:
        assert hasattr(WishlistItem, attr)