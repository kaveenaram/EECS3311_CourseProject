class NotificationService(Subject):

  def __init__(self):
    self.observers = []

  def attach(self, observer: Observer):
    
