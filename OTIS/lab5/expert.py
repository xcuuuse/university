class Expert:
    def __init__(self, title: str, degree: str, coefficient: float):
        self.__title = title
        self.__degree = degree
        self.__coefficient = coefficient

    @property
    def title(self):
        return self.__title

    @property
    def degree(self):
        return self.__degree

    @property
    def coefficient(self):
        return self.__coefficient