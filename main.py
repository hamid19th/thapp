from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.textfield import MDTextField
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.properties import StringProperty, NumericProperty, DictProperty, BooleanProperty, ListProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from sheets_config import verify_credentials, get_user_by_id, save_score, get_top_scores, get_user_history, register_user, get_sheets_client, SPREADSHEET_ID, WORKSHEET_USERS
from kivymd.uix.spinner import MDSpinner
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import MDList, OneLineListItem, TwoLineIconListItem
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.scrollview import ScrollView
from kivymd.uix.gridlayout import MDGridLayout
from kivy.uix.image import Image
from kivymd.uix.fitimage import FitImage

KV = '''
<Tab>:
    MDFloatLayout:
        MDList:
            id: container
            pos_hint: {'center_x': .5, 'center_y': .5}

<LoginScreen>:
    MDBoxLayout:
        orientation: 'vertical'
        spacing: "20dp"
        padding: "50dp"
        pos_hint: {"center_x": 0.5, "center_y": 0.5}
        size_hint: 0.8, None
        height: self.minimum_height

        MDLabel:
            text: "Quiz Python"
            halign: "center"
            font_style: "H4"
            theme_text_color: "Primary"
            size_hint_y: None
            height: "60dp"

        FitImage:
            source: "python_logo.png"
            size_hint_y: None
            height: "100dp"
            allow_stretch: True

        Widget:
            size_hint_y: None
            height: "20dp"

        MDTextField:
            id: username
            hint_text: "Nom d'utilisateur"
            icon_right: "account"
            helper_text: "Entrez votre identifiant"
            helper_text_mode: "on_focus"
            required: True
            disabled: root.is_loading
            size_hint_y: None
            height: "48dp"

        MDTextField:
            id: password
            hint_text: "Mot de passe"
            icon_right: "eye-off"
            password: True
            helper_text: "Entrez votre mot de passe"
            helper_text_mode: "on_focus"
            required: True
            disabled: root.is_loading
            size_hint_y: None
            height: "48dp"
            on_icon_right: root.toggle_password_visibility()

        BoxLayout:
            orientation: 'horizontal'
            spacing: "10dp"
            size_hint_y: None
            height: "48dp"
            pos_hint: {"center_x": 0.5}

            MDSpinner:
                size_hint: None, None
                size: "24dp", "24dp"
                pos_hint: {'center_y': .5}
                active: root.is_loading
                color: app.theme_cls.primary_color

            MDRaisedButton:
                text: "Se connecter"
                pos_hint: {"center_x": 0.5}
                on_release: root.verify_login()
                disabled: root.is_loading
                size_hint_x: 1

        MDLabel:
            id: error_label
            text: ""
            theme_text_color: "Error"
            halign: "center"
            size_hint_y: None
            height: "30dp"

<RegisterScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: dp(20)
        spacing: dp(20)

        MDLabel:
            text: "Créer un compte"
            halign: "center"
            font_style: "H4"
            size_hint_y: None
            height: dp(60)

        MDCard:
            orientation: 'vertical'
            padding: dp(15)
            spacing: dp(10)
            size_hint: None, None
            size: root.width - dp(40), dp(350)
            pos_hint: {"center_x": .5, "center_y": .5}
            elevation: 4

            MDTextField:
                id: username
                hint_text: "Nom d'utilisateur"
                helper_text: "3-20 caractères (lettres, chiffres, _ ou -)"
                helper_text_mode: "on_error"
                disabled: root.is_loading

            MDTextField:
                id: password
                hint_text: "Mot de passe"
                helper_text: "Minimum 6 caractères"
                helper_text_mode: "on_error"
                password: True
                disabled: root.is_loading

            MDTextField:
                id: confirm_password
                hint_text: "Confirmer le mot de passe"
                helper_text: "Les mots de passe doivent correspondre"
                helper_text_mode: "on_error"
                password: True
                disabled: root.is_loading

            BoxLayout:
                orientation: 'horizontal'
                spacing: dp(10)
                size_hint_y: None
                height: dp(36)

                MDSpinner:
                    size_hint: None, None
                    size: dp(24), dp(24)
                    pos_hint: {'center_y': .5}
                    active: root.is_loading
                    color: app.theme_cls.primary_color

                MDRaisedButton:
                    text: "S'inscrire"
                    size_hint_x: 1
                    on_release: root.register()
                    disabled: root.is_loading

            MDRaisedButton:
                text: "Retour à la connexion"
                size_hint_x: 1
                on_release: root.manager.current = 'login'
                disabled: root.is_loading

            MDLabel:
                id: error_label
                text: ""
                theme_text_color: "Error"
                halign: "center"

<QuizScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: dp(20)
        spacing: dp(20)

        BoxLayout:
            size_hint_y: None
            height: dp(60)
            spacing: dp(10)

            MDLabel:
                text: f"Bienvenue {root.user_data.get('username', '')}"
                halign: "left"
                font_style: "H6"

            MDRaisedButton:
                text: "Déconnexion"
                size_hint: None, None
                size: dp(120), dp(40)
                pos_hint: {'center_y': .5}
                on_release: root.logout()

        MDLabel:
            text: "Quiz Python"
            halign: "center"
            font_style: "H4"
            size_hint_y: None
            height: dp(60)

        MDCard:
            orientation: 'vertical'
            padding: dp(15)
            spacing: dp(10)
            size_hint: None, None
            size: root.width - dp(40), root.height - dp(260)
            pos_hint: {"center_x": .5, "center_y": .5}
            elevation: 4

            MDLabel:
                id: question_label
                text: root.current_question
                halign: "center"
                size_hint_y: None
                height: dp(100)
                font_style: "H6"

            BoxLayout:
                orientation: 'vertical'
                spacing: dp(10)
                
                MDRaisedButton:
                    text: root.option_a
                    size_hint_x: 1
                    on_release: root.check_answer("A")

                MDRaisedButton:
                    text: root.option_b
                    size_hint_x: 1
                    on_release: root.check_answer("B")

                MDRaisedButton:
                    text: root.option_c
                    size_hint_x: 1
                    on_release: root.check_answer("C")

                MDRaisedButton:
                    text: root.option_d
                    size_hint_x: 1
                    on_release: root.check_answer("D")

        BoxLayout:
            size_hint_y: None
            height: dp(50)
            spacing: dp(10)

            MDLabel:
                text: f"Niveau {root.current_stage} - Score: {root.score}"
                halign: "center"
                font_style: "H6"

            MDLabel:
                text: f"Question: {root.current_question_num}/{len(root.questions) if root.questions else 0}"
                halign: "center"
                font_style: "H6"

<ScoreDialog>:
    orientation: 'vertical'
    spacing: dp(10)
    size_hint_y: None
    height: dp(400)

    MDTabs:
        Tab:
            title: 'Meilleurs Scores'
            MDList:
                id: top_scores_list
        
        Tab:
            title: 'Mon Historique'
            MDList:
                id: history_list

<AdminScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: dp(20)
        spacing: dp(20)

        BoxLayout:
            size_hint_y: None
            height: dp(60)
            spacing: dp(10)

            MDLabel:
                text: "Panel Administrateur"
                halign: "left"
                font_style: "H6"

            MDRaisedButton:
                text: "Déconnexion"
                size_hint: None, None
                size: dp(120), dp(40)
                pos_hint: {'center_y': .5}
                on_release: root.logout()

        MDTabs:
            id: tabs
            
            Tab:
                title: 'Ajouter Utilisateur'
                
                BoxLayout:
                    orientation: 'vertical'
                    padding: dp(20)
                    spacing: dp(10)
                    pos_hint: {'center_x': .5, 'center_y': .5}
                    size_hint: .8, .8

                    MDTextField:
                        id: new_username
                        hint_text: "Nom d'utilisateur"
                        helper_text: "3-20 caractères (lettres, chiffres, _ ou -)"
                        helper_text_mode: "on_error"

                    MDTextField:
                        id: new_password
                        hint_text: "Mot de passe"
                        helper_text: "Minimum 6 caractères"
                        helper_text_mode: "on_error"
                        password: True

                    MDRaisedButton:
                        text: "Ajouter l'utilisateur"
                        size_hint_x: 1
                        on_release: root.add_user()

                    MDLabel:
                        id: add_user_status
                        text: ""
                        theme_text_color: "Error"
                        halign: "center"
            
            Tab:
                title: 'Liste des Utilisateurs'
                
                ScrollView:
                    MDList:
                        id: users_list
                        padding: dp(10)
            
            Tab:
                title: 'Statistiques'
                
                ScrollView:
                    MDList:
                        id: stats_list
                        padding: dp(10)

<StageSelectionScreen>:
    BoxLayout:
        orientation: 'vertical'
        spacing: dp(20)
        padding: dp(20)

        MDTopAppBar:
            title: "Sélection du Niveau"
            left_action_items: [["arrow-left", lambda x: root.logout()]]
            elevation: 4
            md_bg_color: app.theme_cls.primary_color

        ScrollView:
            MDGridLayout:
                cols: 1
                spacing: dp(20)
                padding: dp(20)
                size_hint_y: None
                height: self.minimum_height

                MDLabel:
                    text: f"Bienvenue {root.username}"
                    halign: "center"
                    font_style: "H5"
                    size_hint_y: None
                    height: dp(50)

                Widget:
                    size_hint_y: None
                    height: dp(20)

                MDCard:
                    orientation: 'vertical'
                    padding: dp(15)
                    spacing: dp(10)
                    size_hint: None, None
                    size: min(root.width - dp(40), dp(400)), dp(80)
                    pos_hint: {"center_x": .5}
                    elevation: 2
                    md_bg_color: app.theme_cls.primary_color
                    on_release: root.start_stage(1)

                    MDLabel:
                        text: root.stage_titles.get(1, "Niveau 1")
                        halign: "center"
                        theme_text_color: "Custom"
                        text_color: 1, 1, 1, 1
                        font_style: "H6"

                    MDLabel:
                        text: root.stage_descriptions.get(1, "")
                        halign: "center"
                        theme_text_color: "Custom"
                        text_color: 1, 1, 1, 0.8

                MDCard:
                    orientation: 'vertical'
                    padding: dp(15)
                    spacing: dp(10)
                    size_hint: None, None
                    size: min(root.width - dp(40), dp(400)), dp(80)
                    pos_hint: {"center_x": .5}
                    elevation: 2
                    md_bg_color: app.theme_cls.primary_dark
                    on_release: root.start_stage(2)

                    MDLabel:
                        text: root.stage_titles.get(2, "Niveau 2")
                        halign: "center"
                        theme_text_color: "Custom"
                        text_color: 1, 1, 1, 1
                        font_style: "H6"

                    MDLabel:
                        text: root.stage_descriptions.get(2, "")
                        halign: "center"
                        theme_text_color: "Custom"
                        text_color: 1, 1, 1, 0.8

                MDCard:
                    orientation: 'vertical'
                    padding: dp(15)
                    spacing: dp(10)
                    size_hint: None, None
                    size: min(root.width - dp(40), dp(400)), dp(80)
                    pos_hint: {"center_x": .5}
                    elevation: 2
                    md_bg_color: app.theme_cls.primary_light
                    on_release: root.start_stage(3)

                    MDLabel:
                        text: root.stage_titles.get(3, "Niveau 3")
                        halign: "center"
                        theme_text_color: "Custom"
                        text_color: 1, 1, 1, 1
                        font_style: "H6"

                    MDLabel:
                        text: root.stage_descriptions.get(3, "")
                        halign: "center"
                        theme_text_color: "Custom"
                        text_color: 1, 1, 1, 0.8

                MDCard:
                    orientation: 'vertical'
                    padding: dp(15)
                    spacing: dp(10)
                    size_hint: None, None
                    size: min(root.width - dp(40), dp(400)), dp(80)
                    pos_hint: {"center_x": .5}
                    elevation: 2
                    md_bg_color: app.theme_cls.accent_color
                    on_release: root.start_stage(4)

                    MDLabel:
                        text: root.stage_titles.get(4, "Niveau 4")
                        halign: "center"
                        theme_text_color: "Custom"
                        text_color: 1, 1, 1, 1
                        font_style: "H6"

                    MDLabel:
                        text: root.stage_descriptions.get(4, "")
                        halign: "center"
                        theme_text_color: "Custom"
                        text_color: 1, 1, 1, 0.8

                MDCard:
                    orientation: 'vertical'
                    padding: dp(15)
                    spacing: dp(10)
                    size_hint: None, None
                    size: min(root.width - dp(40), dp(400)), dp(80)
                    pos_hint: {"center_x": .5}
                    elevation: 2
                    md_bg_color: app.theme_cls.accent_dark
                    on_release: root.start_stage(5)

                    MDLabel:
                        text: root.stage_titles.get(5, "Niveau 5")
                        halign: "center"
                        theme_text_color: "Custom"
                        text_color: 1, 1, 1, 1
                        font_style: "H6"

                    MDLabel:
                        text: root.stage_descriptions.get(5, "")
                        halign: "center"
                        theme_text_color: "Custom"
                        text_color: 1, 1, 1, 0.8
'''

