import requests
from bs4 import BeautifulSoup
import pandas as pd
import openpyxl
# import time

class Scraper():
    """
    Clase que scrapea MercadoLibre en base al producto ingresado por el usuario y 
    genera un Excel 'Output.xlsx' dentro del mismo directorio con los datos extraídos
    """
    def __init__(self) -> None:
        """ Constructor que inicializa el atributo de clase con la URL de Mercado Libre Argentina """
        self.url = "https://listado.mercadolibre.com.ar/"
        # self.product = ""
        return None
    
    
    def user_input(self) -> None:
        """ Método que recibe el input del usuario y modifica el atributo de clase 'self.url' en base al input """
        product = input("\n¿Qué producto desea buscar?: ")
        self.product = product.replace(" ", "-").lower() 
        self.url = self.url + self.product
        return None    
    
    
    def scraping(self) -> pd.DataFrame:
        """ Método que scrapea MercadoLibre buscando el producto ingresado por el usuario, y retorna un pd.DataFrame con los productos, precios y links """
        # listas para almacenar los datos
        product_titles = []
        product_prices = []
        product_links = []

        # variables para recorrer todas las páginas de resultados
        page_number = 1
        url_desde_number = 1

        while True:
            # en cada iteración construye el URL de la página actual a scrapear
            if page_number > 1:
                url_desde_number += 50
                self.url = f"https://listado.mercadolibre.com.ar/{self.product}_Desde_{url_desde_number}_NoIndex_True"

            # realiza la solicitud HTTP
            response = requests.get(self.url)
            # parsea el contenido HTML de la página
            soup = BeautifulSoup(response.content, "html.parser")
            # forma una lista con todas las publicaciones de la página actual
            items = soup.find_all("li", class_="ui-search-layout__item")
            
            if not items:   # si la lista está vacía se termina el bucle
                break
            
            print(f"--> Scrapeando {len(items)} elementos página {page_number}: {self.url} <--")
            
            # extrae títulos, precios y links de cada una de las publicaciones de la página actual
            for item in items:
                title = item.find("h2")#, class_="poly-box") 
                price = item.find("span", class_="andes-money-amount__fraction") 
                link = item.find("a")#, class_="ui-search-item__group__element")

                if title and price and link:    # si todas las extracciones fueron exitosas, se appendean a sus correspondientes listas
                    product_titles.append(title.text.strip())
                    product_prices.append(price.text.strip())
                    product_links.append(link['href'])
                
            # pasa a la siguiente página para continuar con la siguiente iteración
            page_number += 1
        
        # construye un pd.DataFrame en base a un diccionario de listas appendeadas
        df_ml = pd.DataFrame({
            "product"   : product_titles, 
            "price"     : product_prices,
            "link"      : product_links
            })
        
        # pd.set_option("display.max_colwidth", None)
        # imprime los primeros 10 productos en consola
        print(df_ml.head(11))
        return df_ml
        
    
    def quick_analysis(self, df: pd.DataFrame) -> None:
        """
        Método que calcula algunos estadísticos básicos de importancia
        Moda: expresa el valor con mayor frecuencia en un conjunto de datos
        """
        df["price"] = df["price"].str.replace(".", "").str.replace(",", ".")
        df["price"] = pd.to_numeric(df["price"])
        print(f"""
                --> Promedio precios  : $ {df['price'].mean()}
                --> Moda precio/s     : {[f'$ {p}' for p in df['price'].mode().values.tolist()]}
                --> Mínimo precio     : $ {df['price'].min()}
                --> Máximo precio     : $ {df['price'].max()}
              """)
        # print(df.dtypes)
        return None
    
    def ask_for_download(self, df: pd.DataFrame) -> None:
        """ Método que consulta al usuario si desea descargar los resultados del scraping a un Excel dentro del mismo directorio"""
        while True:
            download = input("¿Desea descargar los resultados a Excel? (S/N): ").upper()
            if download in ["S", "N"]:
                break
            print("Por favor, ingrese 'S' para sí o 'N' para no.")

        if download == "S":
            df.to_excel("Output.xlsx")
            print("Los resultados se han descargado en 'Output.xlsx'")
        else:
            print("Fin del scraping")
            exit()
        return None