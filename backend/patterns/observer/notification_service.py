from .observer import Observer
from .subject import Subject

"""
NotificationService Class: Implements the Subject interface for the Observer pattern to manage and notify observers of state changes.
"""

class NotificationService(Subject):

  def __init__(self):
    self.observers = [] #creates an empty list that stores all Observers

  def attach(self, observer: Observer):
    self.observers.append(observer) #adds the observer to the list created above

  def detach(self, observer: Observer):
    self.observers.remove(observer) #removes observer from the list

  def notifyObservers(self, message: str):
      for obs in self.observers:
        obs.update(message)
