from experta import *

class Factorial(Fact):
    n = Field(lambda n: isinstance(n, int) and n >= 0, mandatory=True)
    result = Field(int, mandatory=True)

class ComputeFactorial(KnowledgeEngine):
    @DefFacts()
    def first(self):
        yield Factorial(n=0, result=1)

    @Rule(
        AS.f << Factorial(
            n=MATCH.n,
            result=MATCH.r))
    def factorial(self, f, n, r):
        self.declare(
            Factorial(
                n=n + 1,
                result=(n + 1) * r))
        self.retract(f)

cf = ComputeFactorial()
cf.reset()
cf.run(1000)
print(cf.facts)
