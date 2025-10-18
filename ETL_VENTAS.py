import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FuncFormatter

#CARGAR LOS DATOS DESDE EL ARCHIVO CSV
datos=pd.read_csv("data.csv", encoding='utf-8')
print(datos.head(5))
print(datos.info())
print(datos['producto'].value_counts())
print("Datos nulos:\n",datos.isnull().sum()) #se verifica los datos faltantes
print(datos.describe()) #resumen estadistico de las columnas numericas
print("**"*50)

#TRANSFORMACIÓN: Limpiar, unificar, crear nuevas columnas
print("Iniciando el proceso de Transformación...")
#Limpiar y convertir columna de moneda a formato numerico
datos['precio']=datos['precio'].replace({r'\$':''}, regex=True).astype(float) #quito el simbolo de $ y convertir a float
print(datos['precio'].head(5)) #verifico la transformacion
datos['total']=datos['total'].replace({r'\$':''}, regex=True).astype(float) #quito el simbolo de $ y convertir a float
print(datos['total'].head(5)) #verifico la transformacion
#Cambiar el mes texto a numero
meses={'enero':1,'febrero':2,'marzo':3,'abril':4,'mayo':5,'junio':6,'julio':7,'agosto':8,'septiembre':9,'octubre':10,'noviembre':11,'diciembre':12}
datos['num_mes']=datos['mes'].map(meses) #crear nueva columna con el numero del mes
print(datos[['mes','num_mes']].head(5)) #verifico la nueva columna
#Crear columna de fecha completa, concatenando dia, num_mes y año
datos['fecha']=(datos['dia'].astype(str) + '-' +
                datos['num_mes'].astype(str) + '-' +
                datos['año'].astype(str))
print("\nVerificar: Así se ve la columna de texto antes de la conversión:")
print(datos[['año', 'mes', 'dia', 'fecha']].head())
datos['fecha']=pd.to_datetime(datos['fecha'], format='%d-%m-%Y') #convertir a formato fecha
print("\nVerificar: Así se ve la columna de fecha después de la conversión:")
print(datos['fecha'].head()) #verifico la nueva columna con el nuevo formato
print("Estandarizando la columna de 'PAÍS' y 'CATEGORÍA' ...")
datos['pais'] = datos['pais'].str.strip().str.lower()
datos['categoria'] = datos['categoria'].str.strip().str.lower()
print("**"*50)
print("Luego de limpiar columnas innecesarias...\n")
data_final=datos.drop(columns=['dia','mes','año','num_mes']) #elimino columnas innecesarias
columnas_ordenadas = [
    'fecha', 'producto', 'categoria', 'pais',
    'vendedor', 'cantidad', 'precio', 'total'
]
data_final = data_final[columnas_ordenadas]
print(data_final.head(5)) #verifico el nuevo orden de columnas
print("**"*50)
#CARGAR LOS DATOS TRANSFORMADOS A UN NUEVO ARCHIVO CSV
print("Guardando los datos transformados en un nuevo archivo CSV...")
nombre_Archivo="data_final.csv"
data_final.to_csv(nombre_Archivo, index=False, encoding='utf-8')
print(f"¡Proceso ETL finalizado! 🚀 Tus datos limpios están en '{nombre_Archivo}'.")
print("**"*50)
#ANALISIS DE LOS DATOS
#Usando funciones de numpy 
print("Analizando la data transformada...\n")
total_ventas=data_final['total'].sum()
total_ventas=np.round(total_ventas,2)
print(f'El total de ventas es: {total_ventas}')
promedio_ventas=data_final['total'].mean()
promedio_ventas=np.round(promedio_ventas,2)
print(f'El promedio de ventas es: {promedio_ventas}')
venta_max=data_final['total'].max()
print(f'La venta máxima realizada en una transacción fue de: {venta_max}')
venta_min=data_final['total'].min()
print(f'La venta mínima realizada en una transacción fue de: {venta_min}')
#analisis de la columna cantidad
cantidad_max=data_final['cantidad'].max()
print(f'La cantidad máxima vendida en una transacción fue de: {cantidad_max}')
cantidad_min=data_final['cantidad'].min()
print(f'La cantidad mínima vendida en una transacción fue de: {cantidad_min}')
total_productos_vendidos=data_final['cantidad'].sum()
print(f'El total de productos vendidos es: {total_productos_vendidos}')
print("**"*50)
#Generación de reportes
print("Gráfico para visualizar las ventas por pais:")
ventas_por_pais=data_final.groupby('pais')['total'].sum().sort_values(ascending=False)
ventas_por_pais.plot(kind='bar', color='skyblue')
plt.title('Ventas Totales por País')
plt.xlabel('País')
plt.ylabel('Ventas Totales ($)')
plt.tight_layout()
plt.savefig('ventas_por_pais.png')
plt.show()

print("Gráfico para ver la evolución de ventas a lo largo del tiempo:")
data_final['mes']=data_final['fecha'].dt.to_period('M')
ventasxmes=data_final.groupby(['mes','pais'])['total'].sum().reindex()
ventasxmes.unstack().plot(kind='line', marker='o')
plt.title('Evolución de Ventas a lo Largo del Tiempo por País')
plt.xlabel('Mes')
plt.ylabel('Ventas Totales ($)')
plt.legend(title='País')
plt.tight_layout()
plt.savefig('ventasxmes.png')
plt.show()
#usando seaborn para graficos mas avanzados
print("Gráfico de Top 10 Vendedores por Ingresos Generados:")
top_vendedores = data_final.groupby('vendedor')['total'].sum().nlargest(10).sort_values(ascending=True)

plt.figure()
ax = sns.barplot(x=top_vendedores.values, y=top_vendedores.index,hue=top_vendedores.index, palette="plasma", orient='h')
ax.set_title('Top 10 Vendedores por Ingresos Generados', fontsize=18, weight='bold', pad=20)
ax.set_xlabel('Ingresos Totales (en $)', fontsize=14)
ax.set_ylabel('Vendedor', fontsize=14)
ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f'${int(x/1000):,}K'))
plt.tight_layout()
plt.savefig('top_vendedores.png')
plt.show()





