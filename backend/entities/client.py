from database import db
from .user import User
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

"""
Client Class: User who browses services and books consultating sessions.
"""
class Client(User):
    __tablename__ = "clients"

    user_id = Column(String, ForeignKey('users.user_id'), primary_key=True)
    payment_methods = relationship("PaymentMethod", back_populates="client")
    bookings = relationship("Booking", back_populates="client", foreign_keys='Booking.client_id')

    __mapper_args__ = {
        'polymorphic_identity': 'client'
    }

    # Client constructor initializes payment methods and bookings list, and uses User constructor for basic attributes
    def __init__(self,user_id:str, name:str,email:str,password:str):
        super().__init__(user_id,name,email,password)

    # Client-specific methods for managing payment methods, viewing bookings, and payment history

    def add_payment_method(self, method) -> None:
        self.payment_methods.append(method)

    def remove_payment_method(self, method) -> None:
        if method in self.payment_methods:
            self.payment_methods.remove(method)

    def get_bookings(self):
        return self.bookings

    def get_payment_history(self):
        from entities.payment_result import PaymentResult
        from entities.booking import Booking

        history = db.query(PaymentResult).join(
            Booking, PaymentResult.booking_id == Booking.id
            ).filter(Booking.client_id == self.user_id).all()
        
        return history

    def get_payment_methods(self):
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


    