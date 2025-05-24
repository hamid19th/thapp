# Python Quiz App

Une application de quiz Python avec authentification et suivi des scores, utilisant KivyMD et Google Sheets.

## Fonctionnalités

- Interface utilisateur moderne avec KivyMD
- Authentification des utilisateurs
- Questions à choix multiples
- Suivi des scores
- Classement des meilleurs scores
- Historique personnel
- Support multilingue (Français)

## Prérequis

- Python 3.9 ou supérieur
- KivyMD
- Google Sheets API
- Buildozer (pour la compilation Android)

## Installation

1. Clonez le dépôt :
```bash
git clone https://github.com/votre-username/python-quiz-app.git
cd python-quiz-app
```

2. Installez les dépendances :
```bash
pip install -r requirements.txt
```

3. Configurez les credentials Google Sheets :
- Placez votre fichier `credentials.json` à la racine du projet

## Compilation de l'APK

### Méthode automatique (GitHub Actions)

1. Forkez ce dépôt
2. Activez GitHub Actions dans votre fork
3. Poussez vos modifications
4. L'APK sera automatiquement compilé et disponible dans les artifacts

### Méthode manuelle

1. Installez buildozer :
```bash
pip install buildozer
```

2. Compilez l'APK :
```bash
buildozer android debug
```

L'APK sera généré dans le dossier `bin/`

## Structure du projet

- `main.py` : Point d'entrée de l'application
- `sheets_config.py` : Configuration et fonctions Google Sheets
- `buildozer.spec` : Configuration de la compilation
- `.github/workflows/` : Configuration GitHub Actions

## Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
1. Forker le projet
2. Créer une branche pour votre fonctionnalité
3. Commiter vos changements
4. Pousser vers la branche
5. Ouvrir une Pull Request

## Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails. 