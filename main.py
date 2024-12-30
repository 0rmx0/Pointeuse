import csv
from datetime import datetime
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout


class TimeTrackerApp(App):
    def build(self):
        self.entries = []  # Liste pour stocker les heures
        self.main_layout = BoxLayout(orientation="vertical", padding=10, spacing=10)

        # Champs pour la saisie
        self.start_time_input = TextInput(hint_text="Heure de début (HH:mm)", multiline=False)
        self.end_time_input = TextInput(hint_text="Heure de fin (HH:mm)", multiline=False)
        self.main_layout.add_widget(self.start_time_input)
        self.main_layout.add_widget(self.end_time_input)

        # Boutons
        button_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
        add_button = Button(text="Ajouter")
        export_button = Button(text="Exporter CSV")
        add_button.bind(on_press=self.add_entry)
        export_button.bind(on_press=self.export_to_csv)
        button_layout.add_widget(add_button)
        button_layout.add_widget(export_button)
        self.main_layout.add_widget(button_layout)

        # Historique des entrées
        self.history_layout = GridLayout(cols=2, size_hint_y=None, spacing=10)
        self.history_layout.bind(minimum_height=self.history_layout.setter("height"))
        scroll_view = ScrollView(size_hint=(1, 1))
        scroll_view.add_widget(self.history_layout)
        self.main_layout.add_widget(scroll_view)

        return self.main_layout

    def add_entry(self, instance):
        """Ajoute une nouvelle entrée."""
        start_time = self.start_time_input.text.strip()
        end_time = self.end_time_input.text.strip()

        if self.validate_time(start_time) and self.validate_time(end_time):
            self.entries.append((start_time, end_time))
            self.history_layout.add_widget(Label(text=start_time))
            self.history_layout.add_widget(Label(text=end_time))
            self.start_time_input.text = ""
            self.end_time_input.text = ""
        else:
            print("Format d'heure invalide. Utilisez HH:mm.")

    def validate_time(self, time_str):
        """Valide le format HH:mm."""
        try:
            datetime.strptime(time_str, "%H:%M")
            return True
        except ValueError:
            return False

    def export_to_csv(self, instance):
        """Exporte les données en CSV."""
        file_path = "timesheet.csv"
        try:
            with open(file_path, "w", newline="") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["Heure de début", "Heure de fin"])
                writer.writerows(self.entries)
            print(f"Fichier exporté : {file_path}")
        except Exception as e:
            print(f"Erreur lors de l'export : {e}")


if __name__ == "__main__":
    TimeTrackerApp().run()
