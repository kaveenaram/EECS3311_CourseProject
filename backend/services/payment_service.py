from typing import List
from entities.payment_result import PaymentResult
from entities.booking import Booking
from patterns.strategy.payment_method import PaymentMethod

"""
PaymentService Class: Manages the processing of payments for bookings, including validating payment methods, updating booking states, and maintaining a history of payments.
Provides a method to process payments for a given booking using a specified payment method and amount, and a method to retrieve the payment history.
"""

class PaymentService:

    def __init__(self):
        #initialising a list to store all the payments processed by the system 
        self.payment_history: List[PaymentResult] = []

    def process_payment(self,booking :Booking ,payment_method: PaymentMethod,amount:float) ->PaymentResult | None:
        #validate the payment method
        if not payment_method.validate():
            print("Invalid Payment Details")
            return None 

        #process payment using the selected payment method 
        result = payment_method.process(amount)   

        if result.success:
            booking.paid(amount)
            self.payment_history.append(result)
            return result
        else:
            print("Payment Failed. Please try again")
            return None
    
    def get_payment_history(self) -> List[PaymentResult]:
        return self.payment_history

