from certification import CertificationDiplome

diplome = CertificationDiplome()

is_connect = diplome.connect_node_status()
if is_connect:
    code_etudiant = str(input("Entrez le code de l'etudiant : "))
    nom_etudiant = str(input("Entrez le nom de l'etudiant : "))
    resultat = str(input("Entrez le resultat du diplome : "))
    hash_diplome = str(input("Entrez le hash du diplome : "))
    date_delivrance = str(input("Entrez l'année de delivrance : "))

    response = diplome.emettrer_diplome(code_etudiant, nom_etudiant, date_delivrance, hash_diplome, resultat)
    if response is not None:
        print(f"Diplome emit pour {code_etudiant} {nom_etudiant} avec le hash {response}")
    else:
        print(f"Aucune information renvoyée pour le diplome de {code_etudiant}")
else:
    print("Connexion au noeud Ethereum echoue")
