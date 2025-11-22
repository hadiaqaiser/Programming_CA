# what: test that batch model basic metadata and fields look correct
import sys, os
# fix path so python can find backend package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.models import Batch


def test_batch_tablename_and_fields():
    # table name should match __tablename__
    assert Batch.__tablename__ == "batches"

    # check all important attributes exist on class
    for attr in ["id", "shade_id", "batch_code", "mfg_date", "expiry_date", "status"]:
        assert hasattr(Batch, attr)