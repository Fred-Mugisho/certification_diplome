from certification import CertificationDiplome

diplome = CertificationDiplome()

is_connect = diplome.connect_node_status()
if is_connect:
    code_etudiant = str(input("Entrez le code de l'etudiant : "))
    date_delivrance = str(input("Entrez l'année de delivrance : "))

    response = diplome.verifier_diplome(code_etudiant, date_delivrance)
    if response is not None:
        print(f"Diplome valide pour {code_etudiant} {response['nom_etudiant']} délivré en {date_delivrance}")
    else:
        print(f"Aucune information renvoyée pour le diplome de {code_etudiant}")
else:
    print("Connexion au noeud Ethereum echoue")