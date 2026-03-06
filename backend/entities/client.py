from typing import List
from .user import User
from backend.patterns.strategy.payment_method import PaymentMethod
from ..entities.payment_result import PaymentResult
from ..entities.booking import Booking

class Client(User):

    def __init__(self,user_id:str, name:str,email:str,password:str):
        super().__init__(user_id,name,email,password)

        self.payment_methods : List[PaymentMethod] = []
        
        self.bookings: List[Booking] = []


    def add_payment_method(self, method: PaymentMethod ) -> None:
        self.payment_methods.append(method)

    def remove_payment_method(self, method : PaymentMethod) -> None:
        if method in self.payment_methods:
            self.payment_methods.remove(method)

    def get_bookings(self) -> List[Booking]:
        return self.bookings

    def get_payment_history(self) -> List[PaymentResult]:
        history = []
        for booking in self.bookings:
            history.extend(booking.payment_history)
        return history

    def get_payment_methods(self) -> List[PaymentMethod]:
        return self.payment_methods
    
    def logIn(self, password: str) -> bool:
        if password == self.password:
            print(f"Welcome {self.name}")
            return True
        else:
            print(f"password incorrect.Please try again...")
            return False

    def logOut(self) -> None:
        print(f"{self.name} logged out")


    