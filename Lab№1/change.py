import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Исходные данные
data = {
    'Car': ['Audi A6 C6', 'Mini Cooper 2.0', 'Toyota Chaser 2.5'],
    'price': [800000, 1000000, 1400000],
    'visual': [6, 7, 9],
    'reliability': [7, 9, 7],
    'fuel_consumption': [11, 7, 10]
}

df = pd.DataFrame(data)
print("Исходные данные:")
print(df)

weights = [0.4, 0.3, 0.2, 0.1]
print(f"\nВеса критериев: [Price: {weights[0]}, Visual: {weights[1]}, Reliability: {weights[2]}, Fuel: {weights[3]}]")

# Создаем копию DataFrame для нормализованных данных
df_norm = df.copy()

# Нормализация для критерия к минимизации (цена)
df_norm['price_norm'] = (df['price'].max() - df['price']) / (df['price'].max() - df['price'].min())

# Нормализация для критерия к максимизации (визуал)
df_norm['visual_norm'] = (df['visual'] - df['visual'].min()) / (df['visual'].max() - df['visual'].min())

# Нормализация для критерия к максимизации (надежность)
df_norm['reliability_norm'] = (df['reliability'] - df['reliability'].min()) / (df['reliability'].max() - df['reliability'].min())

# Нормализация для критерия к минимизации (расход)
df_norm['fuel_norm'] = (df['fuel_consumption'].max() - df['fuel_consumption']) / (df['fuel_consumption'].max() - df['fuel_consumption'].min())

# Выводим таблицу с нормализованными значениями (по шкале от 0 до 1)
print("\nНормализованные данные (по шкале от 0 до 1):")
print(df_norm[['Car', 'price_norm', 'visual_norm', 'reliability_norm', 'fuel_norm']])


df_norm['total_score'] = (df_norm['price_norm'] * weights[0] +
                         df_norm['visual_norm'] * weights[1] +
                         df_norm['reliability_norm'] * weights[2] +
                         df_norm['fuel_norm'] * weights[3])


print("\nИтоговая таблица с интегральными оценками:")
print(df_norm[['Car', 'price_norm', 'visual_norm', 'reliability_norm', 'fuel_norm', 'total_score']])


plt.figure(figsize=(10, 6))
cars = df_norm['Car']
scores = df_norm['total_score']

colors = ['red', 'blue', 'green']

plt.bar(cars, scores, color=colors)
plt.title('Результаты многокритериального анализа')
plt.ylabel('Интегральная оценка')
plt.show()