class Tab(MDFloatLayout, MDTabsBase):
    """Class implementing content for a tab."""
    pass

class StageSelectionScreen(Screen):
    username = StringProperty("")
    stage_titles = DictProperty({})
    stage_descriptions = DictProperty({})

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'stage_selection'
        self.load_stage_titles()

    def load_stage_titles(self):
        """Charge les titres et descriptions des stages depuis Google Sheets"""
        try:
            client = get_sheets_client()
            if not client:
                return
            
            spreadsheet = client.open_by_key(SPREADSHEET_ID)
            worksheet = spreadsheet.worksheet('Questions')
            data = worksheet.get_all_records()
            
            # Initialiser les dictionnaires
            titles = {}
            descriptions = {}
            
            # Parcourir les données pour extraire les titres uniques par niveau
            for row in data:
                stage = row.get('stage', 0)
                if stage > 0 and stage not in titles:
                    # Utiliser directement les colonnes titre_niveau et description_niveau
                    titles[stage] = row.get('titre_niveau', f"Niveau {stage}")
                    descriptions[stage] = row.get('description_niveau', "")
            
            # S'assurer que tous les niveaux ont un titre et une description
            for stage in range(1, 6):
                if stage not in titles:
                    titles[stage] = f"Niveau {stage}"
                    descriptions[stage] = "Contenu à venir"
            
            self.stage_titles = titles
            self.stage_descriptions = descriptions
            
        except Exception as e:
            print(f"Erreur lors du chargement des titres : {e}")
            # Utiliser des titres par défaut en cas d'erreur
            self.stage_titles = {
                1: "Niveau 1 - Introduction à Python",
                2: "Niveau 2 - Structures de Données",
                3: "Niveau 3 - Programmation Avancée",
                4: "Niveau 4 - Programmation Orientée Objet",
                5: "Niveau 5 - Projets et Applications"
            }
            self.stage_descriptions = {
                1: "Premiers pas en programmation Python",
                2: "Listes, dictionnaires et manipulation des données",
                3: "Boucles, conditions et fonctions",
                4: "Classes, objets et héritage",
                5: "Création d'applications complètes"
            }

    def on_enter(self, *args):
        """Called when the screen is displayed"""
        if hasattr(self, 'user_data'):
            self.username = self.user_data.get('username', '')
        self.load_stage_titles()

    def start_stage(self, stage):
        """Start the selected stage"""
        self.manager.current = 'quiz'
        quiz_screen = self.manager.get_screen('quiz')
        quiz_screen.user_data = self.user_data
        quiz_screen.start_stage(stage)

    def logout(self):
        """Return to login screen"""
        self.manager.current = 'login'

