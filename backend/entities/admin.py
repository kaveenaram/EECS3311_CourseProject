from sqlalchemy import Column, String, ForeignKey
from .user import User
from database import db
from .system_policy import System_Policy
from patterns.observer.notification_service import NotificationService

"""
Admin Class: Platform administrator who oversees consultants and system policies
"""

class Admin(User):
    __tablename__ = "admins"

    user_id = Column(String, ForeignKey('users.user_id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'admin'
    }
    # Admin constructor takes in system policy and notification service for managing policies and sending notifications
    # Uses User constructor for basic user attributes

    def __init__(self, user_id: str, name: str, email: str, password: str,
                 system_policy: System_Policy, notifier: NotificationService):
        super().__init__(user_id, name, email, password)
        self.system_policy = system_policy
        self.notifier = notifier

    # Admin login/logout methods with simple password check and console messages
    # Overrides user login/logout to provide admin-specific messages and functionality
    def logIn(self, password: str) -> bool:
        if password == self.password:
            print(f"Admin {self.name} logged in.")
            return True
        print("Incorrect password.")
        return False

    def logOut(self) -> None:
        print(f"Admin {self.name} logged out.")

    # Admin-specific methods for approving consultants and updating system policies

    def approveConsultant(self, consultant, db):
        consultant.approved = True
        db.commit()
        self.notifier.notifyObservers(
            f"Consultant {consultant.name} has been approved by the Admin."
        )

    def updatePolicies(self, db, cancellation_rules: str = None,
                       pricing_strategy: str = None,
                       refund_policy: str = None):

        if cancellation_rules is not None:
            self.system_policy.updateCancellationRules(cancellation_rules)
            db.commit()
            self.notifier.notifyObservers("Cancellation policy updated.")

        if pricing_strategy is not None:
            self.system_policy.updatePricingStrategy(pricing_strategy)
            db.commit()
            self.notifier.notifyObservers("Pricing strategy updated.")

        if refund_policy is not None:
            self.system_policy.updateRefundPolicy(refund_policy)
            db.commit()
            self.notifier.notifyObservers("Refund policy updated.")

    def __str__(self):
        return f"Admin {self.name} | Email: {self.email}"
