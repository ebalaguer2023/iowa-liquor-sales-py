import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt
import os
import re
import openpyxl

def load_data(filepath):
    df = pd.read_csv(filepath, quoting=3, encoding='latin1')
    df['DATE'] = pd.to_datetime(df['DATE'], errors='coerce')
    df['YEAR'] = df['DATE'].dt.year
    df['Bottles Sold'] = df['Bottles Sold'].fillna(0).astype(int)
    df['City'] = df['City'].fillna('-')
    df = df[df['YEAR'] >= 2015]
    return df

def get_top_vendors(df, top_n=10):
    df10 = df.groupby('Vendor Name')['Bottles Sold'].sum().sort_values(ascending=False).reset_index()
    return df10['Vendor Name'].head(top_n)

def get_selection(options, column_name):
    options = options.reset_index().rename(columns={0: column_name})
    options.sort_values(column_name, inplace=True)
    options.reset_index(drop=True, inplace=True)
    print(options)
    max_value = options.shape[0]
    
    while True:
        try:
            selected = int(input(f'Select a {column_name} code: '))
            if 0 <= selected < max_value:
                return options.iloc[selected, 1]
            else:
                print("Invalid selection. Try again.")
        except ValueError:
            print("Please enter a valid number.")

def clean_filename_part(name):
    """Limpia los nombres para que sean válidos en nombres de archivo de Windows."""
    name = name.strip()
    return re.sub(r'[\\/*?:"<>|]', '_', name)

def plot_top_items(df, vendor, store, city, year):
    safe_vendor = clean_filename_part(vendor)
    safe_store = clean_filename_part(store)
    export_dir = os.path.join("C:/Users/emili/Downloads", f"Sales_of_{safe_vendor}_at_{safe_store}")
    os.makedirs(export_dir, exist_ok=True)

    # Gráfico 1: Top 10 productos
    dfstore = df.groupby('Item Description')['Bottles Sold'].sum().sort_values(ascending=False).reset_index()
    dfbar = dfstore.head(10)
    plt.figure(figsize=(10,5))
    plt.bar(dfbar['Item Description'], dfbar['Bottles Sold'])
    plt.xticks(rotation=45, ha='right')
    plt.title(f'Bottles of {vendor} sold at {store}, {city} ({year})')
    plt.tight_layout()
    plot_path1 = os.path.join(export_dir, f"{safe_vendor}_at_{safe_store}_top_items.png")
    plt.savefig(plot_path1)
    plt.close()
    print(f"Gráfico de top items guardado en: {plot_path1}")

    # Gráfico 2: Ventas por año
    dftemp = df.groupby('YEAR')['Bottles Sold'].sum().reset_index()
    plt.figure(figsize=(8,5))
    plt.plot(dftemp['YEAR'], dftemp['Bottles Sold'], marker='o')
    plt.title(f'Ventas por año - {vendor} en {store}')
    plt.xlabel('Año')
    plt.ylabel('Botellas vendidas')
    plt.grid(True)
    plt.tight_layout()
    plot_path2 = os.path.join(export_dir, f"{safe_vendor}_at_{safe_store}_sales_by_year.png")
    plt.savefig(plot_path2)
    plt.close()
    print(f"Gráfico por año guardado en: {plot_path2}")

    # Gráfico 3: Ventas por grupo de categoría
    if 'Category Group' in df.columns:
        dfcat = df.groupby('Category Group')['Bottles Sold'].sum().sort_values(ascending=False).reset_index()
        plt.figure(figsize=(10,5))
        sns.barplot(data=dfcat, x='Category Group', y='Bottles Sold', palette='muted')
        plt.xticks(rotation=45, ha='right')
        plt.title(f'Ventas por categoría - {vendor} en {store}')
        plt.tight_layout()
        plot_path3 = os.path.join(export_dir, f"{safe_vendor}_at_{safe_store}_sales_by_category.png")
        plt.savefig(plot_path3)
        plt.close()
        print(f"Gráfico por categoría guardado en: {plot_path3}")
    else:
        print("⚠️ La columna 'Category Group' no está presente en el DataFrame.")

def export_sales_data(df, vendor, store):
    safe_vendor = clean_filename_part(vendor)
    safe_store = clean_filename_part(store)
    export_dir = os.path.join("C:/Users/emili/Downloads", f"Sales_of_{safe_vendor}_at_{safe_store}")
    os.makedirs(export_dir, exist_ok=True)

    pivot_table = pd.pivot_table(df, index='YEAR', columns='Item Description', values='Bottles Sold', aggfunc=['sum', 'mean'])

    filepath = os.path.join(export_dir, f"{safe_vendor}_at_{safe_store}.xlsx")
    with pd.ExcelWriter(filepath, engine='openpyxl', mode='w') as writer:
        pivot_table.to_excel(writer, sheet_name='Sales_Resume')
    print(f"Archivo Excel guardado en: {filepath}")

if __name__ == "__main__":
    df = load_data('ILS20222024.csv')
    print('List top 10 Vendors:\n', get_top_vendors(df))
    
    vendor = get_selection(pd.DataFrame(df['Vendor Name'].unique()), 'Vendor Name')
    city = get_selection(pd.DataFrame(df[df['Vendor Name'] == vendor]['City'].unique()), 'City')
    store = get_selection(pd.DataFrame(df[(df['Vendor Name'] == vendor) & (df['City'] == city)]['Store Name'].unique()), 'Store')

    df_filtered = df[(df['Vendor Name'] == vendor) & (df['City'] == city) & (df['Store Name'] == store)]
    print(df_filtered.groupby('Item Description')['Bottles Sold'].sum().sort_values(ascending=False).head(10))

    plot_top_items(df_filtered, vendor, store, city, 2024)
    export_sales_data(df_filtered, vendor, store)
