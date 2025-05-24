import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
from datetime import datetime
import re

# ====================================
# IMPORTANT: Mettez à jour cet ID avec celui de votre feuille
# Pour obtenir l'ID, exécutez setup_sheets.py et copiez l'ID affiché
# ====================================
SPREADSHEET_ID = '1Ym7kmI7-G8kpmfbVRbfxWvRBRrLujUWXA3w6cyeTxxE'  # <-- Remplacez cet ID par le vôtre

# Nom des onglets dans Google Sheets
WORKSHEET_USERS = 'Users'  # Onglet des utilisateurs
WORKSHEET_SCORES = 'Scores'  # Onglet des scores
WORKSHEET_QUESTIONS = 'Questions'  # Nouvel onglet pour les questions

def get_sheets_client():
    try:
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/spreadsheets',
                 'https://www.googleapis.com/auth/drive.file',
                 'https://www.googleapis.com/auth/drive']
        
        # Vérifier si le fichier credentials existe
        if not os.path.exists('credentials.json'):
            raise FileNotFoundError("Le fichier credentials.json est manquant. Veuillez suivre les instructions pour le configurer.")
        
        creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
        client = gspread.authorize(creds)
        return client
    except FileNotFoundError as e:
        print(f"Erreur de configuration : {e}")
        return None
    except Exception as e:
        print(f"Erreur d'authentification : {e}")
        return None

def is_admin(username, password):
    """Vérifie si l'utilisateur est un administrateur"""
    return username == 'admin' and password == '123456admin'

def verify_credentials(username, password):
    try:
        # Vérifier d'abord si c'est un admin
        if is_admin(username, password):
            return {
                'success': True,
                'user_id': 'admin',
                'username': username,
                'is_admin': True
            }
            
        client = get_sheets_client()
        if client is None:
            return {'success': False, 'error': 'Erreur de configuration Google Sheets'}
            
        # Ouvrir la feuille par son ID
        spreadsheet = client.open_by_key(SPREADSHEET_ID)
        try:
            worksheet = spreadsheet.worksheet(WORKSHEET_USERS)
        except gspread.WorksheetNotFound:
            print(f"Erreur : L'onglet '{WORKSHEET_USERS}' n'existe pas")
            return {'success': False, 'error': f"L'onglet '{WORKSHEET_USERS}' n'existe pas"}
        
        # Get all username/password pairs
        records = worksheet.get_all_records()
        
        # Check if credentials match and return user data
        for record in records:
            if str(record.get('username', '')).strip() == str(username).strip() and str(record.get('password', '')).strip() == str(password).strip():
                return {
                    'success': True,
                    'user_id': record.get('id', ''),
                    'username': record['username'],
                    'is_admin': False
                }
        return {'success': False, 'error': 'Identifiants invalides'}
    except gspread.SpreadsheetNotFound:
        print("Erreur : Feuille Google Sheets non trouvée ou non accessible")
        return {'success': False, 'error': 'Feuille non trouvée'}
    except Exception as e:
        print(f"Erreur d'accès à Google Sheets : {e}")
        return {'success': False, 'error': str(e)}

def get_user_by_id(user_id):
    try:
        client = get_sheets_client()
        if client is None:
            return None
            
        # Ouvrir la feuille par son ID
        spreadsheet = client.open_by_key(SPREADSHEET_ID)
        try:
            worksheet = spreadsheet.worksheet(WORKSHEET_USERS)
        except gspread.WorksheetNotFound:
            print(f"Erreur : L'onglet '{WORKSHEET_USERS}' n'existe pas")
            return None
            
        records = worksheet.get_all_records()
        
        for record in records:
            if str(record.get('id', '')) == str(user_id):
                return {
                    'id': record['id'],
                    'username': record['username']
                }
        return None
    except Exception as e:
        print(f"Erreur d'accès à Google Sheets : {e}")
        return None

def save_score(user_id, username, score, total_questions):
    """Sauvegarde le score d'un quiz dans Google Sheets"""
    try:
        client = get_sheets_client()
        if client is None:
            return False
            
        spreadsheet = client.open_by_key(SPREADSHEET_ID)
        
        # Vérifier si l'onglet Scores existe, sinon le créer
        try:
            worksheet = spreadsheet.worksheet(WORKSHEET_SCORES)
        except gspread.WorksheetNotFound:
            worksheet = spreadsheet.add_worksheet(WORKSHEET_SCORES, 1000, 6)
            # Ajouter les en-têtes
            headers = ['date', 'user_id', 'username', 'score', 'total_questions', 'pourcentage']
            worksheet.update('A1:F1', [headers])
            worksheet.format('A1:F1', {
                'textFormat': {'bold': True},
                'backgroundColor': {'red': 0.8, 'green': 0.8, 'blue': 0.8}
            })
        
        # Ajouter le nouveau score
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        pourcentage = (score / total_questions) * 100
        new_row = [date, user_id, username, score, total_questions, f"{pourcentage:.1f}%"]
        worksheet.append_row(new_row)
        
        return True
    except Exception as e:
        print(f"Erreur lors de la sauvegarde du score : {e}")
        return False

def get_top_scores(limit=5):
    """Récupère les meilleurs scores"""
    try:
        client = get_sheets_client()
        if client is None:
            return []
            
        spreadsheet = client.open_by_key(SPREADSHEET_ID)
        try:
            worksheet = spreadsheet.worksheet(WORKSHEET_SCORES)
        except gspread.WorksheetNotFound:
            return []
            
        records = worksheet.get_all_records()
        if not records:
            return []
            
        # Trier par pourcentage (enlever le % et convertir en float)
        records.sort(key=lambda x: float(x['pourcentage'].replace('%', '')), reverse=True)
        
        return records[:limit]
    except Exception as e:
        print(f"Erreur lors de la récupération des meilleurs scores : {e}")
        return []

