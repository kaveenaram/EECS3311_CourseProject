from typing import List
from entities.service import Service
from entities.timeslot import TimeSlot
from entities.consultant import Consultant


class AvailabilityService:

    def __init__(self):
        # list all services
        self.services: List[Service] = []
        

  
    def add_service(self, service: Service):
        self.services.append(service)

    def browse_services(self) -> List[Service]:
        return self.services


  
    def add_timeslot(self, consultant: Consultant, timeslot: TimeSlot):
        consultant.add_timeslot(timeslot)

    def remove_timeslot(self, consultant: Consultant, timeslot: TimeSlot):
        if timeslot in consultant.timeslots:
            consultant.timeslots.remove(timeslot)

    def get_available_slots(self, consultant: Consultant) -> List[TimeSlot]:
        return [slot for slot in consultant.timeslots if slot.available]



    def validate_slot(self, consultant: Consultant, timeslot: TimeSlot) -> bool:
        # Ensures a slot:
        if timeslot not in consultant.timeslots:
            raise Exception("Timeslot does not belong to consultant")

        if not timeslot.available:
            raise Exception("Timeslot is already booked")

        return True


    def mark_slot_unavailable(self, timeslot: TimeSlot):
        timeslot.mark_unavailable()
