class Observer:
    def update(self, message: str):
        raise NotImplementedError #prevents the base case from being used directly. If its not overriden, python will throw an error.
