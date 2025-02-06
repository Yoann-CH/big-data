# Définir la variable d'environnement
$env:PIPENV_IGNORE_VIRTUALENVS = "1"

# Chemin vers Python 3.8
$PYTHON_PATH = "C:\Users\$env:USERNAME\AppData\Local\Programs\Python\Python38\python.exe"

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
    "boto3"
)


foreach ($dep in $dependencies) {
    Write-Host "Installation de $dep..."
    pipenv install $dep
}

# Installer le package local
Write-Host "Installation du package local..."
pipenv install -e ./src
