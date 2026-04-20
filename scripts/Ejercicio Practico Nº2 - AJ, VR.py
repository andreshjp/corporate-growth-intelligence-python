# Ejercicio Práctico Nº2
# Andrés Jiménez C.I. 29.686.525
# Vanessa Rendón C.I. 30.309.567

# Te queremos gabito <3 

# Activamos el paquete pandas para poder trabajar con DataFrames de csv y otros paquetes para poder graficar
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import squarify
import country_converter as coco

# Definimos los colores a utilizar en los gráficos
custom_palette = sns.color_palette(["#0c5254", "#1b6265", "#2a7376", "#398487", "#499598", "#59a6a9", "#69b7ba", "#79c8cb", "#89d9dc","#b3c4db"])
base_color = "#0c5254"

# Importamos el archivo companies.csv
data = pd.read_csv('companies.csv')

# Aquí podemos ver las primeras filas del DataFrame
pd.set_option('display.max_rows', None)
print(data.head())

#Revisamos que todos los paises esten escritos de la misma manera
print(data['Company Origin'].unique())
# Reemplazamos 'USA' con 'United States'
data['Company Origin'] = data['Company Origin'].replace('USA', 'United States')

# Primero veremos unos datos que podrían sser relevantes para entender la data
# El número total de compañías
companies = data['Company'].count()
print(f"El número total de compañías en la data es {companies}")
# El número total de países
countries = data['Company Origin'].nunique()
print(f"El número total de países en la data es {countries}")

# 1. ¿Cuál es el promedio del Price to Book Ratio de las empresas en el dataset?
avg_pb_ratio = data['price to book ratio'].mean()
print(f"El Price to Book Ratio promedio es {avg_pb_ratio}")

# 1.1 Grafico de barras con top 10 y bottom 10 del Price to Book Ratio promedio por país
mean_PB_per_country = data.groupby('Company Origin')['price to book ratio'].mean().to_frame('Mean Price to Book Ratio')
top_10_countries_PB = mean_PB_per_country.nlargest(10, 'Mean Price to Book Ratio')
bottom_10_countries_PB = mean_PB_per_country.nsmallest(10, 'Mean Price to Book Ratio')

# Top 10 paises
plt.figure(figsize=(14, 8))
sns.barplot(x=top_10_countries_PB.index, y='Mean Price to Book Ratio', data=top_10_countries_PB, palette=custom_palette)
plt.title('Top 10 Países con el Mayor Price to Book Ratio Promedio')
plt.xlabel('País')
plt.ylabel('Promedio Price to Book Ratio')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('top_10_countries_PB.png')
plt.show()

# Bottom 10 paises
plt.figure(figsize=(14, 8))
sns.barplot(x=bottom_10_countries_PB.index, y='Mean Price to Book Ratio', data=bottom_10_countries_PB, palette=custom_palette)
plt.axhline(0, color='black', linewidth=0.8)
plt.title('Bottom 10 Países con el Menor Price to Book Ratio Promedio')
plt.xlabel('País')
plt.ylabel('Promedio Price to Book Ratio')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('bottom_10_countries_PB.png')
plt.show()

# 2. ¿Cuál es el precio promedio de las acciones (Share Price) en el dataset?
avg_share_price = data['share price (USD)'].mean()
print(f"El precio promedio de las acciones es de {avg_share_price} USD")

# 3. ¿Cuántas empresas hay en cada país?
companies_per_country = data['Company Origin'].value_counts()
print(companies_per_country)

# 3.1 Treemap con la distribución de empresas por país
data['Alpha-3 Code'] = coco.convert(names=data['Company Origin'].tolist(), to='ISO3')
companies_per_country_alpha3 = data['Alpha-3 Code'].value_counts()
threshold = 20
filtered_companies_per_country_alpha3 = companies_per_country_alpha3[companies_per_country_alpha3 >= threshold]
total_companies = companies_per_country_alpha3.sum()
percentages = (companies_per_country_alpha3 / total_companies) * 100
labels = [f'{country}\n({percentage:.1f}%)' if count >= threshold and percentage >= 0.5 else country if count >= threshold else '' 
          for country, count, percentage in zip(companies_per_country_alpha3.index, 
                                                companies_per_country_alpha3.values, 
                                                percentages.values)]
