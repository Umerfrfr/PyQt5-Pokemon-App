import sys
from shlex import join

import requests
from PyQt5.QtWidgets import (QApplication,QLineEdit,QWidget,
                             QLabel,QPushButton,QVBoxLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap


class PokemonApp(QWidget):
    def __init__(self):
        super().__init__()
        self.pokemon_name=QLabel("Enter Pokemon Name",self)
        self.pokemon_input=QLineEdit(self)
        self.get_pokemon_button=QPushButton("Get Pokemon",self)
        self.sprite_label=QLabel(self)
        self.description=QLabel("Description",self)
        self.description_label=QLabel(self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Pokemon Information App")

        vbox=QVBoxLayout()

        vbox.addWidget(self.pokemon_name)
        vbox.addWidget(self.pokemon_input)
        vbox.addWidget(self.get_pokemon_button)
        vbox.addWidget(self.sprite_label)
        vbox.addWidget(self.description)
        vbox.addWidget(self.description_label)

        self.setLayout(vbox)

        self.pokemon_name.setAlignment(Qt.AlignCenter)
        self.pokemon_input.setAlignment(Qt.AlignCenter)
        self.sprite_label.setAlignment(Qt.AlignCenter)
        self.description.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)


        self.pokemon_name.setObjectName("pokemon_name")
        self.pokemon_input.setObjectName("pokemon_input")
        self.get_pokemon_button.setObjectName("get_pokemon_button")
        self.sprite_label.setObjectName("sprite_label")
        self.description.setObjectName("description")
        self.description_label.setObjectName("description_label")


        self.setStyleSheet("""
            QLabel,QPushButton{
                font-family:calibri;
            }
            QLabel#pokemon_name{
                font-size:40px;
                font-style:italic;
            }
            QLineEdit#pokemon_input{
                font-size:40px;            
            }
            QPushButton#get_pokemon_button{
                font-size:30px;
                font-weight:bold;
            }
            QLabel#sprite_label{
                font-size:100px;
                font-family:Segoe UI Font;
            }
            QLabel#description{
                font-size:55px;
                font-weight:bold;
            }
            QLabel#description_label{
                font-size:45px;
            }
        """)
        self.get_pokemon_button.clicked.connect(self.get_pokemon)


    def get_pokemon(self):
        base_url="https://pokeapi.co/api/v2/"
        pokemon=self.pokemon_input.text()
        url=f"{base_url}pokemon/{pokemon}"

        try:
            response=requests.get(url)
            response.raise_for_status()
            if response.status_code == 200:
                data=response.json()
                self.display_pokemon(data)
        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                    self.display_error("Bad Request\nPlease check your input")
                case 404:
                    self.display_error("Not Found\nPokemon not found")
                case 405:
                    self.display_error("Method not Allowed\nTry again")
                case 429:
                    self.display_error("Too Many Requests\nPlease try again later")
                case 500:
                    self.display_error("Not Found\nCity not found")
                case 503:
                    self.display_error("Service Unavailable\nServer is down")
                case _:
                    self.display_error(f"HTTP Error occured\n{http_error}")
        except requests.exceptions.ConnectionError:
            self.display_error("Connection Error\nCheck your internet connection")
        except requests.exceptions.Timeout:
            self.display_error("Timeout Error\nThe request timed out")
        except requests.exceptions.TooManyRedirects:
            self.display_error("Too Many Redirects\nCheck the URL")
        except requests.exceptions.RequestException as req_error:
            self.display_error(f"Request Error\n{req_error}")
        except Exception as e:
            # This will catch ANY other unexpected error and print it to your console instead of crashing!
            print(f"CRITICAL ERROR: {e}")
            self.display_error("An unexpected error occurred.")

    def display_error(self,message):
        self.description_label.setStyleSheet("font-size:30px;")
        self.description_label.setText(message)


    def display_pokemon(self,data):
        self.description_label.setStyleSheet("font-size:45px;")
        description1=data['name']
        description2=data['height']
        description3=data['weight']
        abilities_list=data.get('abilities',[])
        description4=[item['ability']['name'] for item in abilities_list]
        abilities_str=",".join(description4)
        self.description_label.setText(f"{description1.capitalize()}|{description2}cm|{description3}N|{abilities_str}")
        try:
            sprite_url = data['sprites']['front_default']
            if sprite_url:
                image_data = requests.get(sprite_url).content
                pixmap = QPixmap()
                pixmap.loadFromData(image_data)
                self.sprite_label.setPixmap(pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            else:
                self.sprite_label.clear()
        except Exception as e:
            print(f"Could not load sprite: {e}")
            self.sprite_label.clear()





if __name__=="__main__":
    app=QApplication(sys.argv)
    pokemon=PokemonApp()
    pokemon.show()
    sys.exit(app.exec_())
