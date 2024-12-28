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

- Gestion de tâches système   
    

- Ecriture et gestion de fichiers   
    

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

- Gestion de tâches système   
    

- Ecriture et gestion de fichiers   
    

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
    

- Test unitaire   
    