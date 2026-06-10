"""
Seed script: 2 users, each assigned a laptop and a monitor.
Each record is checked before insert — existing records are skipped.

Run with:
    python -m app.seed.seed_dummy_users
"""

import uuid
import datetime
from app.models.session import SessionLocal
from app.models.user import User
from app.models.asset_categories import AssetCategory
from app.models.asset_item import AssetItem
from app.utils.constants.asset_item import AssetItemStatus, AssetItemLocation

USER_1_EMAIL = "soham.kolapkar@coditas.com"
USER_2_EMAIL = "aman.kadam@coditas.com"

NOW = datetime.datetime.now()


def seed():
    db = SessionLocal()
    try:
        # ---- Users ----
        user1 = db.query(User).filter(User.email == USER_1_EMAIL).first()
        if not user1:
            user1 = User(id=uuid.uuid4(), email=USER_1_EMAIL, is_active=True, created_at=NOW)
            db.add(user1)
            db.flush()
            print(f"  Created user: {USER_1_EMAIL}")
        else:
            print(f"  Skipped user (exists): {USER_1_EMAIL}")

        user2 = db.query(User).filter(User.email == USER_2_EMAIL).first()
        if not user2:
            user2 = User(id=uuid.uuid4(), email=USER_2_EMAIL, is_active=True, created_at=NOW)
            db.add(user2)
            db.flush()
            print(f"  Created user: {USER_2_EMAIL}")
        else:
            print(f"  Skipped user (exists): {USER_2_EMAIL}")

        # ---- Asset Categories ----
        laptop_cat = db.query(AssetCategory).filter(AssetCategory.name == "laptop").first()
        if not laptop_cat:
            laptop_cat = AssetCategory(id=uuid.uuid4(), name="laptop", quantity=2, is_active=True, created_at=NOW)
            db.add(laptop_cat)
            db.flush()
            print("  Created category: laptop")
        else:
            print("  Skipped category (exists): laptop")

        monitor_cat = db.query(AssetCategory).filter(AssetCategory.name == "monitor").first()
        if not monitor_cat:
            monitor_cat = AssetCategory(id=uuid.uuid4(), name="monitor", quantity=2, is_active=True, created_at=NOW)
            db.add(monitor_cat)
            db.flush()
            print("  Created category: monitor")
        else:
            print("  Skipped category (exists): monitor")

        # ---- Asset Items ----
        asset_definitions = [
            ("LAP-001", "Dell XPS 15 Laptop",           laptop_cat,  user1, AssetItemLocation.NYATI),
            ("MON-001", 'Dell UltraSharp 27" Monitor',   monitor_cat, user1, AssetItemLocation.NYATI),
            ("LAP-002", 'Apple MacBook Pro 14"',         laptop_cat,  user2, AssetItemLocation.GAIA),
            ("MON-002", 'LG 27" 4K Monitor',             monitor_cat, user2, AssetItemLocation.GAIA),
        ]

        for asset_code, name, category, user, location in asset_definitions:
            existing = db.query(AssetItem).filter(AssetItem.asset_code == asset_code).first()
            if not existing:
                db.add(AssetItem(
                    id=uuid.uuid4(),
                    asset_code=asset_code,
                    name=name,
                    asset_category_id=category.id,
                    user_id=user.id,
                    status=AssetItemStatus.ALLOCATED.value,
                    location=location.value,
                    is_active=True,
                    created_at=NOW,
                ))
                print(f"  Created asset: {asset_code} — {name}")
            else:
                print(f"  Skipped asset (exists): {asset_code}")

        db.commit()
        print("Seed complete.")

    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


if __name__ == "__main__":
    seed()
