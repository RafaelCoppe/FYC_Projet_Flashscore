# FYC Groupe 20 - Projet Flashscore

Sommaire : 

1. Sujet du projet
2. Limites techniques
3. Fonctionnalités principales
4. Fonctionnalités optionelles

## 1. Sujet du projet
Flashscore.fr est un site de référence pour suivre les résultats sportifs en direct. Il couvre une large gamme de sports tels que le football, le tennis, le basketball et bien d'autres, offrant des mises à jour en temps réel sur les scores, classements, et statistiques. 

Nous voulons stocker et analyser les résultats sportifs sur les sports donnés afin de fournir des statistiques à nos clients. Nous devons donc, chaque jour, récupérer les résultats des matchs **terminés** de la veille et les stocker dans des dossiers spécifiques (par entité / pays, par ligue et par équipe / participant).

## 2. Limites techniques
Url du site : https://www.flashscore.fr  
**!!! L'url https://m.flashscore.fr (site version mobile) est interdite !!!**

- Scraping  
    Bibliothèques : 
    - Selenium pour le scraping
    - Driver navigateur : libre

- Gestion de tâches systèmes
    Bibliothèques :
    - pip3 pour les installations
    - psutil
    - firefox
    - et d'autres ressources que vous pourrez installer progressivement...

- Ecriture et gestion de fichiers   
    - **Système de fichiers** :
        - Le système doit pouvoir gérer la création dynamique de dossiers imbriqués (compatibilité avec les systèmes Windows, macOS, Linux).
        - Les noms des fichiers et dossiers doivent être validés pour éviter des caractères non compatibles avec les systèmes de fichiers.
          
    - **Encodage des fichiers** :
        - Tous les fichiers CSV doivent être encodés en UTF-8 pour garantir la compatibilité avec les caractères spéciaux et les langues internationales.
  
    - **Volume des données** :
        - Si un sport ou une ligue comporte de nombreux matchs (plusieurs centaines), les performances du script et la taille des fichiers doivent être surveillées.
          
    - **Suppression automatique des données inutiles** :
        - Les ligues vides (sans matchs) et les entités sans ligues actives doivent être nettoyées avant la création des fichiers.


- Test unitaire   
    

## 3. Fonctionnalités principales (/15)
- Scraping  
    - Récupération des résultats des sports suivants : Football, Basket, Rugby, Handball
    - Une requete par script - changement de page via les boutons
    - Informations demandées : 
        - Lien du résumé du match
        - Equipe / participant 1
        - Equipe / participant 2
        - Score final 1 
        - Score final 2   
    - Protocole adapté à la mise en page des informations  
    _Indice : les résulats du football et du rugby ne sont pas mis en page comme ceux des autres sports_  
    - Mise en place d'une fonction "get_data_for_sport"  
        Variables :  
            - infos : l'élément `<div>` contenant les informations du match  
            - sport : le nom du sport  

        Utilisation d'une boucle "match" pour choisir la routine de récupération de données à effectuer  
    - Suppression des ligues et entités vides  
        Du à la mise en page, les résultats des ligues mineures sont inaccessibles. Cependant, les noms des ligues sont récupérables et peuvent donc être ajoutés aux fichiers  
        Mettez en place un système pour supprimer les ligues sans matchs, puis supprimer les pays qui n'ont pas de ligue 
    - Vocabulaire pour les variables : 
        - Entity : le groupe responsable de la ligue. Exemple : France pour la Ligue 1, Angleterre pour la Premier League, FIFA pour la coupe du monde
        - League : la ligue dans laquelle les rencontres se déroulent : Ligue 1, Premier League
        - Game : les infos de la partie
    - Format des informations sauvegardées : 
        ```
        {
            'link': link,
            'team1': team1,
            'score1': score1,
            'team2': team2,
            'score2': score2
        }
        ```

