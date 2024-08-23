from web3 import Web3
import json
import os
import logging

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

logging.basicConfig(
    filename= os.path.join(BASE_DIR, 'logs.log'),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class CertificationDiplome:
    def __init__(self) -> None:
        self.ganache_url = "http://127.0.0.1:7545"
        self.web3 = Web3(Web3.HTTPProvider(self.ganache_url))
        self.contract_address = "0x6cd2A0E9b6d09Fe400d5D3d3c1F5e969164DCfDf"
        self.account_address = "0x0b753Ec4996700E5bd3739634197FcF100B1A8C1"
        self.web3.eth.default_account = self.account_address

        self.abi_path = os.path.join(BASE_DIR, 'smart-contract/abi.json')

        with open(self.abi_path, 'r') as abi_file:
            self.contract_abi = json.load(abi_file)

        self.contract = self.web3.eth.contract(address=self.contract_address, abi=self.contract_abi)

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    def connect_node_status(self) -> bool:
        try:
            is_connect = self.web3.is_connected()
            return is_connect
        except Exception as e:
            self.logger.error(f"Erreur lors de la connexion au nœud Ethereum : {e}")
            return False

    def emettrer_diplome(self, code_etudiant: str, nom_etudiant: str, date_delivrance: str, hash_diplome: str, resultat: str):
        try:
            transaction = self.contract.functions.emettrer_diplome(code_etudiant, nom_etudiant, date_delivrance, hash_diplome, resultat).transact({'from': self.account_address})
            hash_transaction = f"{transaction.hex()}"
            self.web3.eth.wait_for_transaction_receipt(transaction)
            self.logger.info(f"Transaction réussie avec le hash: {hash_transaction}")
            return hash_transaction
        except Exception as e:
            print(f"Erreur --> {e}")
            self.logger.error(f"Une erreur s'est produite: {e}")
            return None

    def verifier_diplome(self, code_etudiant: str, date_delivrance: str):
        try:
            diplome_info = self.contract.functions.verifier_diplome(code_etudiant, date_delivrance).call()
            
            if diplome_info:
                code_etudiant, nom_etudiant, hash_diplome, resultat, valide = diplome_info
                if valide:
                    self.logger.info(f"Diplome valide pour {code_etudiant} délivré le {date_delivrance}")
                    return {
                        "code_etudiant": code_etudiant,
                        "nom_etudiant": nom_etudiant,
                        "hash_diplome": hash_diplome,
                        "resultat": resultat,
                        "valide": valide
                    }
                else:
                    self.logger.warning(f"Diplome non valide pour {code_etudiant} délivré le {date_delivrance}")
                    return None
            else:
                self.logger.warning(f"Aucune information renvoyée pour le diplôme de {code_etudiant}")
                return None
        except Exception as e:
            self.logger.error(f"Une erreur s'est produite: {e}")
            return None