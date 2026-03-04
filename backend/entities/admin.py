from .system_policy import SystemPolicy
from .patterns.observer.notification_service import NotificationService
from .consultant.py import Consultant

class Admin:

  def __init__(self, system_policy: SystemPolicy, notifier: NotificationService):
    self.system_policy = system_policy
    self.notifier = notifier

  def approveConsultant(self, consultant: Consultant):
    consultant.approved = True
    self.notifier.notify_observers(
            f"Consultant {consultant.name} has been approved by the Admin.")

  def updatePolicies(self, cancellation_rules: str = None,
                   pricing_strategy: str = None,
                   refund_policy: str = None): #lets admnin update cancellation rules, pricing strategy and refund policy. Each parameter is optional so Admin can update one or multiple policies at once.
    if cancellation_rules is not None:
    self.system_policy.updateCancellationRules(cancellation_rules)
    self.notifier.notify_observers("Cancellation policy updated.") #notifies observers of a change in cancellation rules

    if pricing_strategy is not None:
            self.system_policy.updatePricingStrategy(pricing_strategy)
            self.notifier.notify_observers("Pricing strategy updated.")
  if refund_policy is not None:
            self.system_policy.updateRefundPolicy(refund_policy)
            self.notifier.notify_observers("Refund policy updated.")

    
