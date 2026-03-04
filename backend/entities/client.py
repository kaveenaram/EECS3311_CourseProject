from typing import List
from .user import User
from patterns.strategy.payment_method import PaymentMethod
from entities.booking import Booking

class Client(User):

    def __init__(self,user_id:str, name:str,email:str):
        super().__init__(user_id,name,email)

        self.payment_methods : List[PaymentMethod] = []
        
        self.bookings: List[Booking] = []  #please feel free to change this as needed 


    def add_payment_method(self, method: PaymentMethod ) -> None:
        self.payment_methods.append(method)

    def remove_payment_method(self, method : PaymentMethod) -> None:
        if method in self.payment_methods:
            self.payment_methods.remove(method)

    def get_payment_history(self):
        pass

    def get_payment_methods(self) -> List[PaymentMethod]:
        return self.payment_methods
    
    def login(self, password: str) -> bool:
        print(f"Welcome {self.name}")
        return True

    def logout(self) -> None:
        print(f"{self.name} logged out")


    