class LoginScreen(Screen):
    is_loading = BooleanProperty(False)

    def verify_login(self):
        username = self.ids.username.text
        password = self.ids.password.text
        
        if not username or not password:
            self.ids.error_label.text = "Veuillez remplir tous les champs"
            return
        
        self.is_loading = True
        self.ids.error_label.text = ""
        
        result = verify_credentials(username, password)
        self.is_loading = False
        
        if result['success']:
            if result.get('is_admin', False):
                self.manager.current = 'admin'
            else:
                stage_screen = self.manager.get_screen('stage_selection')
                stage_screen.user_data = {
                'user_id': result['user_id'],
                'username': result['username']
            }
                self.manager.current = 'stage_selection'
            self.reset_fields()
        else:
            self.ids.error_label.text = result.get('error', 'Erreur de connexion')

    def reset_fields(self):
        """Réinitialise les champs du formulaire"""
        self.ids.error_label.text = ""
        self.ids.username.text = ""
        self.ids.password.text = ""

    def toggle_password_visibility(self):
        """Bascule la visibilité du mot de passe"""
        password_field = self.ids.password
        password_field.password = not password_field.password
        password_field.icon_right = "eye" if password_field.password else "eye-off"

class QuizScreen(Screen):
    current_question = StringProperty("")
    option_a = StringProperty("")
    option_b = StringProperty("")
    option_c = StringProperty("")
    option_d = StringProperty("")
    score = NumericProperty(0)
    current_question_num = NumericProperty(1)
    current_stage = NumericProperty(1)
    user_data = DictProperty({})
    questions = ListProperty([])
    score_dialog = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_index = 0

    def start_stage(self, stage):
        """Démarre un niveau spécifique"""
        self.current_stage = stage
        self.score = 0
        self.current_index = 0
        self.current_question_num = 1
        
        # Charger les questions depuis Google Sheets
        from sheets_config import get_questions_by_stage
        self.questions = get_questions_by_stage(stage)
        
        if not self.questions:
            # S'il n'y a pas de questions, afficher un message d'erreur
            error_dialog = MDDialog(
                title="Erreur",
                text="Impossible de charger les questions pour ce niveau.",
                buttons=[
                    MDRaisedButton(
                        text="Retour",
                        on_release=lambda x: self.return_to_selection(error_dialog)
                    )
                ]
            )
            error_dialog.open()
            return
            
        self.load_question()

    def return_to_selection(self, dialog):
        """Retourne à l'écran de sélection des niveaux"""
        dialog.dismiss()
        self.manager.current = 'stage_selection'

    def load_question(self):
        """Charge la question courante"""
        if self.current_index < len(self.questions):
            question = self.questions[self.current_index]
            # Convertir toutes les valeurs en chaînes de caractères
            self.current_question = str(question.get("question", ""))
            self.option_a = str(question.get("option_a", ""))
            self.option_b = str(question.get("option_b", ""))
            self.option_c = str(question.get("option_c", ""))
            self.option_d = str(question.get("option_d", ""))
        else:
            self.show_final_score()

    def check_answer(self, selected_option):
        """Vérifie la réponse sélectionnée"""
        if self.current_index < len(self.questions):
            correct_answer = str(self.questions[self.current_index].get("correct_answer", ""))
            if selected_option == correct_answer:
                self.score += 1
            self.current_index += 1
            self.current_question_num += 1
            self.load_question()

    def show_final_score(self):
        # Sauvegarder le score
        success = save_score(
            self.user_data['user_id'],
            self.user_data['username'],
            self.score,
            len(self.questions)
        )
        
        # Récupérer les scores
        top_scores = get_top_scores()
        user_history = get_user_history(self.user_data['user_id'])
        
        # Créer et afficher le dialogue des scores
        if not self.score_dialog:
            score_content = ScoreDialog()
            self.score_dialog = MDDialog(
                title=f"Résultats - Niveau {self.current_stage}",
                type="custom",
                content_cls=score_content,
                buttons=[
                    MDRaisedButton(
                        text="Changer de niveau",
                        on_release=lambda x: self.change_stage()
                    ),
                    MDRaisedButton(
                        text="Rejouer",
                        on_release=lambda x: self.restart_quiz()
                    ),
                    MDRaisedButton(
                        text="Quitter",
                        on_release=lambda x: self.logout()
                    )
                ]
            )
        else:
            self.score_dialog.title = f"Résultats - Niveau {self.current_stage}"
        
        # Mettre à jour les scores dans le dialogue
        self.score_dialog.content_cls.update_scores(top_scores, user_history)
        
        # Afficher le dialogue
        self.score_dialog.open()

    def change_stage(self):
        """Change de niveau"""
        if self.score_dialog:
            self.score_dialog.dismiss()
        self.manager.current = 'stage_selection'

    def restart_quiz(self):
        """Redémarre le niveau actuel"""
        if self.score_dialog:
            self.score_dialog.dismiss()
        self.start_stage(self.current_stage)

    def logout(self):
        """Déconnexion"""
        if self.score_dialog:
            self.score_dialog.dismiss()
        self.manager.current = 'login'
        self.score = 0
        self.current_index = 0
        self.current_question_num = 1
        self.current_stage = 1

