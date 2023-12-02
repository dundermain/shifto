# main.py
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.popup import Popup
import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('users.db')
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                               (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                username TEXT,
                                email TEXT,
                                password TEXT,
                                dob TEXT,
                                primary_info TEXT)''')
        self.conn.commit()

    def insert_user(self, username, email, password, dob, primary_info):
        self.cursor.execute('INSERT INTO users (username, email, password, dob, primary_info) VALUES (?, ?, ?, ?, ?)',
                            (username, email, password, dob, primary_info))
        self.conn.commit()

    def get_user(self, username):
        self.cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        return self.cursor.fetchone()

    def close(self):
        self.conn.close()

class BuySellApp(App):
    def build(self):
        self.sm = ScreenManager()

        self.login_screen = LoginScreen(name='login')
        self.register_screen = RegisterScreen(name='register')
        self.buy_sell_screen = BuySellScreen(name='buy_sell')

        self.sm.add_widget(self.login_screen)
        self.sm.add_widget(self.register_screen)
        self.sm.add_widget(self.buy_sell_screen)

        return self.sm

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.db = Database()

        self.username_input = TextInput(hint_text='Username', multiline=False)
        self.password_input = TextInput(hint_text='Password', password=True, multiline=False)
        self.login_button = Button(text='Login', on_press=self.login)
        self.go_to_register_button = Button(text='Go to Register', on_press=self.go_to_register)

        self.layout = BoxLayout(orientation='vertical')
        self.layout.add_widget(Label(text='Login'))
        self.layout.add_widget(self.username_input)
        self.layout.add_widget(self.password_input)
        self.layout.add_widget(self.login_button)
        self.layout.add_widget(self.go_to_register_button)

        self.add_widget(self.layout)

    def login(self, instance):
        username = self.username_input.text
        password = self.password_input.text

        user_data = self.db.get_user(username)

        if user_data and user_data[3] == password:
            self.manager.current = 'buy_sell'
        else:
            self.show_popup('Invalid Login', 'Please check your username and password.')

    def go_to_register(self, instance):
        self.manager.current = 'register'

    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(None, None), size=(400, 200))
        popup.open()

class RegisterScreen(Screen):
    def __init__(self, **kwargs):
        super(RegisterScreen, self).__init__(**kwargs)
        self.db = Database()

        self.name_input = TextInput(hint_text='Name', multiline=False)
        self.email_input = TextInput(hint_text='Email', multiline=False)
        self.password_input = TextInput(hint_text='Password', password=True, multiline=False)
        self.dob_input = TextInput(hint_text='Date of Birth', multiline=False)
        self.primary_input = TextInput(hint_text='Primary Info', multiline=True)
        self.register_button = Button(text='Register', on_press=self.register)

        self.layout = BoxLayout(orientation='vertical')
        self.layout.add_widget(Label(text='Register'))
        self.layout.add_widget(self.name_input)
        self.layout.add_widget(self.email_input)
        self.layout.add_widget(self.password_input)
        self.layout.add_widget(self.dob_input)
        self.layout.add_widget(self.primary_input)
        self.layout.add_widget(self.register_button)

        self.add_widget(self.layout)

    def register(self, instance):
        name = self.name_input.text
        email = self.email_input.text
        password = self.password_input.text
        dob = self.dob_input.text
        primary_info = self.primary_input.text

        self.db.insert_user(name, email, password, dob, primary_info)
        self.manager.current = 'login'

class BuySellScreen(Screen):
    def __init__(self, **kwargs):
        super(BuySellScreen, self).__init__(**kwargs)
        self.db = Database()

        self.price_input = TextInput(hint_text='Price', multiline=False)
        self.image_input = TextInput(hint_text='Image URL', multiline=False)
        self.description_input = TextInput(hint_text='Description', multiline=True)
        self.sell_button = Button(text='Sell', on_press=self.sell)

        self.layout = BoxLayout(orientation='vertical')
        self.layout.add_widget(Label(text='Sell an Item'))
        self.layout.add_widget(self.price_input)
        self.layout.add_widget(self.image_input)
        self.layout.add_widget(self.description_input)
        self.layout.add_widget(self.sell_button)

        self.add_widget(self.layout)

    def sell(self, instance):
        price = self.price_input.text
        image_url = self.image_input.text
        description = self.description_input.text

        # Here you can insert the data into the database or perform any other actions needed.

if __name__ == '__main__':
    BuySellApp().run()
