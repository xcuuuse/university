from src.domain.entities.workload_data import WorkloadData

class DynamicPricing:
    def __init__(
            self,
            base_price: float = 0.0
    ):
        self.__base_price = base_price
        self.__current_price = base_price

    @property
    def current_price(self):
        return self.__current_price

    def recalculate_price(self, data: WorkloadData) -> float:
        self.__current_price = self.__base_price * (1 + data.calculate_workload())
        return self.__current_price
