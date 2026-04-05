from datetime import datetime
from typing import List
from entities.payment_result import PaymentResult
from entities.booking import Booking
from patterns.strategy.payment_method import PaymentMethod
from sqlalchemy.orm import Session

"""
PaymentService Class: Manages the processing of payments for bookings, including validating payment methods, updating booking states, and maintaining a history of payments.
Provides a method to process payments for a given booking using a specified payment method and amount, and a method to retrieve the payment history.
"""

class PaymentService:

    def __init__(self, db: Session):
        #initialising a list to store all the payments processed by the system 
        self.db = db

    def process_payment(self,booking :Booking ,payment_method: PaymentMethod,amount:float) ->PaymentResult | None:
        #validate the payment method
        if not payment_method.validate():
            print("Invalid Payment Details")
            return None 

        #process payment using the selected payment method 
        result = payment_method.process(amount)   

        if result.success:
            # record in db
            payment_result = PaymentResult(
                success=True,
                amount=amount,
                timestamp=datetime.now()
            )
            payment_result.booking_id = booking.booking_id

            booking.paid(amount)

            self.db.add(payment_result)
            self.db.commit()

            return payment_result
        else:
            print("Payment Failed. Please try again")
            return None
    
    def get_payment_history(self, booking_id: str):
        # Retrieve payment history for a specific booking
        payment_history = self.db.query(PaymentResult).filter_by(booking_id=booking_id).all()

        return payment_history

