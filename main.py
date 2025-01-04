import os
import csv
import json
import shutil
import time
from datetime import datetime, timedelta  # Import de timedelta pour corriger l'erreur
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager

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
    """
    Supprime les entrées vides d'un dictionnaire ou d'une liste.
    """
    if isinstance(data, dict):
        keys_to_delete = []
        for key, value in data.items():
            clean_empty_data(value)
            if not value:
                keys_to_delete.append(key)
        for key in keys_to_delete:
            del data[key]
    elif isinstance(data, list):
        data[:] = [item for item in data if item]

# Script principal
sports_list = ["football", "basket", "rugby", "handball"]
driver = initialize_driver()  # Initialiser le driver

try:
    driver.get("https://www.flashscore.fr/")  # Ouvrir le site
    time.sleep(3)  # Attendre que la page se charge

    final_data = {}  # Dictionnaire pour stocker les résultats

    for sport in sports_list:
        try:
            # Trouver le bouton correspondant au sport
            if sport == 'football':
                sport_button = driver.find_element(By.XPATH, f"//a[contains(@href, '/')]")
            else:
                sport_button = driver.find_element(By.XPATH, f"//a[contains(@href, '/{sport.lower()}/')]")

            print(f"Récupération des données pour le sport '{sport}'")
            sport_button.click()  # Cliquer sur le bouton
            time.sleep(2)  # Attendre que la page se charge

            sport_data = {}

            # Mettre la date à 'hier'
            yesterday_button = driver.find_element(By.CLASS_NAME, "calendar__navigation--yesterday")
            yesterday_button.click()
            time.sleep(2)

            # Sélectionner les résultats terminés
            button = driver.find_element(By.XPATH, "//div[contains(@class, 'filters__text') and text()='Terminés']")
            parent_button = button.find_element(By.XPATH, "./ancestor::div[contains(@class, 'filters__tab')]")
            parent_button.click()
            time.sleep(2)

            # Récupérer la liste des ligues
            results_container = driver.find_element(By.CLASS_NAME, "sportName")
            results = results_container.find_elements(By.XPATH, "./*")

            current_entity = None
            current_league = None

            for div in results:
                if "wclLeagueHeader" in div.get_attribute("class"):
                    title_box_children = div.find_element(By.CLASS_NAME, "event__titleBox").find_elements(By.XPATH, "./*")
                    current_entity = title_box_children[0].text.strip().lower()
                    current_league = title_box_children[2].text.strip().lower()

                    if current_entity not in sport_data:
                        sport_data[current_entity] = {}

                    if current_league not in sport_data[current_entity]:
                        sport_data[current_entity][current_league] = []
                elif div.get_attribute("data-event-row") == "true":
                    if current_entity and current_league:
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
def create_directory_structure(base_path, sport, entity, league):
    sport_path = os.path.join(base_path, sport)
    os.makedirs(sport_path, exist_ok=True)

    entity_path = os.path.join(sport_path, entity)
    os.makedirs(entity_path, exist_ok=True)

    league_path = os.path.join(entity_path, league)
    os.makedirs(league_path, exist_ok=True)

    return league_path

def write_csv(file_path, matches):
    headers = ['link', 'team1', 'score1', 'team2', 'score2']
    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        writer.writerows(matches)

def write_json(file_path, matches):
    """
    Écrit les données des matchs dans un fichier JSON.
    """
    with open(file_path, 'w', encoding='utf-8') as jsonfile:
        json.dump(matches, jsonfile, indent=4, ensure_ascii=False)

def write_recap_file(base_path, final_data):
    """
    Crée un fichier récapitulatif détaillé des données dans le dossier principal.
    """
    recap_file = os.path.join(base_path, 'recap.txt')
    total_sports = len(final_data)
    total_matches = 0
    lines = [f"Date : {os.path.basename(base_path)}", f"Nombre total de sports : {total_sports}"]

    for sport, sport_data in final_data.items():
        sport_matches = 0
        total_leagues = 0
        total_entities = len(sport_data)

        for entity, entity_data in sport_data.items():
            total_leagues += len(entity_data)
            for matches in entity_data.values():
                sport_matches += len(matches)

        total_matches += sport_matches
        lines.append(f"- {sport.capitalize()} : {sport_matches} matchs ({total_leagues} ligues, {total_entities} pays)")

    lines.insert(2, f"Nombre total de matchs : {total_matches}")
    lines.append("")  # Ligne vide à la fin pour un format propre

    with open(recap_file, 'w', encoding='utf-8') as file:
        file.write('\n'.join(lines))

def archive_results(base_path):
    """
    Crée une archive ZIP du dossier principal.
    """
    archive_path = f"{base_path}.zip"
    shutil.make_archive(base_path, 'zip', base_path)
    print(f"Dossier archivé : {archive_path}")

def get_user_choice():
    """
    Demande à l'utilisateur de choisir le format de sauvegarde (CSV, JSON ou les deux).
    """
    print("Choisissez le format d'enregistrement des données :")
    print("1. CSV uniquement")
    print("2. JSON uniquement")
    print("3. CSV et JSON")
    
    while True:
        choice = input("Votre choix (1, 2 ou 3) : ").strip()
        if choice in {'1', '2', '3'}:
            return choice
        else:
            print("Choix invalide. Veuillez entrer 1, 2 ou 3.")

def save_results(final_data):
    """
    Sauvegarde les résultats de `final_data` dans des dossiers et fichiers selon le choix de l'utilisateur.
    """
    # Obtenir le choix de l'utilisateur
    choice = get_user_choice()

    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    base_path = os.path.join(os.getcwd(), yesterday)

    for sport, sport_data in final_data.items():
        for entity, entity_data in sport_data.items():
            for league, matches in entity_data.items():
                league_path = create_directory_structure(base_path, sport, entity, league)

                # Enregistrer selon le choix de l'utilisateur
                if choice == '1':  # CSV uniquement
                    csv_file_path = os.path.join(league_path, f"{league}_matches.csv")
                    write_csv(csv_file_path, matches)
                elif choice == '2':  # JSON uniquement
                    json_file_path = os.path.join(league_path, f"{league}_matches.json")
                    write_json(json_file_path, matches)
                elif choice == '3':  # CSV et JSON
                    csv_file_path = os.path.join(league_path, f"{league}_matches.csv")
                    json_file_path = os.path.join(league_path, f"{league}_matches.json")
                    write_csv(csv_file_path, matches)
                    write_json(json_file_path, matches)

    # Générer un fichier récapitulatif
    write_recap_file(base_path, final_data)

    # Archiver le dossier principal
    archive_results(base_path)

# Exemple d'appel
save_results(final_data)