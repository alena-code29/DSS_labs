from pulp import *
import time

print("ТРАНСПОРТНАЯ ЗАДАЧА - ВАРИАНТ 8")

demand = [200, 400, 400, 300, 500]  # потребности потребителей
supply = [200, 400, 600, 200, 200]  # запасы поставщиков 

# матрица тарифов
cost_matrix = [
    [1, 6, 9, 3, 4],  
    [3, 2, 2, 4, 5],  
    [4, 5, 4, 7, 6],  
    [1, 4, 3, 9, 8],  
    [7, 9, 7, 1, 9]   
]

print("Дано:")
print(f"Запасы поставщиков: {supply} (сумма = {sum(supply)})")
print(f"Потребности потребителей: {demand} (сумма = {sum(demand)})")

#проверка сбалансированности
total_supply = sum(supply)
total_demand = sum(demand)

if total_supply != total_demand:
    print(f"\nЗадача несбалансированная! Разница: {abs(total_supply - total_demand)}")
    if total_supply < total_demand: #нужен доп. поставщик
        supply.append(total_demand - total_supply)
        cost_matrix.append([0, 0, 0, 0, 0]) #добавление поставщика с запасом
        print("Добавлен фиктивный поставщик")
    else:
        demand.append(total_supply - total_demand)
        for row in cost_matrix:
            row.append(0)
        print("Добавлен фиктивный потребитель")

m = len(supply)
n = len(demand)

print(f"\nРазмерность задачи: {m} поставщиков × {n} потребителей")

#решение
print("Решение методом PULP")

start_time = time.time()

#создание переменных
variables = []
for i in range(m):
    for j in range(n):
        variables.append(LpVariable(f"x_{i+1}_{j+1}", lowBound=0))  

#создание задачи
problem = LpProblem("Transport_Problem", LpMinimize)

#целевая функция
cost_coeffs = []
for i in range(m):
    for j in range(n):
        cost_coeffs.append(cost_matrix[i][j]) 

problem += lpDot(cost_coeffs, variables), "Total_Cost" 

#ограничения поставщиков
for i in range(m):
    constraint_vars = variables[i*n : (i+1)*n] 
    problem += lpSum(constraint_vars) == supply[i], f"Supply_{i+1}" 

#ограничения потребителей
for j in range(n):
    constraint_vars = [variables[i*n + j] for i in range(m)]
    problem += lpSum(constraint_vars) == demand[j], f"Demand_{j+1}"

problem.solve(PULP_CBC_CMD(msg=0)) 
pulp_time = time.time() - start_time

# ВЫВОД РЕЗУЛЬТАТОВ
print("Оптимальный план перевозок:")

total_cost = 0
for variable in problem.variables():
    if variable.varValue > 0.001: 
        parts = variable.name.split('_')
        supplier = int(parts[1])  
        consumer = int(parts[2])  
        amount = variable.varValue
        cost = amount * cost_matrix[supplier-1][consumer-1] 
        total_cost += cost
        print(f"Поставщик{supplier} → Потребитель{consumer}: {amount:.1f} ед. × {cost_matrix[supplier-1][consumer-1]} = {cost:.1f}")

print(f"Минимальная стоимость: {total_cost:.1f}")
print(f"Время выполнения: {pulp_time:.4f} сек")
