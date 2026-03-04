import time
import uuid
from datetime import datetime
from .payment_method import PaymentMethod
from entities.payment_result import PaymentResult

class DebitCard(PaymentMethod):
    
    def __init__(self,card_number: str, expiry : str, cvv:str ):
        self.card_number = card_number
        self.expiry = expiry
        self.cvv = cvv

    def validate(self) -> bool:
        #16 digit check
        if len(self.card_number) != 16 or not self.card_number.isdigit():
            return False
        
        #cvv
        if len(self.cvv) not in (3,4) or not self.cvv.isdigit():
            return False 
        
        #expiry date - assuming its on MMYY format 
        now = datetime.now()
        current_year = now.year
        current_month = now.month

        try:
            card_year = int(self.expiry[2:]) + 2000
            card_month = int(self.expiry[0:2])
            if not 1 <= card_month <=12:
                return False
        except ValueError:
            return False #invalid format
        



        if card_year < current_year:
            return False 
        elif card_year == current_year:
            if card_month < current_month:
                return False
        
        return True 
    
    def process(self,amount:float) ->PaymentResult:
        if not self.validate():
            raise Exception("Invalid Debit Card details")
        
        time.sleep(3) #simulating processing delay 

        transactionID = str(uuid.uuid4())

        return PaymentResult(transactionID,True,amount)
        






