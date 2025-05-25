##Este lee archivos de las ventas separados por año y los reune en un df con pd.concat

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re

def readcsv(year):
    varyear = str(year)
    df = pd.read_csv(f'C:/Users/emili/Downloads/ils{varyear}.csv', delimiter=",", on_bad_lines='skip', encoding='utf-8')

    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df['YEAR'] = df['Date'].dt.year

    patterns = {
        'WHISKEY': re.compile(r'SCOTCH|JIM BEAM|WHISK|YR|RYE|MALT|JAMESON', re.IGNORECASE),
        'COCKTAIL': re.compile(r'MARGARITA|COLADA|COCKTAIL', re.IGNORECASE),
        'RUM': re.compile(r'RUM', re.IGNORECASE),
        'BRANDY': re.compile(r'BRANDIE', re.IGNORECASE),
        'TEQUILA': re.compile(r'TEQUILA', re.IGNORECASE),
        'SCHNAPPS': re.compile(r'SCHNAPPS', re.IGNORECASE),
        'LIQUEUR': re.compile(r'LIQUEUR', re.IGNORECASE),
        'VODKA': re.compile(r'VODKA', re.IGNORECASE),
        'GIN': re.compile(r'GIN', re.IGNORECASE)
    }

    df['Category Name'] = df['Category Name'].fillna('')

    conditions = [df['Category Name'].str.contains(pattern) for pattern in patterns.values()]
    choices = list(patterns.keys())

    df['cat'] = np.select(conditions, choices, default='OTHERS')

    return df

# Inicializar DataFrame vacío
dfcat = pd.DataFrame()

# Leer datos desde 2015 hasta 2024
for year in range(2015, 2025):
    df = readcsv(year)
    dfcat = pd.concat([dfcat, df], ignore_index=True)


# Crear tabla pivot con media y mediana
mean_sales_by_year = dfcat.pivot_table(values='Volume Sold (Liters)', index=['cat','YEAR'], aggfunc=[np.sum, np.mean, np.median])

print(mean_sales_by_year)


print(dfcat.iloc[5000:5051])

# Graficar


fig, axes = plt.subplots(3, 3, figsize=(18, 10))


sns.relplot(ax=axes[0, 0], kind='line', data=cat, x='YEAR', y='Volume Sold (Liters)', col='cat', aspect=2)
sns.relplot(ax=axes[0, 1], kind='line', data=cat, x='YEAR', y='Volume Sold (Liters)', col='cat', aspect=2)
sns.relplot(ax=axes[0, 2], kind='line', data=cat, x='YEAR', y='Volume Sold (Liters)', col='cat', aspect=2)
sns.relplot(ax=axes[1, 0], kind='line', data=cat, x='YEAR', y='Volume Sold (Liters)', col='cat', aspect=2)
sns.relplot(ax=axes[1, 1], kind='line', data=cat, x='YEAR', y='Volume Sold (Liters)', col='cat', aspect=2)
sns.relplot(ax=axes[1, 2], kind='line', data=cat, x='YEAR', y='Volume Sold (Liters)', col='cat', aspect=2)
sns.relplot(ax=axes[2, 0], kind='line', data=cat, x='YEAR', y='Volume Sold (Liters)', col='cat', aspect=2)
sns.relplot(ax=axes[2, 1], kind='line', data=cat, x='YEAR', y='Volume Sold (Liters)', col='cat', aspect=2)
sns.relplot(ax=axes[2, 2], kind='line', data=cat, x='YEAR', y='Volume Sold (Liters)', col='cat', aspect=2)

plt.show()
