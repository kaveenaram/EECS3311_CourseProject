from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from entities.consultant import Consultant

"""
Service Class: Represents a consulting service offered by a consultant, including details like name, duration, price, and associated consultant.
"""

class Service:
    # Service constructor initializes service attributes including a reference to the consultant offering the service

    def __init__(self, service_id: str, serviceName: str, duration: int, price: float, consultant: "Consultant"):
        self.service_id = service_id
        self.serviceName = serviceName
        self.duration = duration
        self.price = price
        self.consultant = consultant

    def __str__(self):
        return f"{self.serviceName} | {self.duration} mins | ${self.price}"
