class SystemPolicy:
    def __init__(self, cancellationRules = "", pricingStrategy = "", refundPolicy=""):
        self.cancellationRules = cancellationRules
        self.pricingStrategy = pricingStrategy
        self.refundPolicy = refundPolicy
    def updateCancellationRules(self, rules: str): #U12: define policies. Replaces existing cancellation rules with new ones.
      self.cancellationRules = rules
    def updatePricingStrategy(self, strategy: str): #updates pricing strategy
      self.pricingStrategy = strategy
    def updateRefundPolicy(self, refund: str): #how and when refunds are issued
      self.refundPolicy = refund
      
