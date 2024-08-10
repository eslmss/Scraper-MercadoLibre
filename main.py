from ClassScraper import Scraper
from ClassDatabaseLoad import DatabaseLoad

if __name__ == "__main__":
    # instancia objeto de la clases Scraper y DatabaseLoad, luego llama a sus métodos para ejecutar el programa
    obj1 = Scraper()
    obj1.user_input()
    print("------------------------------------------------------------------------------------------------------------------------------------------")
    df = obj1.scraping()
    print("------------------------------------------------------------------------------------------------------------------------------------------")
    obj1.quick_analysis(df)
    print("------------------------------------------------------------------------------------------------------------------------------------------")
    obj1.ask_for_download(df)
    
    print("------------------------------------------------------------------------------------------------------------------------------------------")
    obj2 = DatabaseLoad()
    obj2.create_table_if_not_exists()
    print("------------------------------------------------------------------------------------------------------------------------------------------")
    obj2.load_scraped_data_into_database()