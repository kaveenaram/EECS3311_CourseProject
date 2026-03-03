from abc import ABC, abstractmethod
from entities.payment_result import PaymentResult

#abstract class 
class paymentMethod(ABC):
  @abstractmethod
  def validate(self) -> bool:
    pass 

  @abstractmethod
  def process(self, amount:float)->PaymentResult:
    pass

    
  
