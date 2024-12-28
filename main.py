from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
import time

# Initialiser le driver Firefox
def initialize_driver():
    options = webdriver.FirefoxOptions()
    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)
    return driver

def get_data_for_sport(infos, sport):
    match sport:
        case 'football':
            link = infos[0].get_attribute('href')
            team1 = infos[3].text.strip()
            score1 = infos[5].text.strip()
            team2 = infos[4].text.strip()
            score2 = infos[6].text.strip()
        case 'rugby':
            link = infos[0].get_attribute('href')
            team1 = infos[3].text.strip()
            score1 = infos[7].text.strip()
            team2 = infos[5].text.strip()
            score2 = infos[8].text.strip()
        case _:
            link = infos[0].get_attribute('href')
            team1 = infos[4].text.strip()
            team2 = infos[6].text.strip()
            score1 = infos[7].text.strip()
            score2 = infos[8].text.strip()
    
    return {
        'link': link,
        'team1': team1,
        'score1': score1,
        'team2': team2,
        'score2': score2,
    }
    
def clean_empty_data(data):
    # Si l'élément est un dictionnaire, on parcourt ses clés
    if isinstance(data, dict):
        keys_to_delete = []
        for key, value in data.items():
            # Si la valeur est vide (une liste vide ou un dictionnaire vide), on marque la clé pour suppression
            clean_empty_data(value)  # Appel récursif pour nettoyer les sous-éléments
            if not value:  # Si la valeur est devenue vide après le nettoyage
                keys_to_delete.append(key)
        
        # Suppression des clés marquées
        for key in keys_to_delete:
            del data[key]

    # Si l'élément est une liste, on supprime les éléments vides
    elif isinstance(data, list):
        # Suppression des éléments vides dans la liste
        data[:] = [item for item in data if item]

# Script principal
sports_list = ["football", "basket", "rugby", "handball"]
driver = initialize_driver()  # Initialiser le driver
try:
    driver.get("https://www.flashscore.fr/")  # Ouvrir le site
    time.sleep(3)  # Attendre que la page se charge

    final_data = {}
            
    for sport in sports_list:
        try:
            # Trouver le bouton correspondant au sport
            try: 
                if(sport == 'football'):
                    sport_button = driver.find_element(By.XPATH, f"//a[contains(@href, '/')]")
                else:
                    sport_button = driver.find_element(By.XPATH, f"//a[contains(@href, '/{sport.lower()}/')]")
            except: 
                print(f"Erreur : Impossible de trouver le sport '{sport}'")
                continue
            
            print(f"Récupération des données pour le sport '{sport}'")
            
            sport_button.click()  # Cliquer sur le bouton
            time.sleep(2)  # Attendre que la page se charge
            
            sport_data = {}

            # Mettre la date à 'hier'
            yesterday_button = driver.find_element(By.CLASS_NAME, "calendar__navigation--yesterday");
            yesterday_button.click()
            
            time.sleep(2)  # Attendre que la page se charge
            
            # Séléctionner les résultats terminés
            button = driver.find_element(By.XPATH, "//div[contains(@class, 'filters__text') and text()='Terminés']")
            parent_button = button.find_element(By.XPATH, "./ancestor::div[contains(@class, 'filters__tab')]")
            parent_button.click()
            
            time.sleep(2)  # Attendre que la page se charge
            
            # Récupérer la liste des ligues
            # Trouver le conteneur principal des sports
            results_container = driver.find_element(By.CLASS_NAME, "sportName")

            # Trouver tous les enfants de ce conteneur
            results = results_container.find_elements(By.XPATH, "./*")

            current_entity = None
            current_league = None

            # Parcourir les enfants
            for div in results:
                # Si c'est un en-tête de ligue
                if "wclLeagueHeader" in div.get_attribute("class"):
                    title_box_children = div.find_element(By.CLASS_NAME, "event__titleBox").find_elements(By.XPATH, "./*")
                    current_entity = title_box_children[0].text.strip().lower()
                    current_league = title_box_children[2].text.strip().lower()
                
                    if not current_entity in sport_data:
                        sport_data[current_entity] = {}
                        
                    if not current_league in sport_data[current_entity]:
                        sport_data[current_entity][current_league] = []
                # Si c'est un résultat
                elif div.get_attribute("data-event-row") == "true":
                    if current_entity and current_league :
                        result_infos = div.find_elements(By.XPATH, "./*")
                        data = get_data_for_sport(result_infos, sport)

                        sport_data[current_entity][current_league].append(data)
                        
            clean_empty_data(sport_data)
            final_data[sport] = sport_data
            print(f"Données récupérées pour le sport '{sport}'")
        except Exception as e:
            print(f"Erreur lors de la récupération des données: {e}")

finally:
    driver.quit()  # Fermer le navigateur

# Suite du code
