# Analyse de données Airbnb — MongoDB · ReplicaSet · Sharding · Power BI

> Conception et analyse d'une base de données NoSQL MongoDB à partir de
> données Airbnb (Paris + Lyon) : import, requêtes d'analyse, ReplicaSet,
> Sharding et connexion Power BI.

## Contexte & objectif

Ce projet explore les capacités de MongoDB sur un dataset réel de locations
Airbnb (95 885 logements). Il couvre l'ensemble du cycle : import des données,
analyse via mongosh et Polars, mise en place d'une architecture distribuée
(ReplicaSet + Sharding), et exposition des données dans Power BI.

## Stack technique

`Python` `MongoDB` `Polars` `Power BI` `Docker`

## Architecture
```
┌─────────────────────────────────────────────────────┐
│                   Cluster MongoDB                   │
│                                                     │
│  ┌──────────────┐        ┌──────────────┐           │
│  │   rs0 (Lyon) │        │ rs1 (Paris)  │           │
│  │  Primary     │        │  Primary     │           │
│  │  Secondary   │        │  Secondary   │           │
│  │  Arbitre     │        │              │           │
│  └──────┬───────┘        └──────┬───────┘           │
│         │                       │                   │
│         └──────────┬────────────┘                   │
│                    ▼                                │
│             [Config Server]                         │
│                    │                                │
│                    ▼                                │
│              [mongos router]                        │
│         Shard key: city_name + _id                  │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
                 [Power BI]
          via ODBC + BI Connector
```

## Structure du repo
```
├── import_simple.py        # Import du dataset Lyon dans MongoDB
├── queries.ipynb           # Requêtes d'analyse avec Polars
└── README.md
```

## Données

- **Source** : [Inside Airbnb](http://insideairbnb.com/) — Open Data
- **Villes** : Paris + Lyon
- **Volume** : 95 885 logements, 74 champs par document
- **Types** : ObjectID, Int32, String, Int64, Date, Boolean, Double, Array

Le format document MongoDB est particulièrement adapté ici car les données
sont hétérogènes et évolutives — un document correspond naturellement à un
logement, permettant lecture rapide sans jointures et ajout de champs sans
migration.

## Analyses réalisées

### Requêtes mongosh
- Nombre total de documents et logements disponibles
- Nombre d'annonces par type de location
- Logements les plus loués
- Nombre total d'hôtes différents
- Locations réservables instantanément
- Hôtes avec plus de 100 annonces
- Nombre de superhôtes

## Lancement du projet

Prérequis : MongoDB installé localement

**1. Importer les données**

Importer `listings_Paris.csv` ( https://s3.eu-west-1.amazonaws.com/course.oc-static.com/projects/922_Data+Engineer/922_P7/listings_Paris+(1).csv) via MongoDB Compass dans la collection
`noscites.logements`, puis importer Lyon ( https://drive.google.com/file/d/14TfkpdvTV_PNv_5wkaA-CgoYK0Tjyn-X/view) via le script Python :
```bash
pip install pymongo
python import_simple.py
```

**2. Lancer les analyses Polars**
```bash
pip install polars pymongo jupyter
jupyter notebook queries.ipynb
```

## Architecture distribuée

### ReplicaSet rs0 (Lyon)
- Lancement des 3 instances MongoDB
- Création du ReplicaSet avec Primary, Secondary et Arbitre
- Test de réplication des données

### ReplicaSet rs1 (Paris)
- Même architecture sans arbitre

### Sharding
- Lancement du Config Server (`cfgRS`)
- Lancement du routeur `mongos`
- Ajout des shards rs0 et rs1 dans le cluster
- Activation du sharding sur la collection `logements`
- Shard key : `city_name` + `_id`
- Séparation des chunks par ville (Lyon → rs0, Paris → rs1)

## Connexion Power BI

La connexion Power BI → MongoDB passe par :
1. Installation du **MongoDB ODBC Driver**
2. Installation et lancement du **MongoDB BI Connector** (`mongosqld`)
   — agit comme proxy SQL entre Power BI et MongoDB
3. Création d'un **DSN ODBC** dans l'ODBC Manager
4. Connexion Power BI via ODBC avec le DSN configuré
5. Import de la collection `logements` dans Power BI

## Apprentissages clés

- Modélisation orientée document et pertinence du NoSQL pour données hétérogènes
- Requêtes MongoDB (mongosh) et analyse avec Polars
- Mise en place d'un ReplicaSet MongoDB avec arbitre
- Architecture de Sharding : Config Server, routeur mongos, shard keys
- Exposition de MongoDB à un outil BI via ODBC + BI Connector
