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
    "boto3",
    "textblob",
    "nltk",
    "textblob-fr",
    "langdetect",
    "matplotlib",
    "seaborn"
)


foreach ($dep in $dependencies) {
    Write-Host "Installation de $dep..."
    pipenv install $dep
}

# Installer le package local
Write-Host "Installation du package local..."
pipenv install -e ./src

# Initialiser NLTK avant l'exécution
Write-Host "Initialisation des ressources NLTK..."
pipenv run python -c @"
import nltk
resources = ['punkt', 'stopwords', 'averaged_perceptron_tagger', 'words']
for resource in resources:
    try:
        nltk.download(resource, quiet=True)
        print(f'Téléchargement réussi de {resource}')
    except Exception as e:
        print(f'Erreur lors du téléchargement de {resource}: {str(e)}')
"@

# Créer event.json pour l'analyse complète
$eventPath = "src/event.json"
Write-Host "Création du fichier event.json..."
@{
    operation = "analyze_all"
    max_restaurants = 100
} | ConvertTo-Json | Out-File -FilePath $eventPath -Encoding UTF8

# Exécuter la fonction
Write-Host "Test de la fonction..."
pipenv run amplify mock function analyzeReviews --event "src/event.json" --timeout 900 
