from abc import ABC, abstractmethod

"""
Observer Class: Abstract base class representing an observer in the Observer pattern, which defines the update() method that will be called by the Subject to notify observers of state changes.
Observers can be clients, consultants, or any other entities that need to be notified of changes in the system, such as booking status updates or policy changes.
"""
class Observer(ABC):

    # Abstract method that must be implemented by concrete observer classes to handle updates from the subject.
    # The message parameter can contain information about the state change or event that occurred.
    @abstractmethod
    def update(self, message: str) -> None:
        pass
