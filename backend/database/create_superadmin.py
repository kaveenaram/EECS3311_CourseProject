from database.db import SessionLocal, init_db
from entities.admin import Admin
from entities.system_policy import SystemPolicy
from patterns.observer.notification_service import NotificationService

def create_superadmin():
    init_db()
    db = SessionLocal()

    try:
        superadmin_email = "superadmin@example.com"
        existing = db.query(Admin).filter(Admin.email == superadmin_email).first()

        if existing:
            print("Superadmin already exists.")
        else:
            system_policy = SystemPolicy()
            notifier = NotificationService()
            
            superadmin = Admin(
                user_id="admin1",
                name="Super Admin",
                email=superadmin_email,
                password="pass",  # hash in production
                system_policy=system_policy,
                notifier=notifier
            )

            db.add(superadmin)
            db.commit()
            print("Superadmin created successfully!")
    finally:
        db.close()