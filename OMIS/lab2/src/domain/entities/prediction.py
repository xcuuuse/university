from datetime import date

class Prediction:
    def __init__(
            self,
            prediction_date: date,
            expected_workload: float
    ):
        self.__prediction_date = prediction_date
        self.__expected_workload = expected_workload

    @property
    def prediction_date(self) -> date:
        return self.__prediction_date

    @property
    def expected_workload(self) -> float:
        return self.__expected_workload

    def predict_workload(self) -> float:
        return self.__expected_workload




