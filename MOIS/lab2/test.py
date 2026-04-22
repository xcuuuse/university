from experta import *

class Parameter(Fact):
    pass

class Probability(Fact):
    pass

class ProbabilityEngine(KnowledgeEngine):
    @Rule(NOT(Parameter(name='погода')))
    def ask_weather(self):
        value = input("Погода (ясная/пасмурная/неизвестно): ").strip().lower()
        self.declare(Parameter(name='погода', value=value))

    @Rule(NOT(Parameter(name='время_суток')))
    def ask_time(self):
        value = input("Время суток(день/ночь/неизвестно): ").strip().lower()
        self.declare(Parameter(name='время_суток', value=value))

    @Rule(NOT(Parameter(name='состояние_дороги')))
    def ask_road_state(self):
        value = input("Состояние дороги (целая/поврежденная/неизвестно): ").strip().lower()
        self.declare(Parameter(name='состояние_дороги', value=value))

    @Rule(NOT(Parameter(name='скорость')))
    def ask_speed(self):
        value = input("Скорость (высокая/низкая/неизвестно): ").strip().lower()
        self.declare(Parameter(name='скорость', value=value))

    @Rule(NOT(Parameter(name='опыт_водителя')))
    def ask_driver_experience(self):
        value = input("Опыт водителя(нет/средний/высокий/неизвестно): ").strip().lower()
        self.declare(Parameter(name='опыт_водителя', value=value))

    @Rule(
        Parameter(name='погода', value='пасмурная'),
        Parameter(name='время_суток', value='ночь'),
        Parameter(name='состояние_дороги', value='поврежденная'),
        Parameter(name='скорость', value='высокая'),
        Parameter(name='опыт_водителя', value='нет') | Parameter(name='опыт_водителя', value='средний'))
    def high_risk(self):
        self.declare(Probability(name='Высокая'))
        print('Вероятность ДТП: высокая')

    @Rule(
        Parameter(name='погода', value='пасмурная') | Parameter(name='погода', value='ясная'),
        Parameter(name='время_суток', value='ночь') | Parameter(name='время_суток', value='день'),
        Parameter(name='состояние_дороги', value='поврежденная'),
        Parameter(name='скорость', value='высокая') | Parameter(name='скорость', value='неизвестно'),
        Parameter(name='опыт_водителя', value='нет') | Parameter(name='опыт_водителя', value='средний'))
    def low_risk(self):
        self.declare(Probability(name='Низкая'))
        print('Вероятность ДТП: низкая')

    @Rule(
        Parameter(name='погода', value='ясная'),
        Parameter(name='время_суток', value='день') | Parameter(name='время_суток', value='ночь'),
        Parameter(name='состояние_дороги', value='целая'),
        Parameter(name='скорость', value='низкая') | Parameter(name='скорость', value='неизвестно'),
        Parameter(name='опыт_водителя', value='высокий') | Parameter(name='опыт_водителя', value='средний') |
        Parameter(name='опыт_водителя', value='средний'))
    def zero_risk(self):
        self.declare(Probability(name='Нулевая'))
        print('Вероятность ДТП: нулевая')

    @Rule(
        Parameter(name='погода', value = MATCH.w),
        Parameter(name='время_суток', value=MATCH.t),
        Parameter(name='состояние_дороги', value=MATCH.s),
        Parameter(name='скорость', value=MATCH.sp),
        Parameter(name='опыт_водителя', value=MATCH.e),
        NOT(Probability())
    )
    def unknown(self, w, t, s, sp, e):
        print("Неизвестно")
        print(f"Введённые параметры: погода={w}, время={t}, состояние дороги={s}, скорость={sp}, опыт водителя={e}")


if __name__ == "__main__":
    engine = ProbabilityEngine()
    engine.reset()
    engine.run()

    # состояние дороги, скорость, опыт водителя