colors = sns.light_palette(base_color, len(companies_per_country_alpha3))[::-1]
plt.figure(figsize=(12, 8))
squarify.plot(sizes=companies_per_country_alpha3, 
               label=labels, 
               color=colors, 
               alpha=.8)
plt.title('Cantidad de Empresas por País (Porcentaje)')
plt.axis('off')
plt.savefig('companies_per_country.png')
plt.show()

# 3.2 El top 5 de países con más empresas (para una mejor visualización)
top_countries = companies_per_country.nlargest(5)
print(f"Los 5 países con más empresas son: {top_countries}")

# 4. ¿Cuál es la empresa con el menor Price to Book Ratio?
min_pb_ratio = data['price to book ratio'].min()
min_pb_ratio_company = data.loc[data['price to book ratio'].idxmin(), 'Company']
print(f"La empresa con el menor Price to Book Ratio es {min_pb_ratio_company}, con un valor de {min_pb_ratio}")

# 5. ¿Cuál es la empresa con el mayor Share Price?
max_share_price = data['share price (USD)'].max()
max_share_price_company = data.loc[data['share price (USD)'].idxmax(), 'Company']
print(f"La empresa con el mayor Share Price es {max_share_price_company}, con un valor de {max_share_price} USD")

# 6. ¿Cuál es el rango de Price to Book Ratio para las empresas estadounidenses?
us_companies = data[data['Company Origin'] == 'United States']
us_min_PB = us_companies['price to book ratio'].min()
us_max_PB = us_companies['price to book ratio'].max()
us_pb_ratio_range = us_max_PB - us_min_PB 
print(f"El mayor Price to Book Ratio para empresas estadounidenses es {us_max_PB}, mientras que el menor es {us_min_PB}. Por lo tanto el rango del Price to Book Ratio de las empresas estadounidenses es de {us_pb_ratio_range}")

# 6.1 Promedio de Price to Book Ratio de las empresas de Estados Unidos
avg_pb_ratio_us = us_companies['price to book ratio'].mean()
print(f"El Price to Book Ratio promedio de las empresas de Estados Unidos es {avg_pb_ratio_us}")

# 6.2 Promedio de Share Price de las empresas de Estados Unidos
avg_share_price_us = us_companies['share price (USD)'].mean()
print(f"El precio promedio de las acciones de las empresas de Estados Unidos es {avg_share_price_us} USD")

# 7. ¿Cuál es el promedio del Share Price por país?
avg_share_price_by_country = data.groupby('Company Origin')['share price (USD)'].mean().to_frame('Mean Share Price per Country')
print(avg_share_price_by_country)

# 7.1 Grafico de barras con top 10 y bottom 10 del Share Price promedio por país
mean_share_price_per_country = data.groupby('Company Origin')['share price (USD)'].mean().to_frame('Mean Share Price')
top_10_countries_share_price = mean_share_price_per_country.nlargest(10, 'Mean Share Price')
bottom_10_countries_share_price = mean_share_price_per_country.nsmallest(10, 'Mean Share Price')

# Top 10 paises
plt.figure(figsize=(14, 8))
sns.barplot(x=top_10_countries_share_price.index, y='Mean Share Price', data=top_10_countries_share_price, palette=custom_palette)
plt.title('Top 10 Países con el Precio Promedio de Acciones Más Alto')
plt.xlabel('País')
plt.ylabel('Precio Promedio de Acciones (USD)')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('top_10_countries_SP.png')
plt.show()

# Promedio Share Price de Kuwait
avg_share_price_kuwait = mean_share_price_per_country.loc['Kuwait', 'Mean Share Price']
print(f"El precio promedio de las acciones en Kuwait es de {avg_share_price_kuwait} USD")
# Número de empresas en Kuwait
companies_kuwait = companies_per_country.loc['Kuwait']
print(f"El número de empresas en Kuwait es de {companies_kuwait}")

