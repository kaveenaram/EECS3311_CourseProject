from datetime import datetime

class PaymentResult:
  def __init__(self,transactionID:str, success:bool, amount:float ):
    self.transactionID = transactionID
    self.success = success
    self.timestamp = datetime.now()
    self.amount = amount

  def __str__(self):
    return(
      f"Transaction ID: {self.transactionID} \n"
      f"Success: {self.success} \n"
      f"Timestamp: {self.timestamp} \n"
      f"Base Price: {self.amount}")

    
