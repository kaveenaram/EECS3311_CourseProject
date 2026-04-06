from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from database.db import Base
from abc import abstractmethod

"""
PaymentMethod Class: Abstract base class representing a payment method in the Strategy pattern, which defines the interface for validating and processing payments.
Concrete implementations will include CreditCard, DebitCard, and BankTransfer, each with their own validation and processing logic.
"""

#abstract class
# phase 2 sqlalchemy handles the inheritance properly
class PaymentMethod(Base):
    __tablename__ = "payment_methods"
    
    id = Column(String(255), primary_key=True)
    type = Column(String(50))
    client_id = Column(String(255), ForeignKey('clients.user_id'))
    
    client = relationship("Client", back_populates="payment_methods")
    
    __mapper_args__ = {
        'polymorphic_identity': 'payment_method',
        'polymorphic_on': type
    }

    @abstractmethod
    def validate(self) -> bool:
      pass 

    @abstractmethod
    def process(self, amount:float):
      pass

    
  
