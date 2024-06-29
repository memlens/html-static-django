from bs4 import BeautifulSoup
import os

def ouvrirFichier(nom_fichier, mode, contenu_a_ecrire=None):
    """
    Ouvre un fichier en mode lecture ('r') ou écriture ('w').

    Args:
        nom_fichier (str): Le nom du fichier à ouvrir.
        mode (str): Le mode d'ouverture, soit 'r' pour lecture ou 'w' pour écriture.
        contenu_a_ecrire (str, optional): Le contenu à écrire dans le fichier, si le mode est 'w'.

    Returns:
        str: Le contenu du fichier si le mode est 'r'.
        int: Le nombre d'octets écrits si le mode est 'w'.
        None: En cas d'erreur ou si le mode est incorrect.
    """
    file_content = None

    if mode == 'r':
        try:
            with open(nom_fichier, mode, encoding='utf-8') as reading_file:
                file_content = reading_file.read()
        except FileNotFoundError:
            print(f"Erreur : Le fichier '{nom_fichier}' n'a pas été trouvé.")
        except IOError as e:
            print(f"Erreur : Problème d'entrée/sortie avec le fichier '{nom_fichier}': {e}")
    elif mode == 'w':
        if contenu_a_ecrire is None:
            print("Erreur : Vous devez fournir du contenu à écrire dans le fichier.")
            return None
        try:
            with open(nom_fichier, mode, encoding='utf-8') as writing_file:
                file_content = writing_file.write(contenu_a_ecrire)
        except IOError as e:
            print(f"Erreur : Problème d'entrée/sortie avec le fichier '{nom_fichier}': {e}")
    else:
        print("Votre entrée n'est pas prise en compte, il faut choisir entre 'r' et 'w'.")

    return file_content


def balisesAModifier():
    """
    Interroge l'utilisateur pour savoir quelles balises HTML parmi 'link', 'img' et 'script' 
    doivent être modifiées. 
    L'utilisateur répond 'y' pour yes ou 'n' pour no.

    Returns:
        dict: Un dictionnaire des balises à modifier et leurs attributs associés, choisis par l'utilisateur.
    """
    les_balises = {
        'link': 'href',
        'img': 'src',
        'script': 'src'
    }
    balises_a_modifier = {}

    print("Répondez avec 'y' pour yes et 'n' pour no. Tapez 'q' pour quitter.")
    
    for balise, attribut in les_balises.items():
        while True:
            try:
                reponse = input(f"Voulez-vous modifier la balise '{balise}' avec l'attribut '{attribut}' ? (y/n/q pour quitter) ").lower()
                if reponse == 'y':
                    balises_a_modifier[balise] = attribut
                    break
                elif reponse == 'n':
                    break
                elif reponse == 'q':
                    print("Processus de sélection interrompu par l'utilisateur.")
                    return balises_a_modifier
                else:
                    print("Entrée invalide. Veuillez répondre par 'y', 'n' ou 'q'.")
            except KeyboardInterrupt:
                print("\nProcessus de sélection interrompu par l'utilisateur.")
                return balises_a_modifier
            except Exception as e:
                print(f"Erreur inattendue : {e}")
                return balises_a_modifier

    return balises_a_modifier


if __name__ == '__main__':
    print("Veuillez entrer le chemin du fichier HTML à modifier : ")
    fichier_html = input("> ")

    # Vérifier si le fichier existe
    if not os.path.isfile(fichier_html):
        print(f"Erreur : Le fichier '{fichier_html}' n'existe pas.")
    else:
        file = ouvrirFichier(fichier_html, 'r')
        if file:
            soup = BeautifulSoup(file, 'html.parser')
            balises_choisies = balisesAModifier()

            for balise, attribut in balises_choisies.items():
                for balise_html in soup.find_all(balise):
                    old_value = balise_html.get(attribut)
                    if old_value and old_value.startswith('assets'):
                        print(f"Ancien {attribut} : {old_value}")
                        new_value = "{{% static '" + old_value + "' %}}"
                        print(f"Nouveau {attribut} : {new_value}")
                        balise_html[attribut] = new_value

            print("Veuillez entrer le chemin du fichier HTML de destination : ")
            print('Votre fichier sera écrasé !!')
            fichier_destination = input("> ")

            # Écrire les modifications dans le fichier de destination
            if fichier_destination:
                result = ouvrirFichier(fichier_destination, 'w', str(soup.prettify()))
                if result is not None:
                    print(f"Les modifications ont été enregistrées dans '{fichier_destination}'.")
