import requests
from bs4 import BeautifulSoup
import datetime
import os
import time

# --- Fonctions ---


def get_user_inputs():
    """
    Demande à l'utilisateur la date de la course et ses informations personnelles,
    ou utilise les valeurs par défaut du script.
    Retourne un tuple: (user_data_dict, race_date_str).
    """
    # --- Valeurs par défaut (peuvent être modifiées directement ici) ---
    default_race_date = "2025-10-05"  # Format AAAA-MM-JJ
    default_user_data = {
        "gender": "male",
        "last_name": "CECILLON",
        "first_name": "Dupont",
        "birth_day": "22",
        "birth_month": "08",
        "birth_year": "1990",
        "email": "votre.email@exemple.com",
    }
    # -----------------------------------------------------------------

    choice = (
        input("Voulez-vous saisir vos informations manuellement ? (o/n) : ")
        .lower()
        .strip()
    )

    if choice in ["o", "oui", "y", "yes"]:
        print("\n--- Saisie des informations ---")

        # Saisie de la date de la course avec validation
        while True:
            race_date_input = input("Date de la course (format AAAA-MM-JJ) : ")
            try:
                datetime.datetime.strptime(race_date_input, "%Y-%m-%d")
                race_date = race_date_input
                break
            except ValueError:
                print(
                    "Erreur : Le format de la date est incorrect. Veuillez utiliser AAAA-MM-JJ."
                )

        # Saisie des informations personnelles
        user_data = {}
        user_data["last_name"] = input("Nom de famille : ")
        user_data["first_name"] = input("Prénom : ")
        user_data["email"] = input("Email : ")
        while True:
            gender = input("Sexe (male/female) : ").lower()
            if gender in ["male", "female"]:
                user_data["gender"] = gender
                break
            else:
                print("Erreur : veuillez saisir 'male' ou 'female'.")
        user_data["birth_day"] = input("Jour de naissance (ex: 15) : ")
        user_data["birth_month"] = input("Mois de naissance (ex: 9) : ")
        user_data["birth_year"] = input("Année de naissance (ex: 1990) : ")
        print("----------------------------------------\n")
        return user_data, race_date
    else:
        print(
            f"\nUtilisation des informations par défaut :\n- Date de la course : {default_race_date}\n- Données personnelles : pré-remplies dans le script.\n"
        )
        return default_user_data, default_race_date


def get_tokens_and_update_session(soup, session):
    """Extrait les jetons et met à jour la session."""
    csrf_token = soup.find("meta", {"name": "csrf-token"})["content"]
    auth_token = soup.find("input", {"name": "authenticity_token"})["value"]
    session.headers.update({"X-CSRF-Token": csrf_token})
    return auth_token


# --- Programme Principal ---
session = requests.Session()
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
}
session.headers.update(headers)
BASE_URL = "https://pps.athle.fr"

