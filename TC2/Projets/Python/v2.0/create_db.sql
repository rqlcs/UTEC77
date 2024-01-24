CREATE DATABASE IF NOT EXISTS tournoi_foot;

USE tournoi_foot;

CREATE TABLE IF NOT EXISTS equipes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(255) NOT NULL,
    matchs_joues INT NOT NULL,
    matchs_gagnes INT NOT NULL,
    matchs_nuls INT NOT NULL,
    matchs_perdus INT NOT NULL,
    points INT NOT NULL
);

CREATE TABLE IF NOT EXISTS arbitres (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS matchs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    equipe1 VARCHAR(255) NOT NULL,
    equipe2 VARCHAR(255) NOT NULL,
    arbitre VARCHAR(255) NOT NULL,
    stade VARCHAR(255) NOT NULL,
    date_match DATE NOT NULL
);
