import random
from expert import Expert


def random_composition():
    nums = [random.random() for _ in range(4)]
    total = sum(nums)
    return [round(x / total, 2) for x in nums]


experts = [
    Expert("complex supervisor", "PhD", 4.5), #руководитель комплекса
    Expert("headmaster", "Doctor of Science", 8.0),#директор
    Expert("deputy supervisor", "Academician", 7.5) #зам руководителя
]
goals = ["Brightness", "Frequency", "Resolution", "Diagonal"]

matrix = [random_composition() for _ in experts]

total_R = sum(e.coefficient for e in experts)
Z = [round(e.coefficient / total_R, 2) for e in experts]

weights = []
for i in range(len(goals)):
    w_i = sum(matrix[j][i] * Z[j] for j in range(len(experts)))
    weights.append(round(w_i, 2))

sum_check = round(sum(weights), 2)

sorted_goals = sorted(zip(goals, weights), key=lambda x: x[1], reverse=True)

print("Matrix of goal weights (Vji):")
print("Ej/Zi\t", "\t".join(goals))
for idx, expert in enumerate(experts):
    print(f"{expert.title} ({expert.degree})\t", "\t".join(map(str, matrix[idx])))

print("\nExpert competence coefficients:")
for i, expert in enumerate(experts):
    print(f"{expert.title} ({expert.degree}) -> R{i+1} = {expert.coefficient}, Z{i+1} = {Z[i]}")

print("\nGoal weights (Wi):")
for goal, weight in zip(goals, weights):
    print(f"{goal}: {weight}")

print(f"Sum of all Wi = {sum_check}\n")
print("Goal preferences:")
for goal, weight in sorted_goals:
    print(f"{goal}: {weight}")

