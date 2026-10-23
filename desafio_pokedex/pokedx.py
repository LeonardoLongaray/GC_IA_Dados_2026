from flask import Flask, jsonify
import requests

pokedex = []
pedido = requests.get('https://pokeapi.co/api/v2/pokemon?limit=50')

