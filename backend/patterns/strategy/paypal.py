import re
import time
import uuid
from datetime import datetime
from .payment_method import PaymentMethod
from entities.payment_result import PaymentResult


class Paypal(PaymentMethod):
    
    def __init__(self,email: str):
        self.email = email     

    def validate(self) -> bool:
        return re.fullmatch(r"[^@]+@[^@]+\.[^@]+", self.email) is not None

    
    def process(self,amount:float) ->PaymentResult:
        if not self.validate():
            raise Exception("Invalid Paypal details")
        
        time.sleep(3) #simulating processing delay 

        transactionID = str(uuid.uuid4())

        return PaymentResult(transactionID,True,amount,datetime.now())
        







