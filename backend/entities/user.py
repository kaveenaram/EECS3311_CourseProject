from abc import ABC, abstractmethod

class User(ABC):

    def __init__(self, user_id:str, name:str, email:str):
        self.user_id = user_id
        self.name = name 
        self.email = email

    @abstractmethod
    def logIn(self,password:str) ->bool:
        pass

    @abstractmethod
    def logOut(self) ->None:
        pass 

