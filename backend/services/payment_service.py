from typing import List
from entities.payment_result import PaymentResult

#this class process payments, update booking state,stores history and provide access to the history 
class PaymentService:

    def __init__(self):
        #initialising a list to store all the payments processed by the system 
        self.payment_history: List[PaymentResult] = []

    def process_payment(self,booking,payment_method,amount:float) ->PaymentResult:
        #process payment using the selected payment method 
        result = payment_method.process(amount)   

        if result.success:
            booking.paid(amount)
            self.payment_history.append(result)

        return result
    
    def get_payment_history(self) -> List[PaymentResult]:
        return self.payment_history

