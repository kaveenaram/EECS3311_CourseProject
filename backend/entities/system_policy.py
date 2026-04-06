from database import db
from sqlalchemy import Column, String
from database.db import Base

"""
SystemPolicy Class: Represents the overarching policies of the consulting platform, including cancellation rules, pricing strategy, and refund policy.
Admins can update these policies, and they are used to govern how the platform operates and how consultants and clients interact with the system.
"""

class SystemPolicy(Base):
    __tablename__ = "system_policies"

    id = Column(String(255), primary_key=True)
    cancellation_rules = Column(String(1000))
    pricing_strategy = Column(String(1000))
    refund_policy = Column(String(1000))
    
    # SystemPolicy constructor initializes cancellation rules, pricing strategy, and refund policy with default empty values
    def __init__(self, cancellationRules = "", pricingStrategy = "", refundPolicy=""):
        self.cancellationRules = cancellationRules
        self.pricingStrategy = pricingStrategy
        self.refundPolicy = refundPolicy

    # Methods to update policies, which can be called by the Admin class to modify the system's rules and strategies

    def updateCancellationRules(self, rules: str): #U12: define policies. Replaces existing cancellation rules with new ones.
      self.cancellationRules = rules
      db.commit() 

    def updatePricingStrategy(self, strategy: str): #updates pricing strategy
      self.pricingStrategy = strategy
      db.commit()

    def updateRefundPolicy(self, refund: str): #how and when refunds are issued
      self.refundPolicy = refund
      db.commit()
      
