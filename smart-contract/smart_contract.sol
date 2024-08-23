// SPDX-License-Identifier: GPL-3.0
pragma solidity ^0.8.0;

contract CertificationDiplome {
    struct Diplome {
        string code_etudiant;
        string nom_etudiant;
        string date_delivrance;
        string hash_diplome;
        string resultat;
        bool livrer;
    }

    address public university;
    mapping(bytes32 => Diplome) public diplomes;

    constructor() {
        university = msg.sender; // L'université déploie le contrat
    }

    modifier university_required() {
        require(msg.sender == university, "Seul l'universite est autorise a l'utiliser");
        _;
    }

    function emettrer_diplome(string memory _code_etudiant, string memory _nom_etudiant, string memory _date_delivrance, string memory _hash_diplome, string memory _resultat) public university_required {
        bytes32 hash_etudiant = keccak256(abi.encodePacked(_code_etudiant, _date_delivrance));
        require(!diplomes[hash_etudiant].livrer, "Le diplome a deja ete emis");

        diplomes[hash_etudiant] = Diplome({
            code_etudiant: _code_etudiant,
            nom_etudiant: _nom_etudiant,
            date_delivrance: _date_delivrance,
            hash_diplome: _hash_diplome,
            resultat: _resultat,
            livrer: true
        });
    }

    function verifier_diplome(
        string memory _code_etudiant, string memory _date_delivrance
    ) public view returns (string memory code_etudiant, string memory nom_etudiant, string memory hash_diplome, string memory resultat, bool valide
    ) {
        bytes32 hash_etudiant = keccak256(abi.encodePacked(_code_etudiant, _date_delivrance));
        Diplome memory diplome = diplomes[hash_etudiant];
        return (diplome.code_etudiant, diplome.nom_etudiant, diplome.hash_diplome, diplome.resultat, diplome.livrer);
    }
}
