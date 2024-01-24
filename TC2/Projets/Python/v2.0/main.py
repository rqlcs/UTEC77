# -*- coding: utf-8 -*-
# Author Lucas REQUENA & Yassine Boutaouza

import tkinter as tk
from tkinter import simpledialog, messagebox
import mysql.connector

class Application:
    def __init__(self, master):
        self.master = master
        master.title("Tournoi De Foot BTS SIO")

        # Structures de données temporaires
        self.equipes = []
        self.arbitres = []
        self.matchs = []

        # Connexion à la base de données MySQL
        self.db_connection = mysql.connector.connect(
            host="localhost",
            user="reqlu",
            password="root",
            database="tournoi_foot"
        )
        self.cursor = self.db_connection.cursor()

        # Création des tables s'il n'existe pas
        self.creer_tables()

        # Menu
        self.menu = tk.Menu(master)
        master.config(menu=self.menu)

        # Sous-menu "Tournoi"
        self.sous_menu_tournoi = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Tournoi", menu=self.sous_menu_tournoi)
        self.sous_menu_tournoi.add_command(label="Saisir des equipes", command=self.saisir_equipes)
        self.sous_menu_tournoi.add_command(label="Afficher les equipes", command=self.afficher_equipes)
        self.sous_menu_tournoi.add_command(label="Saisir des arbitres", command=self.saisir_arbitres)
        self.sous_menu_tournoi.add_command(label="Planifier des matchs", command=self.planifier_matchs)
        self.sous_menu_tournoi.add_command(label="Saisir des resultats", command=self.saisir_resultats)
        self.sous_menu_tournoi.add_command(label="Afficher les resultats", command=self.afficher_resultats)
        self.sous_menu_tournoi.add_command(label="Afficher le classement", command=self.afficher_classement)
        self.sous_menu_tournoi.add_command(label="Pronostics", command=self.pronostics)
        self.sous_menu_tournoi.add_separator()
        self.sous_menu_tournoi.add_command(label="Quitter", command=self.quitter)

    def creer_tables(self):
        # Création de la table "equipes" si elle n'existe pas
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS equipes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nom VARCHAR(255) UNIQUE,
                matchs_joues INT,
                matchs_gagnes INT,
                matchs_nuls INT,
                matchs_perdus INT,
                points INT
            )
        """)

        # Création de la table "arbitres" si elle n'existe pas
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS arbitres (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nom VARCHAR(255) UNIQUE
            )
        """)

        # Création de la table "matchs" si elle n'existe pas
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS matchs (
                id INT AUTO_INCREMENT PRIMARY KEY,
                equipe1 VARCHAR(255),
                equipe2 VARCHAR(255),
                arbitre VARCHAR(255),
                stade VARCHAR(255),
                date_match DATE
            )
        """)
        self.db_connection.commit()

    def saisir_equipes(self):
        nom_equipe = simpledialog.askstring("Saisir une equipe", "Nom de l'equipe:")
        if nom_equipe:
            equipe = {
                'nom': nom_equipe,
                'matchs_joues': 0,
                'matchs_gagnes': 0,
                'matchs_nuls': 0,
                'matchs_perdus': 0,
                'points': 0
            }
            self.equipes.append(equipe)

            # Insérer l'équipe dans la base de données
            query = "INSERT INTO equipes (nom, matchs_joues, matchs_gagnes, matchs_nuls, matchs_perdus, points) VALUES (%s, %s, %s, %s, %s, %s)"
            values = (nom_equipe, 0, 0, 0, 0, 0)
            self.cursor.execute(query, values)
            self.db_connection.commit()

    def afficher_equipes(self):
        for equipe in self.equipes:
            print(equipe)  # Affichage sur la console

    def saisir_arbitres(self):
        nom_arbitre = simpledialog.askstring("Saisir un arbitre", "Nom de l'arbitre:")
        if nom_arbitre:
            self.arbitres.append(nom_arbitre)  # Ajout à la liste des arbitres

            # Insérer l'arbitre dans la base de données
            query = "INSERT INTO arbitres (nom) VALUES (%s)"
            values = (nom_arbitre,)
            self.cursor.execute(query, values)
            self.db_connection.commit()

    def planifier_matchs(self):
        if len(self.equipes) < 2:
            messagebox.showwarning("Erreur", "Il faut au moins deux equipes pour planifier un match.")
            return

        date_match = simpledialog.askstring("Planifier des matchs", "Date du match (ex: 2023-01-01):")
        if not date_match:
            return

        matchs_planifies = []
        for i in range(0, len(self.equipes), 2):
            equipe1 = self.equipes[i]['nom']
            equipe2 = self.equipes[i + 1]['nom']
            arbitre = self.arbitres[i % len(self.arbitres)]  # Attribution arbitraire
            match = {'equipe1': equipe1, 'equipe2': equipe2, 'arbitre': arbitre, 'stade': 'Stade XYZ', 'date': date_match}
            matchs_planifies.append(match)

            # Insérer le match dans la base de données
            query = "INSERT INTO matchs (equipe1, equipe2, arbitre, stade, date_match) VALUES (%s, %s, %s, %s, %s)"
            values = (equipe1, equipe2, arbitre, 'Stade XYZ', date_match)
            self.cursor.execute(query, values)
            self.db_connection.commit()

        self.matchs.extend(matchs_planifies)
        print("Matchs planifies pour le", date_match)
        for match in matchs_planifies:
            print(match)

    def saisir_resultats(self):
        for match in self.matchs:
            resultat = messagebox.askquestion("Saisir des resultats", "{} vs {}\nL'équipe1 a-t-elle gagné?".format(match['equipe1'], match['equipe2']))
            if resultat == 'yes':
                self.equipes[self.trouver_equipe(match['equipe1'])]['matchs_gagnes'] += 1
                self.equipes[self.trouver_equipe(match['equipe1'])]['points'] += 3
            elif resultat == 'no':
                self.equipes[self.trouver_equipe(match['equipe2'])]['matchs_gagnes'] += 1
                self.equipes[self.trouver_equipe(match['equipe2'])]['points'] += 3
            else:
                self.equipes[self.trouver_equipe(match['equipe1'])]['matchs_nuls'] += 1
                self.equipes[self.trouver_equipe(match['equipe2'])]['matchs_nuls'] += 1
                self.equipes[self.trouver_equipe(match['equipe1'])]['points'] += 1
                self.equipes[self.trouver_equipe(match['equipe2'])]['points'] += 1

            self.equipes[self.trouver_equipe(match['equipe1'])]['matchs_joues'] += 1
            self.equipes[self.trouver_equipe(match['equipe2'])]['matchs_joues'] += 1

            # Mettre à jour les résultats dans la base de données
            query = "UPDATE equipes SET matchs_joues=%s, matchs_gagnes=%s, matchs_nuls=%s, points=%s WHERE nom=%s"
            values = (self.equipes[self.trouver_equipe(match['equipe1'])]['matchs_joues'],
                      self.equipes[self.trouver_equipe(match['equipe1'])]['matchs_gagnes'],
                      self.equipes[self.trouver_equipe(match['equipe1'])]['matchs_nuls'],
                      self.equipes[self.trouver_equipe(match['equipe1'])]['points'],
                      match['equipe1'])
            self.cursor.execute(query, values)

            values = (self.equipes[self.trouver_equipe(match['equipe2'])]['matchs_joues'],
                      self.equipes[self.trouver_equipe(match['equipe2'])]['matchs_gagnes'],
                      self.equipes[self.trouver_equipe(match['equipe2'])]['matchs_nuls'],
                      self.equipes[self.trouver_equipe(match['equipe2'])]['points'],
                      match['equipe2'])
            self.cursor.execute(query, values)

            self.db_connection.commit()

    def afficher_resultats(self):
        for match in self.matchs:
            print("{} vs {}: Résultat non saisi".format(match['equipe1'], match['equipe2']))

    def afficher_classement(self):
        classement = sorted(self.equipes, key=lambda x: (x['points'], x['matchs_gagnes']), reverse=True)
        print("Classement actuel :")
        for i, equipe in enumerate(classement, 1):
            print("{}. {} - Points: {}, Matchs gagnes: {}".format(i, equipe['nom'], equipe['points'], equipe['matchs_gagnes']))

    def pronostics(self):
        pronostics_equipes = simpledialog.askstring("Pronostics", "Pronostiquez les trois premieres équipes (separees par des virgules):")
        if pronostics_equipes:
            pronostics_list = [equipe.strip() for equipe in pronostics_equipes.split(',')]
            classement_actuel = [equipe['nom'] for equipe in self.equipes]

            if pronostics_list == classement_actuel[:3]:
                messagebox.showinfo("Pronostics", "Felicitations ! Vos pronostics sont corrects.")
            else:
                messagebox.showinfo("Pronostics", "Dommage, vos pronostics ne sont pas corrects.")

    def quitter(self):
        # Fermer la connexion à la base de données avant de détruire la fenêtre
        self.cursor.close()
        self.db_connection.close()
        self.master.destroy()

    def trouver_equipe(self, nom_equipe):
        for i, equipe in enumerate(self.equipes):
            if equipe['nom'] == nom_equipe:
                return i

if __name__ == "__main__":
    root = tk.Tk()
    app = Application(root)
    root.mainloop()
