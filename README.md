# ⚡ Pokémon Information App

A desktop graphical user interface (GUI) application built in Python using PyQt5. This app connects to the public [PokéAPI](https://pokeapi.co/) to fetch, parse, and display real-time data and official pixel sprites for any searched Pokémon.

This project was built as part of my programming portfolio to explore desktop UI design, network handling, and JSON data parsing.

## 🚀 Features

* **Live API Integration:** Fetches up-to-date stats directly from the PokéAPI.
* **Dynamic UI Updates:** Displays the Pokémon's name, height, weight, and abilities cleanly on screen.
* **Sprite Rendering:** Downloads and renders official front-facing pixel sprites dynamically using `QPixmap`.
* **Robust Error Handling:** Features comprehensive exception handling and an HTTP status code `match-case` block to gracefully catch connection drops, timeouts, and invalid inputs (404, 400, 500, etc.) without crashing.

## 🛠️ Tech Stack

* **Language:** Python 3.x
* **GUI Framework:** PyQt5
* **Networking:** Requests library
* **Data Source:** PokéAPI
