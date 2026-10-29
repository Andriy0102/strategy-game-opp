class Resources:
    def __init__(self, res_type: str = "Gold", amount: int = 1):
        self._res_type = res_type
        self.amount = amount

    @property
    def res_type(self) -> str:
        return self._res_type

    @property
    def amount(self) -> int:
        return self._amount

    # Prevent economic bugs or negative quantities
    @amount.setter
    def amount(self, value: int):
        if value < 0:
            raise ValueError("Amount cannot be negative!")
        self._amount = value

    #Safely deducts resources and returns the amount actually collected
    def collect(self, requested_amount: int) -> int:
        if requested_amount <= 0:
            return 0

        taken_amount = min(self.amount, requested_amount)
        self.amount -= taken_amount
        return taken_amount

    def __repr__(self):
        return f'Resources({self.res_type}: {self.amount})'