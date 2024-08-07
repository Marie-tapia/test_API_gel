import os
import pandas as pd
from django.conf import settings

def load_dictionaries():
    # Obtenir le chemin absolu du répertoire dictionnaires
    base_dir = os.path.join(settings.BASE_DIR, 'dictionnaires')

    # Charger les fichiers CSV en utilisant des chemins relatifs
    dico_rac_harc = pd.read_csv(os.path.join(base_dir, 'dico_racines_harcelement.csv'), sep=',')
    dico_racine_harc = dict(zip(dico_rac_harc['mots'], dico_rac_harc['valeur']))

    dico_harc_assos_mots = pd.read_csv(os.path.join(base_dir, 'dico_harcelement.csv'), sep=',')
    dico_harcelement = dict(zip(dico_harc_assos_mots['mots'], dico_harc_assos_mots['valeur']))
    dico_harcelement = {tuple(association.split()): valeur for association, valeur in dico_harcelement.items() if len(association.split())}

    manque_droit = pd.read_csv(os.path.join(base_dir, 'dico_manque_droit.csv'), sep=',')
    dico_manque_droit = dict(zip(manque_droit['mots'], manque_droit['valeur']))
    dico_manque_droit = {tuple(key.split()): valeur for key, valeur in dico_manque_droit.items() if len(key.split())}

    manque_encadrement = pd.read_csv(os.path.join(base_dir, 'dico_encadrement.csv'), sep=',')
    dico_manque_encadrement = dict(zip(manque_encadrement['mots'], manque_encadrement['valeur']))
    dico_manque_encadrement = {tuple(key.split()): valeur for key, valeur in dico_manque_encadrement.items() if len(key.split())}


    manque_pedagogie = pd.read_csv(os.path.join(base_dir, 'dico_pedagogie.csv'), sep=',')
    dico_manque_pedagogie = dict(zip(manque_pedagogie['mots'], manque_pedagogie['valeur']))
    dico_manque_pedagogie = {tuple(key.split()): valeur for key, valeur in dico_manque_pedagogie.items() if len(key.split())}

    return {
        "dico_racine_harc": dico_racine_harc,
        "dico_harcelement": dico_harcelement,
        "dico_manque_droit": dico_manque_droit,
        "dico_manque_encadrement": dico_manque_encadrement,
        "dico_manque_pedagogie": dico_manque_pedagogie,
    }

# Charger les dictionnaires
dictionaries = load_dictionaries()