try:
    # ## ÉTAPE 0 : Récupération des informations utilisateur
    user_data, race_date = get_user_inputs()

    # ## ÉTAPE 1 : Accès à la page d'accueil et soumission de la date
    print("➡️ Étape 1 : Accès à la page d'accueil et soumission de la date...")
    r_home = session.get(BASE_URL)
    r_home.raise_for_status()
    soup_home = BeautifulSoup(r_home.text, "html.parser")
    auth_token_home = soup_home.find("input", {"name": "authenticity_token"})["value"]
    r_personal_infos_page = session.post(
        f"{BASE_URL}/courses/wizards/race_date",
        data={
            "_method": "patch",
            "authenticity_token": auth_token_home,
            "course[race_date]": race_date,
            "button": "",
        },
    )
    r_personal_infos_page.raise_for_status()
    print(f"✅ Date de la course ({race_date}) soumise.")

    # ... Le reste du script est inchangé ...
    # (Le script continue avec les étapes 2 à 7 comme précédemment)
    print("\n➡️ Étape 2 : Soumission des informations personnelles...")
    soup_personal_infos = BeautifulSoup(r_personal_infos_page.text, "html.parser")
    auth_token_personal = get_tokens_and_update_session(soup_personal_infos, session)
    payload_personal_infos = {
        "_method": "patch",
        "authenticity_token": auth_token_personal,
        "course[gender]": user_data["gender"],
        "course[last_name]": user_data["last_name"],
        "course[first_name]": user_data["first_name"],
        "course[birthdate(3i)]": user_data["birth_day"],
        "course[birthdate(2i)]": user_data["birth_month"],
        "course[birthdate(1i)]": user_data["birth_year"],
        "course[email]": user_data["email"],
        "button": "",
    }
    r_cardio_page = session.post(
        f"{BASE_URL}/courses/wizards/personal_infos", data=payload_personal_infos
    )
    r_cardio_page.raise_for_status()
    print("✅ Informations personnelles soumises.")

    print("\n➡️ Étape 3 : Validation des risques cardiovasculaires...")
    soup_cardio = BeautifulSoup(r_cardio_page.text, "html.parser")
    auth_token_cardio = get_tokens_and_update_session(soup_cardio, session)
    payload_cardio = {
        "_method": "patch",
        "authenticity_token": auth_token_cardio,
        "course[cardiovascular_risks_video]": "1",
        "course[cardiovascular_risks_checkbox]": "1",
        "button": "",
    }
    r_risk_factors_page = session.post(
        f"{BASE_URL}/courses/wizards/cardiovascular_risks", data=payload_cardio
    )
    r_risk_factors_page.raise_for_status()
    print("✅ Formulaire des risques cardiovasculaires validé.")

    print("\n➡️ Étape 4 : Validation des facteurs de risque...")
    soup_risk_factors = BeautifulSoup(r_risk_factors_page.text, "html.parser")
    auth_token_risk = get_tokens_and_update_session(soup_risk_factors, session)
    payload_risk = {
        "_method": "patch",
        "authenticity_token": auth_token_risk,
        "course[risk_factors_video]": "1",
        "course[risk_factors_checkbox]": "1",
        "button": "",
    }
    r_precautions_page = session.post(
        f"{BASE_URL}/courses/wizards/risk_factors", data=payload_risk
    )
    r_precautions_page.raise_for_status()
    print("✅ Formulaire des facteurs de risque validé.")

    print("\n➡️ Étape 5 : Validation des précautions et recommandations...")
    soup_precautions = BeautifulSoup(r_precautions_page.text, "html.parser")
    auth_token_precautions = get_tokens_and_update_session(soup_precautions, session)
    payload_precautions = {
        "_method": "patch",
        "authenticity_token": auth_token_precautions,
        "course[precautions_video]": "1",
        "course[precautions_checkbox]": "1",
        "button": "",
    }
    r_finalization_page = session.post(
        f"{BASE_URL}/courses/wizards/precautions", data=payload_precautions
    )
    r_finalization_page.raise_for_status()
    print("✅ Formulaire des précautions validé.")

    print("\n➡️ Étape 6 : Finalisation du parcours...")
    soup_finalization = BeautifulSoup(r_finalization_page.text, "html.parser")
    auth_token_final = get_tokens_and_update_session(soup_finalization, session)
    payload_final = {
        "_method": "patch",
        "authenticity_token": auth_token_final,
        "course[finalization_checkbox]": "1",
        "course[ffa_newsletter]": "1",
        "button": "",
    }
    r_result_page = session.post(
        f"{BASE_URL}/courses/wizards/finalization", data=payload_final
    )
    r_result_page.raise_for_status()
    print("✅ Parcours finalisé.")

    print("\n➡️ Étape 7 : Extraction des résultats...")
    soup_result = BeautifulSoup(r_result_page.text, "html.parser")
    pps_number_div = soup_result.find(
        "div", string="Attestation PPS numéro :"
    ).find_next_sibling("div")
    pps_number = pps_number_div.find("div").text.strip()

    pdf_full_url = None
    polling_form = soup_result.find("turbo-frame", id="certificate_download").find(
        "form"
    )
    polling_url = BASE_URL + polling_form["action"]

    print("   - Attente de la génération du lien de téléchargement PDF...")
    for i in range(10):
        print(f"   - Tentative de récupération ({i + 1}/10)...")
        r_check_pdf = session.get(polling_url)
        soup_check_pdf = BeautifulSoup(r_check_pdf.text, "html.parser")
        pdf_link_tag = soup_check_pdf.find(
            "a", href=lambda href: href and "/rails/active_storage/" in href
        )

        if pdf_link_tag:
            pdf_full_url = pdf_link_tag["href"]
            print("   - Lien PDF trouvé !")
            break
        time.sleep(2)

    if not pdf_full_url:
        raise Exception("Impossible de récupérer le lien de téléchargement du PDF.")

    print("\n--- RÉSULTATS ---")
    print(f"📄 Numéro PPS obtenu : {pps_number}")
    print(f"🔗 Lien de téléchargement de l'attestation : {pdf_full_url}")

    print("\n➡️ Bonus : Téléchargement du fichier PDF...")
    r_pdf = session.get(pdf_full_url)
    r_pdf.raise_for_status()
    file_name = f"Attestation_PPS_{pps_number}.pdf"
    with open(file_name, "wb") as f:
        f.write(r_pdf.content)

    print(f"✅ Fichier PDF sauvegardé sous le nom : {os.path.abspath(file_name)}")
    print("\n🎉 Scénario terminé avec succès ! 🎉")

except requests.exceptions.RequestException as e:
    print(f"\n❌ Une erreur réseau est survenue: {e}")
except Exception as e:
    print(f"\n❌ Une erreur inattendue est survenue: {e}")