# Promedio Share Price de Suiza
avg_share_price_switzerland = mean_share_price_per_country.loc['Switzerland', 'Mean Share Price']
print(f"El precio promedio de las acciones en Suiza es de {avg_share_price_switzerland} USD")
# Número de empresas en Suiza
companies_switzerland = companies_per_country.loc['Switzerland']
print(f"El número de empresas en Suiza es de {companies_switzerland}")

# Bottom 10 paises
plt.figure(figsize=(14, 8))
sns.barplot(x=bottom_10_countries_share_price.index, y='Mean Share Price', data=bottom_10_countries_share_price, palette=custom_palette)
plt.title('Bottom 10 Países con el Precio Promedio de Acciones Más Bajo')
plt.xlabel('País')
plt.ylabel('Precio Promedio de Acciones (USD)')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('bottom_10_countries_SP.png')
plt.show()

# 8. ¿Cuál es la empresa mejor clasificada (Rank 1)?
top_ranked_company = data.loc[data['Rank'] == 1, ['Company', 'stock Symbol', 'price to book ratio', 'share price (USD)', 'Company Origin']].iloc[0]
print(f"La empresa mejor clasificada (Rank 1) es {top_ranked_company['Company']}, cuyo símbolo de stock es {top_ranked_company['stock Symbol']}, su PB ratio es {top_ranked_company['price to book ratio']}, el precio de su acción es {top_ranked_company['share price (USD)']} USD y proviene de {top_ranked_company['Company Origin']}")

# 9. ¿Cuántas empresas tienen un Price to Book Ratio mayor que 1?
companies_pb_ratio_gt_1 = data[data['price to book ratio'] > 1].shape[0]
print(f"{companies_pb_ratio_gt_1} empresas tienen un Price to Book Ratio mayor que 1")

# 10. ¿Cuál es el precio promedio de las acciones para las empresas con un Price to Book Ratio menor que 1?
avg_share_price_pb_ratio_lt_1 = data[data['price to book ratio'] < 1]['share price (USD)'].mean()
print(f"El precio promedio de las acciones para empresas con Price to Book Ratio menor que 1 es {avg_share_price_pb_ratio_lt_1} USD")

# 11. ¿Cuál es el país con el Share Price promedio más alto?
country_avg_share_price = data.groupby('Company Origin')['share price (USD)'].mean()
country_avg_share_price_max = country_avg_share_price.idxmax()
country_avg_share_price_value = country_avg_share_price.max()
print(f"El país con el Share Price promedio más alto es {country_avg_share_price_max}, con un valor de {country_avg_share_price_value} USD")

# 12. ¿Cuál es la empresa con el mayor Label Count?
pb_ratio_bins = data['price to book ratio'].quantile([0, 0.15, 0.30, 0.45, 0.60, 0.75, 0.90, 1]).tolist()
share_price_bins = data['share price (USD)'].quantile([0, 0.15, 0.30, 0.45, 0.60, 0.75, 0.90, 1]).tolist()
pb_ratio_labels = [f'{pb_ratio_bins[i]:.2f}-{pb_ratio_bins[i+1]:.2f}' for i in range(len(pb_ratio_bins)-1)]
share_price_labels = [f'{share_price_bins[i]:.2f}-{share_price_bins[i+1]:.2f}' for i in range(len(share_price_bins)-1)]
data['PB Ratio Range'] = pd.cut(data['price to book ratio'], bins=pb_ratio_bins, labels=pb_ratio_labels, include_lowest=True)
data['Share Price Range'] = pd.cut(data['share price (USD)'], bins=share_price_bins, labels=share_price_labels, include_lowest=True)
label_count = data.groupby(['PB Ratio Range', 'Share Price Range']).size().unstack(fill_value=0)
print(label_count)

