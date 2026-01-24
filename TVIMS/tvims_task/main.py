import matplotlib.pyplot as plt
import numpy as np
import math

def empirical_graph(data: list): #1.2
    x = np.sort(data)
    n = len(data)
    y = np.arange(1, n + 1) / n
    lambda_val = 0.5516
    x_theory = np.linspace(0, max(data), 500)
    y_theory = 1 - np.exp(-lambda_val * x_theory)
    plt.figure(figsize=(10, 6))
    plt.step(x, y, where='post', label='Эмпирическая функция', color='blue', alpha=0.7)
    plt.plot(x_theory, y_theory, label=f'F(x) = 1 - e^{{-{lambda_val}x}}', color='red', linewidth=2)
    plt.title('График эмпирической функции распределения')
    plt.title('Эмпирическая и теоретическая функции распределения')
    plt.xlabel('x')
    plt.ylabel('F(x)')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)

    plt.xlim(0, max(data) + 0.5)
    plt.ylim(0, 1.05)

    plt.show()


def histogram(data): #1.4
    sorted_data = sorted(data)
    n = len(sorted_data)
    k = 10
    m = n // k
    custom_bins = [sorted_data[i * m] for i in range(k)]
    custom_bins.append(sorted_data[-1])
    plt.figure(figsize=(12, 6))
    plt.hist(data, bins=custom_bins, density=True, color='blue', edgecolor='black', alpha=0.8)
    plt.title('Равновероятностная гистограмма (по заданным границам)')
    plt.xticks(custom_bins, rotation=45)
    plt.grid(axis='y', linestyle=':', alpha=0.7)
    plt.tight_layout()
    plt.show()


one_dim = [
    0.61, 1.19, 1.26, 2.90, 5.82, 0.28, 2.27, 2.61, 0.62, 4.76,
    3.94, 0.59, 0.72, 2.75, 1.55, 6.22, 3.76, 0.03, 0.67, 0.24,
    0.21, 0.89, 0.66, 0.92, 2.84, 1.72, 0.06, 0.68, 1.92, 0.32,
    0.02, 1.55, 0.15, 0.18, 0.53, 1.57, 0.19, 0.55, 4.24, 3.24,
    1.43, 0.75, 2.09, 0.73, 3.60, 0.36, 0.90, 2.64, 3.20, 0.33,
    7.63, 0.67, 0.97, 1.97, 0.29, 1.14, 0.24, 3.19, 2.86, 4.72,
    2.51, 1.79, 1.32, 2.02, 1.72, 0.54, 3.30, 1.76, 1.47, 2.29,
    0.69, 1.87, 3.45, 0.13, 0.54, 3.05, 1.61, 4.30, 1.74, 4.24,
    1.88, 1.70, 0.07, 4.45, 0.07, 1.71, 1.95, 3.11, 1.44, 0.46,
    0.45, 5.32, 0.24, 3.79, 1.85, 3.36, 2.24, 0.66, 1.21, 0.09
]


#empirical_graph(one_dim)
#histogram(one_dim)
x_emp = np.sort(one_dim)
n = len(x_emp)

# Значения i/n и (i-1)/n
fn_top = np.arange(1, n + 1) / n
fn_bot = np.arange(0, n) / n

# Значения теоретической функции
f_theory = 1 - np.exp(-0.5516 * x_emp)

# Считаем разности
d_plus = np.abs(fn_top - f_theory)
d_minus = np.abs(fn_bot - f_theory)

# Максимальное отклонение
Dn = max(np.max(d_plus), np.max(d_minus))
print(f"Максимальное отклонение Dn: {Dn}")
data = [
    (1.20, 1.10), (-0.98, 1.04), (-1.05, -0.02), (0.34, 0.84), (0.87, 0.30),
    (-4.12, -3.87), (0.72, -0.43), (1.28, -1.46), (-1.60, -1.25), (-0.21, -1.81),
    (0.56, 2.68), (-1.82, -3.04), (-2.74, -1.48), (-3.33, -3.16), (-1.33, -3.13),
    (-2.20, -2.57), (0.52, -1.56), (-0.29, -0.64), (-1.72, -1.86), (-1.81, -2.36),
    (-0.63, -2.38), (-0.75, -1.11), (-1.27, -0.79), (-0.30, -0.14), (0.70, 0.93),
    (2.64, 0.85), (-2.58, -1.80), (-1.53, -3.69), (-1.00, -0.72), (-0.35, -2.87),
    (-1.00, -0.32), (-2.55, -1.37), (0.10, -0.43), (-1.26, -1.34), (-1.81, -2.52),
    (-0.75, -0.35), (0.85, -1.30), (1.45, 0.31), (0.41, -1.78), (-0.76, -2.72),
    (-0.98, -1.83), (-0.96, -1.49), (-4.70, -4.92), (-1.76, -2.78), (3.24, 0.33),
    (-2.36, -1.85), (-1.16, -2.83), (-2.85, -3.26), (0.20, -3.18), (-2.04, -1.04)
]


# Разделяем на X и Y
X = [pair[0] for pair in data]
Y = [pair[1] for pair in data]
n = len(data)
mx = sum(X) / n
my = sum(Y) / n
mxy = sum([pair[0]*pair[1] for pair in data]) / n
sq_x = [i*i for i in X]
sq_y = [i*i for i in Y]

D_x = n/(n-1) * ((sum(sq_x) / n) - (mx * mx))
D_y = n/(n-1) * ((sum(sq_y) / n) - (my * my))
K_xy = n/(n-1) * mxy - n/(n-1) * mx*my
R_xy = K_xy / (math.sqrt(D_x*D_y))
Z = abs(R_xy) * math.sqrt(n) / (1-(R_xy)*(R_xy))
print(Z)
# Объём выборки
"""n = len(X)

# Средние значения
x_mean = sum(X) / n
y_mean = sum(Y) / n

# Вычисляем параметры регрессии (a1 и a0)
numerator = sum((x - x_mean) * (y - y_mean) for x, y in zip(X, Y))
denominator = sum((x - x_mean) ** 2 for x in X)
a1 = numerator / denominator
a0 = y_mean - a1 * x_mean

# Создаём точки для линии регрессии (для плавной линии)
import numpy as np
x_line = np.linspace(min(X), max(X), 100)
y_line = a0 + a1 * x_line

# Строим график
plt.figure(figsize=(10, 7))
plt.scatter(X, Y, color='blue', alpha=0.7, label='Данные (наблюдения)')
plt.plot(x_line, y_line, color='red', linewidth=2, label=f'Линия регрессии: y = {a0:.2f} + {a1:.2f}x')

# Настройки графика
plt.title('Диаграмма рассеяния и линия регрессии', fontsize=14)
plt.xlabel('X', fontsize=12)
plt.ylabel('Y', fontsize=12)
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)

# Показать график
plt.show()

# Выводим уравнение в консоль
print(f"Уравнение линии регрессии: y = {a0:.4f} + ({a1:.4f}) * x") """