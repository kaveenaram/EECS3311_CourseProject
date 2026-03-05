import time
from datetime import datetime
from .payment_method import PaymentMethod
from entities.payment_result import PaymentResult


class BankTransfer(PaymentMethod):
    
    def __init__(self, account_number: str, routing_number:str):
        self.account_number = account_number
        self.routing_number = routing_number    

    def validate(self) -> bool:
        #account number - assuming its all digits and length is between 8 -12 
        if (not 8<= len(self.account_number) <=12) or (not self.account_number.isdigit()):
            return False
        
        #routing number - making sure it's length is 9
        if len(self.routing_number) != 9 or not self.routing_number.isdigit():
            return False
        
        return True

    
    def process(self,amount:float) ->PaymentResult:
        if not self.validate():
            raise Exception("Invalid Bank Transfer details")
        
        time.sleep(3) #simulating processing delay 

        return PaymentResult(True,amount,datetime.now())
        







