from .observer import Observer

"""
Subject Class: Abstract base class representing a subject in the Observer pattern, which defines methods for attaching, detaching, and notifying observers of state changes.
"""

class Subject:
  def attach(self, observer: Observer):
    raise NotImplementedError 

  def detach(self, observer: Observer):
    raise NotImplementedError

  def notifyObservers(self, msg : str):
    raise NotImplementedError
