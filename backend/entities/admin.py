from .user import User
from .system_policy import SystemPolicy
from patterns.observer.notification_service import NotificationService
from .consultant import Consultant

class Admin(User):

    def __init__(self, user_id: str, name: str, email: str, password: str,
                 system_policy: SystemPolicy, notifier: NotificationService):
        super().__init__(user_id, name, email, password)
        self.system_policy = system_policy
        self.notifier = notifier

    def logIn(self, password: str) -> bool:
        if password == self.password:
            print(f"Admin {self.name} logged in.")
            return True
        print("Incorrect password.")
        return False

    def logOut(self) -> None:
        print(f"Admin {self.name} logged out.")

    def approveConsultant(self, consultant: Consultant):
        consultant.approved = True
        self.notifier.notifyObservers(
            f"Consultant {consultant.name} has been approved by the Admin."
        )

    def updatePolicies(self, cancellation_rules: str = None,
                       pricing_strategy: str = None,
                       refund_policy: str = None):

        if cancellation_rules is not None:
            self.system_policy.updateCancellationRules(cancellation_rules)
            self.notifier.notifyObservers("Cancellation policy updated.")

        if pricing_strategy is not None:
            self.system_policy.updatePricingStrategy(pricing_strategy)
            self.notifier.notifyObservers("Pricing strategy updated.")

        if refund_policy is not None:
            self.system_policy.updateRefundPolicy(refund_policy)
            self.notifier.notifyObservers("Refund policy updated.")
