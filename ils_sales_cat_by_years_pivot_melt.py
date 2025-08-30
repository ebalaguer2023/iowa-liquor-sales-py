##Trabaja datos categóricos agrupandolos por categorías generando patrones de búsqueda guardados en un diccionario
##e invocados en un np.select(conditions, choices, default='OTHERS') donde conditions son los values() del diccionario
##y las choices son las keys.
##En función de esas agregaciones calcula el total y el promedio de ventas por año para cada categoría.
##Y muestra los datos en distintos formatos pivot/melt

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt
import re
from docx import Document
import openpyxl

##Establezco arbitratiamente un valor de código de Store, podría ser un dato solicitado al usuario vía input()
##Otro dato que se fija arbitrariamente es el año, se podría requerir también al usuario
STORE= 2583

df = pd.read_csv('C:/Users/emili/Downloads/ILS20222024.csv', quoting=3,\
                 dtype = {'Invoice Item Description': str , 'DATE': str, 'Store Name': str , 'LATITUDE': str,\
                 'LONGITUDE' : str, 'City' : str, 'Category Group': str, 'Category Name': str,\
                 'Vendor Name': str, 'Item Description' : str, 'Pack' : int, 'Bottle Volume (ml)': float,\
                 'State Bottle Cost': float, 'State Bottle Retail' : float, 'Bottles Sold' : int,\
                 'Sale (Dollars)' : float, 'Volume Sold (Liters)' : float, 'Volume Sold (Gallons)' : float},\
                 encoding='latin1')
##Se puede probar esto también type={"Bottles Sold": "float64"}

df['DATE'] = pd.to_datetime(df['DATE'], errors='coerce')
df['YEAR'] = df['DATE'].dt.year


##YEAR = 2013
##df = df[df['YEAR'] == YEAR]


# Compilar patrones de búsqueda (para mayor eficiencia)
patterns = {
    'WHISKEY': re.compile(r'BOURBON|SCOTCH|JIM BEAM|WHISK|YR|RYE|MALT|JAMESON', re.IGNORECASE),
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

# Crear una lista de condiciones y las categorías correspondientes
conditions = [df['Category Name'].str.contains(pattern) for pattern in patterns.values()]
choices = list(patterns.keys())

# Asignar categorías con numpy.select() (MUCHO MÁS RÁPIDO que múltiples loc[])
df['cat'] = np.select(conditions, choices, default='OTHERS')


df['Bottles Sold'] = pd.to_numeric(df['Bottles Sold'], errors='coerce')
##df = df.dropna(subset=['Bottles Sold'])
print('fILAS DONDE BOTTLES SOLD ES NA \n',df[df['Bottles Sold'].isna()])
dfna = df[df['Bottles Sold'].isna()]

dfna.to_csv('C:/Users/emili/Downloads/dfna.csv')


cat = df.groupby('cat')['Bottles Sold'].sum().reset_index()
print(cat.columns)  


cat = cat.set_index('cat')   

cat['Bottles Sold - MEAN'] = df.groupby('cat')['Bottles Sold'].mean()

cat=cat.sort_values('Bottles Sold',ascending=False)
print(cat)


ilspivot = pd.pivot_table(df, index = 'YEAR', columns = 'cat', values = 'Bottles Sold', aggfunc = ['sum','mean'])

with pd.ExcelWriter('C:/Users/emili/Downloads/tablasils2024.xlsx', engine='openpyxl', mode = 'w') as writer:
    ilspivot.to_excel(writer, sheet_name='Sales_Resume')


ilspivot_reset = ilspivot.copy().reset_index()
ilspivot_reset.columns = ['YEAR'] + [f"{agg}_{cat}" for agg, cat in ilspivot_reset.columns[1:]]

# Verificar las nuevas columnas
print("Nuevas columnas después de reset_index():", ilspivot_reset.columns)

# Aplicar melt para estructurar la tabla correctamente
ilspivot_melted = ilspivot_reset.melt(id_vars=['YEAR'], var_name='Metric', value_name='Value')
print('ilspivot_melted - paso 1')
print(ilspivot_melted)

# Separar 'Metric' en dos columnas: 'Aggregation' y 'cat'
ilspivot_melted[['Aggregation', 'cat']] = ilspivot_melted['Metric'].str.split('_', expand=True)

# Eliminar la columna auxiliar 'Metric'
ilspivot_melted = ilspivot_melted.drop(columns=['Metric'])

print('ilspivot_melted - paso 2')
print(ilspivot_melted)



# Pivotear para tener columnas 'SUM' y 'MEAN'
ilspivot_final = ilspivot_melted.pivot(index=['YEAR', 'cat'], columns='Aggregation', values='Value').reset_index()

# Renombrar las columnas correctamente
ilspivot_final.columns.name = None  # Eliminar el nombre de las columnas
ilspivot_final = ilspivot_final.rename(columns={'sum': 'SUM', 'mean': 'MEAN'})

with pd.ExcelWriter('C:/Users/emili/Downloads/tablasils2024.xlsx', engine='openpyxl', mode = 'a') as writer:
    ilspivot_final.to_excel(writer, sheet_name='Sales_Resume_Long')


unstack = ilspivot.unstack()


with pd.ExcelWriter('C:/Users/emili/Downloads/tablasils2024.xlsx', engine='openpyxl', mode = 'a') as writer:
    unstack.to_excel(writer, sheet_name='Sales_Resume_Unstack')

YEAR = 2015
df = df[df['YEAR'] == YEAR]

print(YEAR)
print(df.groupby('cat')['Bottles Sold'].value_counts())
print(df.groupby('cat')['Bottles Sold'].sum())


dfselect = df.iloc[166]
print(dfselect)


dfselect = df.iloc[537]
print(dfselect)


dfselect = df.iloc[843]
print(dfselect)

print(df['DATE'].count())


















