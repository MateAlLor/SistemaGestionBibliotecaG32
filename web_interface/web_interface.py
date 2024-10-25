from flask import Flask, render_template, redirect, url_for, request
from utils.clases import Autor
import requests


def create_interface(app):
    # Ruta de Inicio
    @app.route('/front/home')
    def front_home():
        return render_template('home.html')
    
    # Rutas de Autores
    @app.route('/front/autores')
    def front_autores():
        return render_template('autores/menu.html')
    
    @app.route('/front/autores/registrar')
    def front_autores_registrar():
        return render_template('autores/registrar.html')
    
    @app.route('/front/autores/listar')
    def front_autores_listar():
        return render_template('autores/listar.html')
