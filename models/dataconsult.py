import pandas as pd
import pyodbc
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.seasonal import seasonal_decompose

#Extrayendo variable a analizar desde base de datos de Yunque
def plotData():
    imae = 710 #id en base de datos de Yunque
    conn = pyodbc.connect(driver='{ODBC Driver 17 for SQL Server}', 
                        server='servidor-yunque-capital.database.windows.net', 
                        database='YunqueDB', 
                        uid='servidor-yunque-capital', 
                        pwd='Baseyun123')
    c= conn.cursor()
    query = "select Fecha,Valor from datos where Variable_ID =" + str(imae)
    df = pd.read_sql(query,conn)
    df["Fecha"]=pd.to_datetime(df['Fecha'], utc=True)
    df = df.set_index("Fecha")
    return df