# 12.1 Heatmap de la tabla de Label Count
plt.figure(figsize=(12, 8))
sns.heatmap(label_count, annot=True, fmt='d', cmap=sns.light_palette(base_color, as_cmap=True))
plt.title('Mapa de calor de Label Count')
plt.xlabel('Rango de Precio de Acciones (USD)')
plt.ylabel('Rango de Price to Book Ratio')
plt.tight_layout()
plt.savefig('label_count_heatmap.png')
plt.show()

# 13. Cualquier otro hallazgo valioso será bien recibido por el cliente. 

# Correlación entre Price to Book Ratio y Share Price
correlation = data['price to book ratio'].corr(data['share price (USD)'])
print(f"La correlación entre el Price to Book Ratio y el Share Price es: {correlation:.6f}")
# Grafico de correlación entre Price to Book Ratio y Share Price
plt.figure(figsize=(10, 6))
sns.scatterplot(x='price to book ratio', y='share price (USD)', data=data, color=base_color)
plt.title('Relación entre Price to Book Ratio y Share Price')
plt.xlabel('Price to Book Ratio')
plt.ylabel('Precio de la Acción (USD)')
plt.savefig('correlation_PB_SP.png')
plt.show()

# Empresas poco favorables para invertir
#   Empresas con Price to Book Ratio negativo 
negative_pb_ratio = data[data['price to book ratio'] < 0].shape[0]
print(f"{negative_pb_ratio} empresas tienen un Price to Book Ratio negativo")

#   Empresas con Price to Book Ratio negativo por país
negative_pb_ratio_per_country = data[data['price to book ratio'] < 0]['Company Origin'].value_counts()
print(negative_pb_ratio_per_country)

#   Peso de empresas con Price to Book Ratio negativo por país
negative_pb_ratio_per_country = negative_pb_ratio_per_country.reindex(companies_per_country.index, fill_value=0)
percentage_negative_pb_ratio_per_country = (negative_pb_ratio_per_country / companies_per_country ) * 100
print(percentage_negative_pb_ratio_per_country)

# Empresas correctamente valoradas y favorables para invertir
#   Empresas con Price to Book Ratio entre 1 y 3
pb_ratio_between_1_and_3 = data[(data['price to book ratio'] >= 1) & (data['price to book ratio'] <= 3)].shape[0]
print(f"{pb_ratio_between_1_and_3} empresas tienen un Price to Book Ratio entre 1 y 3")

#   Empresas con Price to Book Ratio entre 1 y 3 por país
pb_ratio_between_1_and_3_per_country = data[(data['price to book ratio'] >= 1) & (data['price to book ratio'] <= 3)].groupby('Company Origin')['Company'].count()
print(pb_ratio_between_1_and_3_per_country)

#   Peso de empresas con Price to Book Ratio correctamente valorado por país
pb_ratio_between_1_and_3_per_country = pb_ratio_between_1_and_3_per_country.reindex(companies_per_country.index, fill_value=0)
percentage_pb_ratio_between_1_and_3_per_country = (pb_ratio_between_1_and_3_per_country  / companies_per_country ) * 100
print(percentage_pb_ratio_between_1_and_3_per_country)

# Empresas sobrevaloradas
#   Empresas con Price to Book Ratio mayor a 3 
pb_ratio_greater_3 = data[data['price to book ratio'] > 3].shape[0]
print(f"{pb_ratio_greater_3} empresas tienen un Price to Book Ratio mayor a 3")

#   Empresas con Price to Book Ratio mayor a 3 por país
pb_ratio_greater_3_per_country = data[data['price to book ratio'] > 3].groupby('Company Origin')['Company'].count()
print(pb_ratio_greater_3_per_country)

#   Peso de empresas con Price to Book Ratio sobrevalorado por país
pb_ratio_greater_3_per_country = pb_ratio_greater_3_per_country.reindex(companies_per_country.index, fill_value=0)
percentage_pb_ratio_greater_3_per_country = (pb_ratio_greater_3_per_country / companies_per_country ) * 100
print(percentage_pb_ratio_greater_3_per_country)