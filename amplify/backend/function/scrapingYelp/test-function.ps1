# Définir la variable d'environnement
$env:PIPENV_IGNORE_VIRTUALENVS = "1"

# Chemin vers Python 3.8
$PYTHON_PATH = "C:\Users\yoann\AppData\Local\Programs\Python\Python38\python.exe"

# Supprimer l'environnement virtuel existant s'il existe
if (Test-Path ".venv") {
    Write-Host "Suppression de l'environnement virtuel existant..."
    pipenv --rm
}

# Créer un nouvel environnement virtuel
Write-Host "Création d'un nouvel environnement virtuel..."
pipenv --python 3.12

# Installer les dépendances
Write-Host "Installation des dépendances..."
$dependencies = @(
    "boto3",
    "selenium",
    "webdriver-manager",
    "bs4",
    "urllib3",
    "geckodriver-autoinstaller"
)

foreach ($dep in $dependencies) {
    Write-Host "Installation de $dep..."
    pipenv install $dep
}

# Installer le package local
Write-Host "Installation du package local..."
pipenv install -e ./src

# Créer event.json s'il n'existe pas
$eventPath = "src/event.json"
if (-not (Test-Path $eventPath)) {
    Write-Host "Création du fichier event.json..."
    @{
        operation = "restaurants_and_reviews"
        location = "Paris"
        max_restaurants = 10
        max_reviews_per_restaurant = 10
    } | ConvertTo-Json | Out-File -FilePath $eventPath -Encoding UTF8
}


# Exécuter la fonction
Write-Host "Test de la fonction..."
pipenv run amplify mock function scrapingYelp --event "src/event.json" --timeout 600 
