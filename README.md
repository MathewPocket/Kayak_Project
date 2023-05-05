# Plan_your_trip_with_Kayak
Projet Kayak dans le cadre de la certification Machine Learning Engineer

## Description
Le notebook kayak_final.ipynb est la partie principale du projet
Grace à ce notebook vous pouvez pour une liste de ville selectionnées, aller chercher les informations météo et les prix des hotels dans ces villes. 
Afficher de manière graphique les 5 meilleures villes point de vue météo et les 20 hotels les moins chers dans ces zones.

## Tuto Exécution du Script

### Variables d'environnement du projet : 
API_KEY_OW : Doit contenir votre clé de l'api [OpenWeather](https://openweathermap.org) 
MAP_BOX_TOKEN : Doit contenir votre clé api [MAPBOX](https://www.mapbox.com)
AWS_ACCESS_KEY_ID : Clé d'accès Amazon AWS avec des droits sur S3 et RDS
AWS_SECRET_ACCESS_KEY= Secret d'accès à Amazon AWS

### Docker
*Si docker est installé sur votre poste, lancer simplement le script run.sh, il se chargera de créer une image docker "kayakimg", puis de la lancer, ensuite lancer vscode sur votre container docker en cours. Le code se trouve dans /home/app de la machine

*Si vous n'avez pas docker, sur votre environnement python assurez vous d'avoir toutes les librairies indiquées dans requirements.txt

### Paramétrage du script principale kayak_final.ipynb
* Définir la liste des villes à scanner (par défaut 35 villes)
* mode = 'full' ou 'price' : Dans le cas de full, le scrapping des hotels se fera entièrement, à la fois sur leurs localisations, mais aussi les prix, la base amazon RDS sera effacée pour insérer les nouvelles données. En mode price, on actualisera uniquement les prix pour les hotels existants, permet un rafraichissement plus rapide
* local_mode = True or False : Si True, alors aucun appel ne sera fait à des API ou AWS, les fichiers utilisés seront ceux présent dans le dossier /app/testing_data
* no_scrap = True or False : Si True, le scrapping des hotels (partie assez longue) ne sera pas effectuée, le fichier utiliser sera récupérer de /app/testing_data
* rds_mode = True or False : Si True les données seront sauvegardées et récupérées sur AWS RDS
* bucket_name : Paramétrage du nom du bucket de sauvegarde sur AWS S3
* p_DBName : Nom de la base sur AWS RDS
* p_DBInstanceIdentifier : Nom de l'instance sur AWS RDS
* p_MasterUsername : Nom d'utilisateur sur AWS RDS
* p_MasterUserPassword : Password de connexion sur AWS RDS
* date_sejour : Date pour laquelle vous souhaitez partir
* duree_sejour : Nombre de jour du séjour, doit être inférieur à 7 car l'api OpenWeather ne donne accès gratuitement que sur 7 jours pour les prévisions

### Exécution du script
Vous pouvez ensuite lancer chaque cellule à la main ou d'un seul coup, les graphiques seront affichés en bas