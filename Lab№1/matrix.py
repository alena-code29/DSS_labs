import numpy as np

print("1. Находим седло:")
matrix = np.array([
    [9, 6, 0, 11, 12],
    [8, 5, 6, 7, 11],
    [12, 7, 7, 7, 9],
    [4, 0, 12, 10, 12],
    [3, 12, 9, 1, 8]
])

lower_price = max([min(x) for x in matrix])
upper_price = min([max(x) for x in np.rot90(matrix)])

print(f"Нижняя цена игры (α): {lower_price}")
print(f"Верхняя цена игры (β): {upper_price}")

if lower_price == upper_price:
    print("седловая точка есть", f"ответ v={lower_price}")
else:
    print("седловой точки нет")
    print()

print("2. Расчет выигрышей:")

p = [0.36, 0.0, 0.12, 0.29, 0.22] # стратегии игрока A
q = [0.4, 0.5, 0.09, 0.02, 0.0]   # стратегии игрока B

buff = 0 # подсчёт мат ожидания
for i, pin in zip(matrix, p): # произведение вероятности выбора стратегии и суммы выигрыша
    buff += pin * sum([x * y for x, y in zip(i, q)])
answer = {}
answer["H(P,Q)"] = buff

for k, i in enumerate(np.rot90(matrix), 1):
    answer["H(P,B{})".format(k)] = sum([x * y for x, y in zip(i, p)]) #мат ожидание для чистых стратегий B

for situation, win in answer.items():
    print(f"Ответ выигрыш игрока A в ситуации {situation} = {win}")

print("\n3. Активные стратегии:")
active_A = [f"A{i+1}" for i in range(len(p)) if p[i] > 0.001]
active_B = [f"B{i+1}" for i in range(len(q)) if q[i] > 0.001]
print(f"Активные стратегии A: {active_A}")
print(f"Активные стратегии B: {active_B}")

print("\n4. Итог:")
print(f"Цена игры: {answer['H(P,Q)']}")
print(f"P = {p}")
print(f"Q = {q}")