def get_user_history(user_id):
    """Récupère l'historique des scores d'un utilisateur"""
    try:
        client = get_sheets_client()
        if client is None:
            return []
            
        spreadsheet = client.open_by_key(SPREADSHEET_ID)
        try:
            worksheet = spreadsheet.worksheet(WORKSHEET_SCORES)
        except gspread.WorksheetNotFound:
            return []
            
        records = worksheet.get_all_records()
        if not records:
            return []
            
        # Filtrer les scores de l'utilisateur
        user_scores = [r for r in records if str(r['user_id']) == str(user_id)]
        # Trier par date (du plus récent au plus ancien)
        user_scores.sort(key=lambda x: x['date'], reverse=True)
        
        return user_scores
    except Exception as e:
        print(f"Erreur lors de la récupération de l'historique : {e}")
        return []

def validate_password(password):
    """Valide la complexité du mot de passe"""
    if len(password) < 6:
        return False, "Le mot de passe doit contenir au moins 6 caractères"
    return True, ""

def validate_username(username):
    """Valide le format du nom d'utilisateur"""
    if not re.match("^[a-zA-Z0-9_-]{3,20}$", username):
        return False, "Le nom d'utilisateur doit contenir entre 3 et 20 caractères (lettres, chiffres, _ ou -)"
    return True, ""

def register_user(username, password):
    """Enregistre un nouvel utilisateur"""
    try:
        # Valider le nom d'utilisateur et le mot de passe
        username_valid, username_error = validate_username(username)
        if not username_valid:
            return {'success': False, 'error': username_error}
            
        password_valid, password_error = validate_password(password)
        if not password_valid:
            return {'success': False, 'error': password_error}
        
        client = get_sheets_client()
        if client is None:
            return {'success': False, 'error': 'Erreur de configuration Google Sheets'}
            
        spreadsheet = client.open_by_key(SPREADSHEET_ID)
        worksheet = spreadsheet.worksheet(WORKSHEET_USERS)
        
        # Vérifier si le nom d'utilisateur existe déjà
        records = worksheet.get_all_records()
        if any(r['username'] == username for r in records):
            return {'success': False, 'error': 'Ce nom d\'utilisateur existe déjà'}
        
        # Générer un nouvel ID
        new_id = str(len(records) + 1)
        
        # Ajouter le nouvel utilisateur
        worksheet.append_row([new_id, username, password])
        
        return {
            'success': True,
            'user_id': new_id,
            'username': username
        }
        
    except Exception as e:
        print(f"Erreur lors de l'enregistrement : {e}")
        return {'success': False, 'error': str(e)}

def get_questions_by_stage(stage):
    """Récupère les questions pour un niveau spécifique"""
    try:
        client = get_sheets_client()
        if client is None:
            return []
            
        spreadsheet = client.open_by_key(SPREADSHEET_ID)
        try:
            worksheet = spreadsheet.worksheet(WORKSHEET_QUESTIONS)
        except gspread.WorksheetNotFound:
            print(f"Erreur : L'onglet '{WORKSHEET_QUESTIONS}' n'existe pas")
            return []
            
        records = worksheet.get_all_records()
        if not records:
            return []
            
        # Filtrer les questions par niveau
        stage_questions = [q for q in records if str(q.get('stage', '')) == str(stage)]
        
        return stage_questions
    except Exception as e:
        print(f"Erreur lors de la récupération des questions : {e}")
        return []

def add_question(stage, question, option_a, option_b, option_c, option_d, correct_answer):
    """Ajoute une nouvelle question"""
    try:
        client = get_sheets_client()
        if client is None:
            return False
            
        spreadsheet = client.open_by_key(SPREADSHEET_ID)
        try:
            worksheet = spreadsheet.worksheet(WORKSHEET_QUESTIONS)
        except gspread.WorksheetNotFound:
            worksheet = spreadsheet.add_worksheet(WORKSHEET_QUESTIONS, 1000, 8)
            # Ajouter les en-têtes
            headers = ['stage', 'question', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_answer', 'id']
            worksheet.update('A1:H1', [headers])
            worksheet.format('A1:H1', {
                'textFormat': {'bold': True},
                'backgroundColor': {'red': 0.8, 'green': 0.8, 'blue': 0.8}
            })
        
        # Générer un nouvel ID
        records = worksheet.get_all_records()
        new_id = len(records) + 1
        
        # Ajouter la nouvelle question
        new_row = [stage, question, option_a, option_b, option_c, option_d, correct_answer, new_id]
        worksheet.append_row(new_row)
        
        return True
    except Exception as e:
        print(f"Erreur lors de l'ajout de la question : {e}")
        return False

def delete_question(question_id):
    """Supprime une question"""
    try:
        client = get_sheets_client()
        if client is None:
            return False
            
        spreadsheet = client.open_by_key(SPREADSHEET_ID)
        worksheet = spreadsheet.worksheet(WORKSHEET_QUESTIONS)
        
        # Trouver la ligne de la question
        records = worksheet.get_all_records()
        for idx, record in enumerate(records, start=2):  # start=2 car la première ligne est l'en-tête
            if str(record.get('id', '')) == str(question_id):
                worksheet.delete_row(idx)
                return True
        
        return False
    except Exception as e:
        print(f"Erreur lors de la suppression de la question : {e}")
        return False 