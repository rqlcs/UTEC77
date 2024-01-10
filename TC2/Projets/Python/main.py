# -*- coding: utf-8 -*-
#Author Lucas REQUENA & Yassine Boutaouza

import Tkinter as tk
from Tkinter import *
import tkSimpleDialog as simpledialog
import tkMessageBox as messagebox

class Application:
    def __init__(self, master):
        self.master = master  #cest le Tk.tk()
        master.title("Tournoi De Foot BTS SIO") #titre application

        # Structures de donnees temporaires
        self.equipes = []  #liste equipes
        self.arbitres = [] #liste nom arbitres
        self.matchs = []   #liste des matchs

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

    def afficher_equipes(self):
        for equipe in self.equipes:
            print(equipe) #affichage sur shell

    def saisir_arbitres(self):
        nom_arbitre = simpledialog.askstring("Saisir un arbitre", "Nom de l'arbitre:")
        if nom_arbitre:
            self.arbitres.append(nom_arbitre) #ajout a la liste des arbitres

    def planifier_matchs(self):

        if len(self.equipes) < 2:
            messagebox.showwarning("Erreur", "Il faut au moins deux equipes pour planifier un match.")
            return  #nul return

        date_match = simpledialog.askstring("Planifier des matchs", "Date du match (ex: 2023-01-01):")
        if not date_match:
            return #nul return

        matchs_planifies = []
        for i in range(0, len(self.equipes), 2):
            equipe1 = self.equipes[i]['nom']
            equipe2 = self.equipes[i + 1]['nom']
            arbitre = self.arbitres[i % len(self.arbitres)]  # Attribution arbitraire
            match = {'equipe1': equipe1, 'equipe2': equipe2, 'arbitre': arbitre, 'stade': 'Stade XYZ', 'date': date_match}
            matchs_planifies.append(match)

        self.matchs.extend(matchs_planifies)
        print("Matchs planifies pour le", date_match)
        for match in matchs_planifies:
            print(match)

    def saisir_resultats(self):
        # Simplification : On demande simplement si l'equipe1 a gagne ou non
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

    def afficher_resultats(self):
        for match in self.matchs:
            print("{} vs {}: Résultat non saisi".format(match['equipe1'], match['equipe2']))

    def afficher_classement(self):
        classement = sorted(self.equipes, key=lambda x: (x['points'], x['matchs_gagnes']), reverse=True)
        print("Classement actuel :")
        for i, equipe in enumerate(classement, 1):
            print("{}. {} - Points: {}, Matchs gagnes: {}".format(i, equipe['nom'], equipe['points'], equipe['matchs_gagnes']))

    def pronostics(self):  #pronostics sur les trois premiere equipes
        pronostics_equipes = simpledialog.askstring("Pronostics", "Pronostiquez les trois premieres équipes (separees par des virgules):")
        if pronostics_equipes:
            pronostics_list = [equipe.strip() for equipe in pronostics_equipes.split(',')]
            classement_actuel = [equipe['nom'] for equipe in self.equipes]

            if pronostics_list == classement_actuel[:3]:
                messagebox.showinfo("Pronostics", "Felicitations ! Vos pronostics sont corrects.")
            else:
                messagebox.showinfo("Pronostics", "Dommage, vos pronostics ne sont pas corrects.")

    def quitter(self):
        self.master.destroy() #on detruit laffichage graphique

    def trouver_equipe(self, nom_equipe):
        for i, equipe in enumerate(self.equipes):
            if equipe['nom'] == nom_equipe:
                return i

if __name__ == "__main__": #debut du programme
    root = tk.Tk()
    app = Application(root)
