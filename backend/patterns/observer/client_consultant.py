from .observer import Observer


class Client(Observer): #inherits from the observer interface
    def update(self, message: str): 
        print(f"[Client Notification] {message}") #implements how the notification is received by the client


class Consultant(Observer):
    def update(self, message: str):
        print(f"[Consultant Notification] {message}") #implements how the notification is received by the consultant
