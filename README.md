# iowa-liquor-sales-py
Data analysis of the Iowa Liquor Sales from a python approach. The data worked on this project it's the [Iowa Liquor Sales dataset] (https://data.iowa.gov/Sales-Distribution/Iowa-Liquor-Sales/m3tr-qhgy/about_data)

This approach includes the previous ETL tasks; a summary statistics of the dataset and an overview of the data distribution in order to understand how the data are spread so we can later choose the appropiate test (parametric or non parametric depending on the result of this analysis). This summary and Exploratory Data Analysis it's on ils_describe.py


We also have distinct codes that returns:
a) An analysis of the sales over time, with a lineplot: ilstime.py
b) Summary of sales per category by year, proving different modes of display (wide and long formats): ils_sales_cat_by_years_pivot_melt.py
c) An interface to obtain the sales of a certain vendor in an specific store. This interface ask the user to choose the vendor, the city and the store. The results includes a series of plots: stores.py
