from .observer import Observer
class Subject:
  def attach(self, observer: Observer):
    raise NotImplementedError 

  def detach(self, observer: Observer):
    raise NotImplementedError

  def notifyObservers(self, msg : str):
    raise NotImplementedError