- Gestion de tâches systèmes   
    - **Automatisation des processus**

         L'objectif ici est d'automatiser un maximum de tâches systèmes pouvant être utiles à notre programme.
         Dans cette même idée, il faudrait donc :

         **Créer des scripts d'automatisation** :

                - script permettant d'archiver
                - logger (logs)
                - monitoring (watch and restart)
                - resources_monitor (analyse des ressources utilisées)
                - notifier (envoi d'une notification)

      Certains pré-requis seront nécessaires au bon fonctionnement des scripts, ces ressources devront donc être installées via ligne de commande depuis l'IDE.

      Exemple : **webdriver-manager**, **chromium-chromedriver** ou bien **psutil** pour ne citer que ces derniers.

      On souhaiterait se retrouver avec une structure de projet similaire à celle-ci :


               FYC_Projet_Flashscore/
                    ├── flashscore_scraper/        
                    ├── automation/                
                    │   ├── scheduler.py           
                    │   ├── logger_config.py       
                    │   ├── monitor.py             
                    │   ├── resources_monitor.py  
                    │   ├── archiver.py            
                    ├── data/                     
                    │   ├── raw/                  
                    │   ├── archives/              
                    ├── tests/                     
                    ├── requirements.txt          
                    └── README.md

      Explication de la structure :

      - Le dossier *automation* contiendra les scripts permettant d'effectuer les tâches souhaitées
      - Le dossier *data* permettra de stocker toute donnée eventuel pouvant être produite en tant que résultat d'un script
      - Le fichier *requirements* peut contenir des outils ou bibliothèques pouvant être utiles aux scripts

  
     
            *Astuce : Pensez à bien tester vos scripts et prendre connaissance des résultats obtenus.*

      


- Ecriture et gestion de fichiers   
    - **Création de la hiérarchie des dossiers** :
        - Le script doit créer une hiérarchie de dossiers basée sur la structure suivante :
            - Dossier racine : Un dossier par jour au format YYYY-MM-DD.
            - *Sous-dossiers par sport* : Un sous-dossier pour chaque sport traité.
            - *Sous-dossiers par entité/pays* : Chaque pays ou entité doit avoir un sous-dossier dans le sport correspondant.
            - *Sous-dossiers par ligue* : Chaque ligue a son propre dossier dans l’entité correspondante.
        - Exemple :
            ```
              2024-12-30/
              ├── football/
              │   ├── france/
              │   │   ├── ligue_1/
              │   │   │   └── ligue_1_matches.csv
              │   │   ├── ligue_2/
              │   │   │   └── ligue_2_matches.csv
              ├── rugby/
              │   ├── angleterre/
              │   │   ├── premiership/
              │   │   │   └── premiership_matches.csv
            ```


    - **Sauvegarde des données en fichiers CSV** :
        - Les données de chaque ligue doivent être sauvegardées dans des fichiers CSV individuels.
        - *Format des colonnes* : Chaque fichier CSV doit inclure les colonnes suivantes :
            - Lien vers le résumé du match (`link`).
            - Nom des équipes ou participants (`team1`, `team2`).
            - Scores finaux des équipes (`score1`, `score2`).
            - Exemple de contenu CSV :
                ```
                link,team1,score1,team2,score2
                https://flashscore.fr/match/1,equipeA,3,equipeB,2
                https://flashscore.fr/match/2,equipeC,1,equipeD,1
                ```
                **Encodage** : Les fichiers doivent être encodés en UTF-8.

    - **Suppression des données inutiles** :
        - Les ligues sans matchs doivent être supprimées avant la sauvegarde des fichiers.
        - Si un pays n’a aucune ligue active, le dossier correspondant doit être supprimé.

        *Astuce : Implémentez une vérification avant de créer chaque fichier ou dossier.*
    
- Test unitaire   
    

## 4. Fonctionnalités optionelles (/5)
- Scraping  
    - Système de choix de sport dynamique
        Fichier `sports.txt` avec la liste des sports  
        Vérification de l'existence du sport puis scraping des données
    
    - Récupération des scores intermédiaires  
        Scores à la mi-temps pour les sports collectifs, scores aux quart-temps pour le basket ou des sets pour le tennis

    - Système de filtre d'entité  
        Filtrage des Pays / Entités via le fichier `sports.txt`

- Gestion de tâches système   
    

- Ecriture et gestion de fichiers   
    - **Archivage des données** :
        - Après la création des dossiers et des fichiers CSV, compressez automatiquement l’intégralité du dossier de la journée dans une archive ZIP pour économiser de l’espace disque.
        - Nom de l’archive : YYYY-MM-DD_results.zip.
        - Emplacement : Racine du projet ou un dossier dédié (archives/).

    - **Récapitulatif des données** :
        - Ajoutez un fichier texte recap.txt dans le dossier principal pour résumer les données du jour.
            - Nombre total de sports traités.
            - Nombre total de matchs enregistrés.
            - Détail des sports avec leurs statistiques (nombre de ligues, nombre de matchs).

        *Exemple de contenu :*
        ```
        Date : 2024-12-30
        Nombre total de sports : 2
        Nombre total de matchs : 42

        Détails :
        - Football : 28 matchs (3 ligues, 2 pays)
        - Rugby : 14 matchs (1 ligue, 1 pays)
        ```

    - **Export JSON (complément au CSV)** :
        - Sauvegardez les données de chaque ligue dans un fichier JSON en plus du fichier CSV.
        - Format structuré, idéal pour une réutilisation dans des projets ou des API.

- Test unitaire   
    
