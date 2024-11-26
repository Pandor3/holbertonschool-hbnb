# HBnB (Holberton AirBnB)

## Description

HBnB est une application de type AirBnB, structurée en trois couches (Présentation, Logique Métier et Persistance) pour gérer les utilisateurs, les lieux, les avis et les commodités. Le projet est conçu avec Flask et Flask-RESTx pour créer une API RESTful.

## Structure du Projet

```bash
hbnb/
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── v1/
│   │       ├── __init__.py
│   │       ├── users.py
│   │       ├── places.py
│   │       ├── reviews.py
│   │       ├── amenities.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── place.py
│   │   ├── review.py
│   │   ├── amenity.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── facade.py
│   ├── persistence/
│       ├── __init__.py
│       ├── repository.py
├── run.py
├── config.py
├── requirements.txt
├── README.md
```

## Installation
### 1. Clone le dépôt:
```bash
git clone https://github.com/ton-utilisateur/hbnb.git
```
### 2. Accède au dossier du projet:
```bash
cd hbnb
```
### 3. Installe les dépendances:
```bash
pip install -r requirements.txt
```

## Utilisation
### Pour démarrer l'application la première fois, exécute le fichier **create_db.sh**
```bash
./create_db.sh
```
### Puis pour relancer le serveur sans perdre les données déja enregistrées , exécute le fichier **run_app.sh**
```bash
./run_app.sh
```

L'application sera accessible à l'adresse http://127.0.0.1:5000.

## Diagrammes

```mermaid
erDiagram
   USER ||--o{ PLACE : owns
   USER ||--o{ REVIEW : writes
   PLACE ||--o{ REVIEW : receives
   PLACE ||--o{ PLACE_AMENITY : contains
   AMENITY ||--o{ PLACE_AMENITY : associated_with

   USER {
       int id
       string first_name
       string last_name 
       string email
       string password
       bool is_admin
   }

   PLACE {
       int id
       string title
       string description
       float price
       float latitude
       float longitude
       int owner_id 
   }

   REVIEW {
       int id
       string text
       int rating
       int user_id
       int place_id
   }

   AMENITY {
       int id
       string name
   }

   PLACE_AMENITY {
       int place_id
       int amenity_id
   }
```
```mermaid
erDiagram
    USER ||--o{ PLACE : owns
    USER ||--o{ REVIEW : writes
    PLACE ||--o{ REVIEW : receives
    PLACE ||--o{ PLACE_AMENITY : contains
    AMENITY ||--o{ PLACE_AMENITY : associated_with
    USER ||--o{ RESERVATION : makes
    PLACE ||--o{ RESERVATION : booked_for

    USER {
        int id
        string first_name
        string last_name 
        string email
        string password
        bool is_admin
    }

    PLACE {
        int id
        string title
        string description
        float price
        float latitude
        float longitude
        int owner_id 
    }

    REVIEW {
        int id
        string text
        int rating
        int user_id
        int place_id
    }

    AMENITY {
        int id
        string name
    }

    PLACE_AMENITY {
        int place_id
        int amenity_id
    }

    RESERVATION {
        int id
        date start_date
        date end_date
        int user_id
        int place_id
    }
```
