from pulp import *
import time

# Исходные данные варианта 8
a = [200, 400, 600, 200, 200]  # запасы поставщиков
b = [200, 400, 400, 300, 500]  # спрос потребителей

c = [[1, 6, 9, 3, 4],  
     [3, 2, 2, 4, 5],  
     [4, 5, 4, 7, 6],  
     [1, 4, 3, 9, 8],  
     [7, 9, 7, 1, 9]]   # тарифы

print("Транспортная задача. Вариант 8")
print(f"Запасы: {a}, сумма = {sum(a)}")
print(f"Спрос: {b}, сумма = {sum(b)}")

# Проверка на сбалансированность
if sum(a) != sum(b):
    print("Задача открытая")
    if sum(a) < sum(b):
        a.append(sum(b) - sum(a))
        c.append([0] * len(b))
        print("Добавлен фиктивный поставщик")
    else:
        b.append(sum(a) - sum(b))
        for row in c:
            row.append(0)
        print("Добавлен фиктивный потребитель")
else:
    print("Задача закрытая")

m, n = len(a), len(b)

# Метод северо-западного угла
print("\nМетод северо-западного угла:")
supply = a.copy()
demand = b.copy()
nw_plan = [[0]*n for _ in range(m)]
i = j = 0
nw_cost = 0

while i < m and j < n:
    x = min(supply[i], demand[j])
    nw_plan[i][j] = x
    nw_cost += x * c[i][j]
    supply[i] -= x
    demand[j] -= x
    if supply[i] == 0:
        i += 1
    if demand[j] == 0:
        j += 1

print(f"Стоимость по СЗУ: {nw_cost}")

# Решение через PuLP
prob = LpProblem("transport", LpMinimize)

# Переменные
x = {}
for i in range(m):
    for j in range(n):
        x[i,j] = LpVariable(f"x{i+1}_{j+1}", lowBound=0)

# Целевая функция
prob += lpSum(c[i][j] * x[i,j] for i in range(m) for j in range(n))

# Ограничения
for i in range(m):
    prob += lpSum(x[i,j] for j in range(n)) == a[i]
for j in range(n):
    prob += lpSum(x[i,j] for i in range(m)) == b[j]

prob.solve(PULP_CBC_CMD(msg=0))

print("\nОптимальное решение:")
total_cost = 0
for i in range(m):
    for j in range(n):
        if x[i,j].varValue > 0:
            print(f"x{i+1}_{j+1} = {x[i,j].varValue}")
            total_cost += x[i,j].varValue * c[i][j]

print(f"Минимальная стоимость: {total_cost}")
