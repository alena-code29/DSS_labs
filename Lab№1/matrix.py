import numpy as np

print("Матричная игра. Вариант 8")

# Платежная матрица
matrix = np.array([
    [9, 6, 0, 11, 12],
    [8, 5, 6, 7, 11],
    [12, 7, 7, 7, 9],
    [4, 0, 12, 10, 12],
    [3, 12, 9, 1, 8]
])

print("Платежная матрица:")
print(matrix)

# Поиск седловой точки
lower_price = max([min(x) for x in matrix])
upper_price = min([max(x) for x in np.rot90(matrix)])

print(f"Нижняя цена игры α = {lower_price}")
print(f"Верхняя цена игры β = {upper_price}")

if lower_price == upper_price:
    print(f"Седловая точка есть, v = {lower_price}")
else:
    print("Седловой точки нет, игра решается в смешанных стратегиях")

# Оптимальные смешанные стратегии
p = [0.36, 0.0, 0.12, 0.29, 0.22]  # стратегии A
q = [0.4, 0.5, 0.09, 0.02, 0.0]    # стратегии B

print(f"P* = {p}")
print(f"Q* = {q}")

# Расчет выигрышей (код из лекций)
answer = {}

if lower_price == upper_price:
    print("седловая точка есть", f"ответ v={lower_price}")
else:
    buff = 0
    for i, pin in zip(matrix, p):
        buff += pin * sum([x*y for x,y in zip(i,q)])
    answer["H(P,Q)"] = buff
    
    for k, i in enumerate(np.rot90(matrix), 1):
        answer["H(P,B{})".format(k)] = sum([x*y for x,y in zip(i,p)])

for i in [(x,y) for x,y in answer.items()]:
    print("Ответ выигрыш игрока А в ситуации {0[0]} = {0[1]}".format(i))

# Активные стратегии
active_A = [f"A{i+1}" for i in range(len(p)) if p[i] > 0.001]
active_B = [f"B{i+1}" for i in range(len(q)) if q[i] > 0.001]

print(f"Активные стратегии A: {active_A}")
print(f"Активные стратегии B: {active_B}")

print(f"Цена игры: {answer.get('H(P,Q)', 'не определена')}")
