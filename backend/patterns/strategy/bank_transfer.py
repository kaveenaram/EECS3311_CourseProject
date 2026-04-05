import time
from datetime import datetime

from database.db import Base
from .payment_method import PaymentMethod
from entities.payment_result import PaymentResult
from sqlalchemy import Column, String, ForeignKey

"""
BankTransfer Class: Implements the PaymentMethod interface for processing bank transfers.
"""

class BankTransfer(PaymentMethod):
    __tablename__ = "bank_transfers"

    id = Column(String, ForeignKey('payment_methods.id'), primary_key=True)
    account_no = Column(String)
    routing_no = Column(String)

    __mapper_args__ = {
        'polymorphic_identity': 'bank_transfer'
    }
    
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
        







