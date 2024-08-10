from sqlalchemy import create_engine, Table, Column, Integer, String, Float, MetaData, inspect, text
from sqlalchemy.exc import SQLAlchemyError
import pyodbc
import pandas as pd

class DatabaseLoad():
    """
    Clase que recibe el Excel generado por la clase Scraper (con los datos extraídos de ML) 
    y los carga en la tabla 'Productos' de la base de datos local MSSQL 'PythonScrapedData'
    (si la tabla no existe la crea, y si existe la trunca para cargar nuevos datos)
    """
    def __init__(self) -> None:
        """ Constructor que inicializa los atributos de clase necesarios para realizar la conexión a la Base de Datos MSSQL 'PythonScrapedData' """
        self.server = r"SMS\SQLEXPRESS2"
        self.database = r"PythonScrapedData"
        self.driver = "ODBC Driver 17 for SQL Server"
        
        # crea la cadena de conexión
        self.connection_string = f"mssql+pyodbc://{self.server}/{self.database}?driver={self.driver}"
        self.engine = create_engine(self.connection_string)
        
        # diccionario de renombres de columnas
        self.column_mapping = {
            # "Unnamed: 0": "ProductID",
            "product": "Nombre",
            "price": "Precio",
            "link": "URL"
            }
        return None
    
    def create_table_if_not_exists(self) -> None:
        """ crea tabla Productos en la base de datos SQL Server 'PythonScrapedData', en caso de existir, la trunca """
        metadata = MetaData()
        inspector = inspect(self.engine)

        productos = Table(
                "Productos", metadata,
                Column("Nombre", String(100), nullable=False),
                Column("Precio", Float, nullable=False),
                Column("URL", String(255), nullable=False)
                )
        if not inspector.has_table("Productos"):
            # crea la tabla si no existe
            metadata.create_all(self.engine)
            print("La tabla Productos ha sido creada")
        else:
            # trunca la tabla si ya existe
            with self.engine.connect() as connection:
                connection.execute(text("TRUNCATE TABLE Productos"))
                connection.commit()
                print("La tabla Productos ha sido truncada.")
        return None
    
    def load_scraped_data_into_database(self) -> None:
        """ 
        Lee el Excel generado por la clase Scraper
        Adecúa los datos para que coincidan con las restricciones de la tabla Productos 
        y luego los carga a misma dentro de la base de datos 'PythonScrapedData'
        """
        df_ml = pd.read_excel("Output.xlsx")
        df_ml = df_ml.drop(columns="Unnamed: 0")
        df_ml = df_ml.rename(columns=self.column_mapping)
        df_ml['Nombre'] = df_ml['Nombre'].astype(str)
        df_ml['Precio'] = pd.to_numeric(df_ml['Precio'], errors='coerce')
        df_ml['URL'] = df_ml['URL'].astype(str)
        df_ml['Nombre'] = df_ml['Nombre'].str[:100]
        df_ml['URL'] = df_ml['URL'].str[:255]
        # print(df_ml.head())
        try:
            df_ml.to_sql("Productos", self.engine, if_exists="append", index=False)
            print(f"--> Se han cargado {len(df_ml)} registros en la tabla Productos <--")
        except SQLAlchemyError as e:
            print(f"Error al cargar los datos: {str(e)}")
        
        return None