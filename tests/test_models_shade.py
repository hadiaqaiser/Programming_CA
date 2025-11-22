# test that shade model basic metadata is correct (table name and fields)
# source: i used chatgpt for this style of hasattr checks instead of real db query

import sys, os
# fix path so python can see backend package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.models import Shade


def test_shade_tablename_and_fields():
    # table name should match my __tablename__
    assert Shade.__tablename__ == "shades"

    # check important attributes exist
    for attr in ["id", "product_id", "shade_code", "shade_name", "finish", "color_family", "msrp"]:
        assert hasattr(Shade, attr)