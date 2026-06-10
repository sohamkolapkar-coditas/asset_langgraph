"""
Seed script: 2 users, each assigned a laptop and a monitor.
Idempotent — safe to run on every deployment; skips records that already exist.
"""

import uuid
import datetime
from app.models.session import SessionLocal
from app.models.user import User
from app.models.asset_categories import AssetCategory
from app.models.asset_item import AssetItem
from app.utils.constants.asset_item import AssetItemStatus, AssetItemLocation

# ---------------------------------------------------------------------------
# USER DETAILS
# ---------------------------------------------------------------------------

USER_1_EMAIL = "lala.kolapkar@coditas.com"
USER_2_EMAIL = "aman.kadam@coditas.com"

# ---------------------------------------------------------------------------

NOW = datetime.datetime.now()


def _get_or_create_user(db, email):
    user = db.query(User).filter(User.email == email).first()
    if user:
        return user, False
    user = User(id=uuid.uuid4(), email=email, is_active=True, created_at=NOW)
    db.add(user)
    db.flush()
    return user, True


def _get_or_create_category(db, name, quantity):
    cat = db.query(AssetCategory).filter(AssetCategory.name == name).first()
    if cat:
        return cat, False
    cat = AssetCategory(id=uuid.uuid4(), name=name, quantity=quantity, is_active=True, created_at=NOW)
    db.add(cat)
    db.flush()
    return cat, True


def _get_or_create_item(db, asset_code, **kwargs):
    item = db.query(AssetItem).filter(AssetItem.asset_code == asset_code).first()
    if item:
        return item, False
    item = AssetItem(id=uuid.uuid4(), asset_code=asset_code, is_active=True, created_at=NOW, **kwargs)
    db.add(item)
    db.flush()
    return item, True


def seed():
    db = SessionLocal()
    try:
        user1, u1_new = _get_or_create_user(db, USER_1_EMAIL)
        user2, u2_new = _get_or_create_user(db, USER_2_EMAIL)

        laptop_cat, _ = _get_or_create_category(db, "Laptop", 2)
        monitor_cat, _ = _get_or_create_category(db, "Monitor", 2)

        _get_or_create_item(
            db, "LAP-001",
            name="Dell XPS 15 Laptop",
            asset_category_id=laptop_cat.id,
            user_id=user1.id,
            status=AssetItemStatus.ALLOCATED.value,
            location=AssetItemLocation.NYATI.value,
        )
        _get_or_create_item(
            db, "MON-001",
            name='Dell UltraSharp 27" Monitor',
            asset_category_id=monitor_cat.id,
            user_id=user1.id,
            status=AssetItemStatus.ALLOCATED.value,
            location=AssetItemLocation.NYATI.value,
        )
        _get_or_create_item(
            db, "LAP-002",
            name='Apple MacBook Pro 14"',
            asset_category_id=laptop_cat.id,
            user_id=user2.id,
            status=AssetItemStatus.ALLOCATED.value,
            location=AssetItemLocation.GAIA.value,
        )
        _get_or_create_item(
            db, "MON-002",
            name='LG 27" 4K Monitor',
            asset_category_id=monitor_cat.id,
            user_id=user2.id,
            status=AssetItemStatus.ALLOCATED.value,
            location=AssetItemLocation.GAIA.value,
        )

        db.commit()
        print("Seed complete (skipped existing records).")
        print(f"  {'Created' if u1_new else 'Exists '} User 1: {USER_1_EMAIL}  → LAP-001, MON-001")
        print(f"  {'Created' if u2_new else 'Exists '} User 2: {USER_2_EMAIL}  → LAP-002, MON-002")

    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


if __name__ == "__main__":
    seed()
