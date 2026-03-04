class Service:

  def __init__(self, service_id: str, title: str, duration: int, price: float, consultant):
      self.service_id = service_id
      self.title = title
      self.duration = duration
      self.price = price
      self.consultant = consultant

  def __str__(self):
      return f"{self.title} | {self.duration} mins | ${self.price}"
