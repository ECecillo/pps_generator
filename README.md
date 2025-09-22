(code et documentation généré à l'aide de Gemini)

# Script d'automatisation de génération de numéro PPS (Parcours de Prévention Santé) 🇫🇷

Ce projet contient un script Python conçu pour automatiser entièrement le processus de remplissage du formulaire "Parcours de Prévention Santé" (PPS) de la Fédération Française d'Athlétisme (FFA).

Le script simule le comportement d'un utilisateur naviguant à travers les différentes étapes du formulaire. Il gère automatiquement les sessions, les jetons de sécurité (CSRF), et soumet les informations requises à chaque étape.

À la fin du processus, le script récupère le **numéro d'attestation PPS** généré ainsi que le **lien de téléchargement du certificat PDF**, puis sauvegarde ce dernier sur votre ordinateur.

## Disclaimer

Je ne suis en aucun cas responsable de ce qui peux arriver avec l'utilisation de ce script.

Par ailleurs, je ne suis pas non plus certains de la légalité de ce dernier :shrug:

## Installation et Lancement

Pour exécuter ce script, il est recommandé d'utiliser un environnement virtuel Python pour isoler les dépendances. Ce guide utilise `pyenv` et `pyenv-virtualenv`.

1. **Créez un environnement virtuel**
    Ouvrez un terminal et exécutez la commande suivante pour créer un environnement nommé `pps-automation` (vous pouvez choisir un autre nom) :

    ```bash
    pyenv virtualenv 3.10.12 pps-automation
    ```

    *Note : Remplacez `3.10.12` par la version de Python que vous souhaitez utiliser.*

2. **Activez l'environnement virtuel**
    Pour commencer à utiliser l'environnement, activez-le avec :

    ```bash
    pyenv activate pps-automation
    ```

    Le nom de votre environnement devrait maintenant apparaître dans votre invite de commande.

3. **Installez les dépendances**
    Ce script nécessite les bibliothèques `requests` et `beautifulsoup4`. Installez-les simplement via `pip` :

    ```bash
    pip install requests beautifulsoup4
    ```

---

## Lancement et Configuration

Il y a deux façons de fournir vos informations au script.

### 1\. Mode Interactif (Recommandé)

C'est la méthode la plus simple. Lancez simplement le script :

```bash
python pps_script.py
```

Le script vous demandera si vous souhaitez saisir vos informations manuellement. Répondez `o` (oui). Il vous demandera alors de saisir **la date de la course** (au format AAAA-MM-JJ), puis vos **informations personnelles**.

### 2\. Modification Directe du Code

Si vous préférez ne pas saisir vos informations à chaque fois, vous pouvez les inscrire directement dans le code.

Ouvrez le fichier du script et modifiez les variables par défaut au début de la fonction `get_user_inputs()` :

```python
def get_user_inputs():
    # --- Valeurs par défaut (peuvent être modifiées directement ici) ---
    default_race_date = "2025-12-25"  # Format AAAA-MM-JJ
    default_user_data = {
        "gender": "female",
        "last_name": "DUPONT",
        "first_name": "MARIE",
        "birth_day": "22",
        "birth_month": "10",
        "birth_year": "1992",
        "email": "marie.dupont@exemple.com"
    }
    # -----------------------------------------------------------------
    # ...
```

Lorsque vous lancerez le script, répondez `n` (non) à la première question pour qu'il utilise ces informations par défaut.

## Note

J'ai remarqué que si la date de la course est trop éloigné, le service renvoie des erreurs au moment de la génération du PPS.

Pour cela, je vous invite à mettre une date de 2 mois maximum pour éviter tout effet de bord.
