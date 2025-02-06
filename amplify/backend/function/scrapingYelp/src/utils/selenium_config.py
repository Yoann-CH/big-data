from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager

import os
import platform

def get_driver():
    firefox_options = Options()
    
    # Configuration de base
    if os.getenv('AWS_LAMBDA_FUNCTION_NAME'):
        # Mode headless uniquement sur Lambda
        firefox_options.add_argument('--headless')
        firefox_options.add_argument('--no-sandbox')
        firefox_options.add_argument('--disable-dev-shm-usage')
    
    # Définir le chemin de Firefox selon le système d'exploitation
    if platform.system() == 'Windows':
        firefox_paths = [
            r"C:\Program Files\Mozilla Firefox\firefox.exe",
            r"C:\Program Files (x86)\Mozilla Firefox\firefox.exe",
            os.path.expanduser(r"~\AppData\Local\Mozilla Firefox\firefox.exe")
        ]
        
        for path in firefox_paths:
            if os.path.exists(path):
                firefox_options.binary_location = path
                break
        else:
            raise Exception("Firefox n'est pas installé. Veuillez l'installer depuis https://www.mozilla.org/fr/firefox/new/")
    
    # Configuration du token GitHub pour GeckoDriverManager
    os.environ['GH_TOKEN'] = ''  # À remplacer par votre token
    
    # Utiliser GeckoDriverManager avec le token
    service = Service(GeckoDriverManager().install())
    
    # Configuration de la fenêtre en mode visible
    if not os.getenv('AWS_LAMBDA_FUNCTION_NAME'):
        firefox_options.add_argument('--width=1920')
        firefox_options.add_argument('--height=1080')
    
    return webdriver.Firefox(
        service=service,
        options=firefox_options
    )