class ScoreDialog(BoxLayout):
    def update_scores(self, top_scores, user_history):
        # Mettre à jour les meilleurs scores
        top_scores_list = self.ids.top_scores_list
        top_scores_list.clear_widgets()
        for score in top_scores:
            text = f"{score['username']} - {score['score']}/{score['total_questions']} ({score['pourcentage']})"
            top_scores_list.add_widget(OneLineListItem(text=text))

        # Mettre à jour l'historique
        history_list = self.ids.history_list
        history_list.clear_widgets()
        for score in user_history:
            text = f"{score['date']} - Score: {score['score']}/{score['total_questions']} ({score['pourcentage']})"
            history_list.add_widget(OneLineListItem(text=text))

class AdminScreen(Screen):
    def on_enter(self):
        """Appelé quand l'écran devient actif"""
        self.load_users_list()
        self.load_statistics()
    
    def load_users_list(self):
        """Charge la liste des utilisateurs"""
        users_list = self.ids.users_list
        users_list.clear_widgets()
        
        client = get_sheets_client()
        if not client:
            return
            
        try:
            spreadsheet = client.open_by_key(SPREADSHEET_ID)
            worksheet = spreadsheet.worksheet(WORKSHEET_USERS)
            records = worksheet.get_all_records()
            
            for record in records:
                item = TwoLineIconListItem(
                    text=f"Utilisateur: {record['username']}",
                    secondary_text=f"ID: {record['id']}"
                )
                users_list.add_widget(item)
        except Exception as e:
            print(f"Erreur lors du chargement des utilisateurs : {e}")
    
    def load_statistics(self):
        """Charge les statistiques globales"""
        stats_list = self.ids.stats_list
        stats_list.clear_widgets()
        
        try:
            # Récupérer tous les scores
            scores = get_top_scores(limit=100)  # On prend plus de scores pour les stats
            
            if scores:
                # Nombre total de quiz
                total_quizzes = len(scores)
                stats_list.add_widget(OneLineListItem(
                    text=f"Nombre total de quiz : {total_quizzes}"
                ))
                
                # Score moyen
                avg_score = sum(float(s['score']) for s in scores) / total_quizzes
                stats_list.add_widget(OneLineListItem(
                    text=f"Score moyen : {avg_score:.1f}"
                ))
                
                # Meilleur score
                best_score = max(scores, key=lambda x: float(x['score']))
                stats_list.add_widget(OneLineListItem(
                    text=f"Meilleur score : {best_score['score']} par {best_score['username']}"
                ))
        except Exception as e:
            print(f"Erreur lors du chargement des statistiques : {e}")
    
    def add_user(self):
        """Ajoute un nouvel utilisateur"""
        username = self.ids.new_username.text
        password = self.ids.new_password.text
        
        result = register_user(username, password)
        
        if result['success']:
            self.ids.add_user_status.text = "✓ Utilisateur ajouté avec succès"
            self.ids.add_user_status.theme_text_color = "Success"
            self.ids.new_username.text = ""
            self.ids.new_password.text = ""
            self.load_users_list()  # Rafraîchir la liste
        else:
            self.ids.add_user_status.text = result.get('error', "Erreur lors de l'ajout")
            self.ids.add_user_status.theme_text_color = "Error"
    
    def logout(self):
        """Déconnexion et retour à l'écran de login"""
        self.manager.current = 'login'

class QuizApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.accent_palette = "Teal"
        self.theme_cls.theme_style = "Light"
        Builder.load_string(KV)
        
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(StageSelectionScreen(name='stage_selection'))
        sm.add_widget(QuizScreen(name='quiz'))
        sm.add_widget(AdminScreen(name='admin'))
        return sm

if __name__ == '__main__':
    QuizApp().run() 