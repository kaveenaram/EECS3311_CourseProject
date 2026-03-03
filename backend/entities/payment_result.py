from datetime import datetime

class PaymentResult:
  def __init__(self,transactionID:str, success:bool, base_price:float, timestamp:datetime = None):
    self.transactionID = transactionID
    self.success = success
    self.timestamp = timestamp
    self.base_price = base_price

    


