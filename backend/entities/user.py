from abc import ABC, abstractmethod

"""
User Class: Abstract base class representing a user in the system, with common attributes and methods for authentication and session management.
Both Admins, Consultants, and Clients will inherit from this class.
"""
class User(ABC):

    # User constructor initializes common user attributes like user ID, name, email, and password
    def __init__(self, user_id:str, name:str, email:str, password:str):
        self.user_id = user_id
        self.name = name 
        self.email = email
        self.password = password

    # Abstract methods for login and logout that must be implemented by subclasses, ensuring that each user type can have customized authentication behavior
    @abstractmethod
    def logIn(self,password:str) ->bool:
        pass

    @abstractmethod
    def logOut(self) ->None:
        pass 

