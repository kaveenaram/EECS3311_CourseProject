from abc import ABC, abstractmethod
from entities.payment_result import PaymentResult

"""
PaymentMethod Class: Abstract base class representing a payment method in the Strategy pattern, which defines the interface for validating and processing payments.
Concrete implementations will include CreditCard, DebitCard, and BankTransfer, each with their own validation and processing logic.
"""

#abstract class 
class PaymentMethod(ABC):
  @abstractmethod
  def validate(self) -> bool:
    pass 

  @abstractmethod
  def process(self, amount:float)->PaymentResult:
    pass

    
  
