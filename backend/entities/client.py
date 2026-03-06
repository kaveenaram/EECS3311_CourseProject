from typing import List
from .user import User
from patterns.strategy.payment_method import PaymentMethod
from entities.payment_result import PaymentResult
from entities.booking import Booking

"""
Client Class: User who browses services and books consultating sessions.
"""
class Client(User):

    # Client constructor initializes payment methods and bookings list, and uses User constructor for basic attributes
    def __init__(self,user_id:str, name:str,email:str,password:str):
        super().__init__(user_id,name,email,password)

        self.payment_methods : List[PaymentMethod] = []
        self.bookings: List[Booking] = []

    # Client-specific methods for managing payment methods, viewing bookings, and payment history

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
    
    # Client login/logout methods with simple password check and console messages
    # Overrides user login/logout to provide client-specific messages and functionality

    def logIn(self, password: str) -> bool:
        if password == self.password:
            print(f"Welcome {self.name}")
            return True
        else:
            print(f"Password incorrect. Please try again...")
            return False

    def logOut(self) -> None:
        print(f"{self.name} logged out")

    def __str__(self):
        return f"Client {self.name} | Email: {self.email}"


    