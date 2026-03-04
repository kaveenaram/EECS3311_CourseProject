class TimeSlot:

  def __init__(self, slot_id: str, start_time: str, end_time: str):
      self.slot_id = slot_id
      self.start_time = start_time
      self.end_time = end_time
      self.available = True

  def mark_unavailable(self):
      self.available = False

  def mark_available(self):
      self.available = True

  def __str__(self):
      return f"{self.start_time} - {self.end_time} | Available: {self.available}"
