import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re

# Load DataFrame
df = pd.read_csv('ils2015_2024.csv', parse_dates=['Date'], delimiter=",", 
                 on_bad_lines='skip', encoding='utf-8', low_memory=False)
df['YEAR'] = df['Date'].dt.year
df=df[df['YEAR']>=2015]

## Show information of data types and missing values on this DataFrame
print(df.info())
output =  pd.DataFrame(df.info())
print(output)
with pd.ExcelWriter('C:/Users/emili/Dropbox/PROGRAMACION/PYTHON/Prácticas/ILS/ILS_DESCRIBE.xlsx', engine='openpyxl', mode='w') as writer:
     output.to_excel(writer, sheet_name='Info')
print('\n')


### Creating category groups from the 'Category Name'
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


conditions = [df['Category Name'].str.contains(pattern) for pattern in patterns.values()]
choices = list(patterns.keys())

##
df['Category Group'] = np.select(conditions, choices, default='OTHERS')
df['Category Group'] = df['Category Group'].astype('category')
print('\n')
print('\n')
print('Size of "Category Group" as category type:', df['Category Group'].nbytes)

# Casting numeric types 
num_cols = ["Bottles Sold", "Volume Sold (Liters)", "Sale (Dollars)"]
for col in num_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')  # Convert errors to NaN


## Display summary statistics
print(df[['Bottles Sold','Sale (Dollars)','Volume Sold (Liters)']].describe())
print('\n')
output =  pd.DataFrame(df.describe())
print('\n')
with pd.ExcelWriter('C:/Users/emili/Dropbox/PROGRAMACION/PYTHON/Prácticas/ILS/ILS_DESCRIBE.xlsx', engine='openpyxl', mode='a') as writer:
     output.to_excel(writer, sheet_name='EDA - Describe')
print('\n')
## Show bottles sold per category
print(df.groupby('Category Group')['Bottles Sold'].sum())
print('\n')
print('\n')
print('\n')


cat = df.groupby(['Category Group','YEAR'])['Bottles Sold'].sum()

print(cat)

catresetindex = cat.reset_index()
maxbottles = catresetindex['Bottles Sold'].max()

listcat = catresetindex['Category Group'].unique()

for category in listcat:
    selection = catresetindex[catresetindex['Category Group'] == category]
    selection.plot.line(x='YEAR', y='Bottles Sold')
    plt.title(f'Bottles sold over the years - Category: {category}')
    plt.show()    


####identifying outliers
q1=df['Bottles Sold'].quantile(0.25)
q3=df['Bottles Sold'].quantile(0.75)
iqr = q3-q1
lower = q1+1.5 * iqr
upper = q3+1.5 * iqr




### 'Bottles Sold' first histogram (with data as it comes)
df['Bottles Sold'].hist(bins=50)
plt.xlabel("Bottles Sold")
plt.ylabel("Frequency")
plt.title("Distribution of Bottles Sold without removing outliers")
plt.show()


### 'Volume Sold (Liters)' boxplot by categories
g = sns.catplot (x='Category Group', y = 'Volume Sold (Liters)', kind = 'box', data =df)
plt.xticks(rotation=45)
plt.title('Volume Sold (Liters) without removing outliers', y=1.1)
plt.show()


##Removing outliers
outliers=df[(df['Bottles Sold'] < lower) &  (df['Bottles Sold'] > upper)]['Bottles Sold']

print('outliers:', outliers)
print('\n')
print('\n')
print('\n')

dforiginal = df
df = df[(df['Bottles Sold'] > lower) &  (df['Bottles Sold'] < upper)]

print(df[['Bottles Sold','Sale (Dollars)','Volume Sold (Liters)']].sum())

### Display descriptive statistics after removing outliers
print(df[['Bottles Sold','Sale (Dollars)','Volume Sold (Liters)']].describe())
output =  pd.DataFrame(df.describe())
print('\n')
with pd.ExcelWriter('C:/Users/emili/Dropbox/PROGRAMACION/PYTHON/Prácticas/ILS/ILS_DESCRIBE.xlsx', engine='openpyxl', mode='a') as writer:
     output.to_excel(writer, sheet_name='Describe without outliers')


### Histograma de 'Bottles Sold'
df['Bottles Sold'].hist(bins=50)
plt.xlabel("Bottles Sold")
plt.ylabel("Frequency (Millions)")
plt.title("Distribution of Bottles Sold")
plt.show()


### 'Bottles Sold' histogram xscale log
df['Bottles Sold'].hist(bins=50)
plt.xscale('log')
plt.xlabel("Bottles Sold")
plt.ylabel("Frequency (Millions)")
plt.title("Distribution of Bottles Sold 2015-2024")
plt.show()


### 'Volume Sold (Liters)' histogram 
df['Volume Sold (Liters)'].hist(bins=50)
plt.xlabel("Volume Sold (Liters)")
plt.ylabel("Frequency (Millions)")
plt.title("Distribution of Volume Sold in Liters 2015-2024")
plt.show()

### 'Volume Sold (Liters)' histogram xscale log
df['Volume Sold (Liters)'].hist(bins=50)
plt.xscale('log')
plt.xlabel("Volume Sold (Liters)")
plt.ylabel("Frequency (Millions)")
plt.title("Distribution of Volume Sold in Liters 2015-2024")
plt.show()

df['vl-log'] = np.log(df['Volume Sold (Liters)'])
from statsmodels.graphics.gofplots import qqplot
### Plot the qq plot of the chickens' weight
qqplot(data=df['vl-log'], line='s')
plt.show()



# 'Volume Sold (Liters)' boxplot by categories
g = sns.catplot (x='Category Group', y = 'Volume Sold (Liters)', kind = 'box', data =df)
plt.title("Distribution of Volume Sold in Liters 2015-2024", y=1.1)
plt.xticks(rotation=45) 
plt.show()

# 'Volume Sold (Liters)' boxplot by categories
g = sns.violinplot (x='Category Group', y = 'Volume Sold (Liters)', data =df)
plt.title("Distribution of Volume Sold in Liters 2015-2024")
plt.xticks(rotation=45) 
plt.show()
