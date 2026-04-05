import re
import time
from datetime import datetime

from database.db import Base
from .payment_method import PaymentMethod
from entities.payment_result import PaymentResult
from sqlalchemy import Column, String, ForeignKey

"""
Paypal Class: Implements the PaymentMethod interface for processing PayPal payments.
"""
class Paypal(PaymentMethod):
    __tablename__ = "paypal"

    id = Column(String, ForeignKey('payment_methods.id'), primary_key=True)
    paypal_email = Column(String)

    __mapper_args__ = {
        'polymorphic_identity': 'paypal'
    }
    
    def __init__(self,email: str):
        self.email = email     

    def validate(self) -> bool:
        return re.fullmatch(r"[^@]+@[^@]+\.[^@]+", self.email) is not None

    def process(self,amount:float) ->PaymentResult:
        if not self.validate():
            raise Exception("Invalid Paypal details")
        
        time.sleep(3) #simulating processing delay 

        return PaymentResult(True,amount,datetime.now())
        







