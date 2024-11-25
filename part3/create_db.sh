#!/bin/bash

# Empêcher la création des fichiers __pycache__
export PYTHONDONTWRITEBYTECODE=1

# Supprimer les fichiers __pycache__ existants
echo "Suppression des fichiers __pycache__ existants..."
find . -type d -name "__pycache__" -exec rm -rf {} +

# Chemin vers la base de données
DB_PATH="instance/development.db"

# Supprimer development.db s'il existe déjà
if [ -f "$DB_PATH" ]; then
  echo "Suppression du fichier existant $DB_PATH..."
  rm "$DB_PATH"
fi

# Vérifier si Flask est installé
if ! command -v flask &> /dev/null; then
  echo "Flask n'est pas installé. Veuillez l'installer et réessayer."
  exit 1
fi

# Vérifier si sqlite3 est installé
if ! command -v sqlite3 &> /dev/null; then
  echo "sqlite3 n'est pas installé. Veuillez l'installer et réessayer."
  exit 1
fi

# Lancer Flask shell et exécuter les commandes pour initialiser la base de données
echo "Initialisation de la base de données avec Flask..."
flask shell << EOF
from app import db
db.create_all()
exit()
EOF

# Vérifier si le fichier de la base de données a été créé
if [ -f "$DB_PATH" ]; then
  echo "Base de données initialisée avec succès. Lancement de SQLite3..."
  
  # Lancer SQLite3, afficher les tables et quitter immédiatement
  sqlite3 "$DB_PATH" << SQLITE_COMMANDS
.tables
.exit
SQLITE_COMMANDS

  echo "SQLite a été lancé et quitté avec succès."
else
  echo "Erreur : le fichier $DB_PATH n'a pas été trouvé. Assurez-vous que Flask a bien configuré la base de données."
fi

./run_app.sh
