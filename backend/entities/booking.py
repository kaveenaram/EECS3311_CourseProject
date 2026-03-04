class Booking:

  def __init__(self, booking_id, client, consultant, service, timeslot):
      self.booking_id = booking_id
      self.client = client
      self.consultant = consultant
      self.service = service
      self.timeslot = timeslot

      self.state = "CONFIRMED"


  
  def mark_as_paid(self):
      if self.state == "CONFIRMED":
          self.state = "PAID"
          self.timeslot.mark_unavailable()
      else:
          raise Exception("Booking cannot be marked as paid")

  def __str__(self):
      return f"Booking {self.booking_id} | State: {self.state}"
