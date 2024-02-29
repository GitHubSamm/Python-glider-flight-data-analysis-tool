# -*- coding: utf-8 -*-
"""
Created on Fri Apr  2 15:44:24 2021

@author: marin
"""
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg #Sert a creer une canvas specifique pour les graphiques
from tkinter import *
import Extraction_fonctions as ex
from tkinter import ttk as ttk
from tkinter import messagebox

import numpy as np


class Fenetre(Frame):
    global couleurFond1, couleurFond2, couleurText, fondSombre, couleurTextErreur
    couleurFond1 = 'white'
    couleurFond2 = '#222b35'
    couleurText = '#0084A4'
    couleurText2 = '#006FAD'
    couleurGet = '#CECCCB'
    fondSombre = '#161C22'
    couleurTextErreur = '#C20000'

    
    def __init__(self, fenetre):
        
        Frame.__init__(self, fenetre, bg = couleurFond1)
        self.pack(expand = YES, fill=BOTH)
        self.ecran_acceuil()
        fenetre.title("Application d'analyse de données | Envairgure")
        fenetre.geometry("600x600")
        fenetre.iconphoto(False, PhotoImage(file='logo.png'))
        
    def ecran_acceuil(self): 
        self.frame = Frame(self, bg = couleurFond1)
        self.Label_titre=Label(self.frame, text ="Application d'analyse de vol ",font=("Calibri",30,'bold','underline'),bg=couleurFond1 , fg=couleurText, padx=0, pady=20)
        self.Label_titre.pack()
        self.Label_sous_titre=Label(self.frame, text='Grand Projet Planeur', font="Cambria 22 bold",bg=couleurFond1 , fg=couleurText, padx=0, pady=20)
        self.Label_sous_titre.pack()
        # self.image=PhotoImage(file="ideeapp.png")
        # self.canvas_img=Canvas(frame, width=300, height=300)
        # self.canvas_img.create_image(150, 150, image=self.image).pack(expand=YES)
        
        self.consigne=Label(self.frame, text='Entrer le nom du fichier ci-dessous:', font="Arial 18",bg=couleurFond1 , fg=couleurText, pady=10)
        self.consigne.pack()
        self.frame.pack(expand=YES)
        
        self.nomdufichier=StringVar()
        self.nomdufichier.set("Nom_du_fichier.igc")
        self.ecran_nomdufichierEntry = Entry(self.frame, textvariable = self.nomdufichier, width=60, fg = 'black', bg = 'white')
        self.ecran_nomdufichierEntry.pack(expand=YES, anchor='n')
        
        self.analyser = Button(self.frame, text = "Analyser", command = self.ecran2, fg = couleurText, bg= '#A0CCE4')
        self.analyser.pack(pady=10)
        self.bouton_apropos = Button(self, text="A propos",command = self.Apropos, fg = couleurText, bg = couleurFond1)
        self.bouton_apropos.pack(side = BOTTOM, pady = 15)
        
        
    
    #Fonction qui efface l'écran d'acceuil            
    def clearAcceuil(self):
        self.Label_sous_titre.pack_forget()
        self.Label_titre.pack_forget()
        self.bouton_apropos.pack_forget()
        self.analyser.pack_forget()
        self.ecran_nomdufichierEntry.pack_forget()
        self.frame.pack_forget()
        self.consigne.pack_forget()
    def clearEcran2(self):
        for i in self.widget:
            i.pack_forget()
        
        
    #Fenetre graphique de la section "A propos"    
    def Apropos(self):
        
        self.clearAcceuil()
        
        frameApropos = Frame(self, bg = couleurFond1)
        Label(frameApropos, text= "Version logiciel : 1.0 \n \n Année 2020-2021 \n \n Application développée dans le cadre du Grand Projet Planeur \n \n Par : Yaelle Anta, Clement Belloir, Baptiste Canonge, \n Marine Colanson, Sam Collin, Thomas Cliquennois, \n Chloé Dussarrat, Mathis Larsen, Aymeri Moudens", bg = couleurFond1, fg = couleurText).pack()
        
        self.bouton_retour = Button(frameApropos, text="Retour",command = self.retourAcceuil, fg = couleurText, bg = couleurFond1)
        self.bouton_retour.pack(side = RIGHT, pady = 30)
        
        frameApropos.pack(padx = 15, pady = 15)
        
        self.widget = [frameApropos]
    
    def positionVz(self):
        
        #recuperation des données
        fichier=self.ecran_nomdufichierEntry.get()
        time=ex.recupdonnee(fichier)[0]
        latitude=ex.recupdonnee(fichier)[1]
        longitude=ex.recupdonnee(fichier)[2]
        altitude=ex.recupdonnee(fichier)[3]
        
        timeSec=ex.conversion(time,latitude,longitude,altitude)[3]
        Vz=ex.Vario(altitude,timeSec)
        longitude=np.array(longitude)
        latitude=np.array(latitude)
        altitude=np.array(altitude)
        time=np.array(time)  
        
        #Affiche le graphique dans la fenetre --> Changer le backend dans preference en "en ligne"--> Pourquoi le backend Tkinter fait planter la console ?  
        self.canvas = FigureCanvasTkAgg(ex.trajectoire(longitude,latitude,Vz,"Vitesse verticale"), master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget (). pack ( side = "bottom" , fill = "both" , expand = True )
        
        self.label = Label(self, text ="Position - Vitesse verticale",font=("Calibri",20,'bold','underline'),bg=couleurFond1 , fg=couleurText)
        self.label.pack()
        
        self.widget = [self.label,self.canvas.get_tk_widget ()]
        
        
    def positionAlti(self):
        
        #recuperation des données
        fichier=self.ecran_nomdufichierEntry.get()
        time=ex.recupdonnee(fichier)[0]
        latitude=ex.recupdonnee(fichier)[1]
        longitude=ex.recupdonnee(fichier)[2]
        altitude=ex.recupdonnee(fichier)[3]
        
        timeSec=ex.conversion(time,latitude,longitude,altitude)[3]
        Vz=ex.Vario(altitude,timeSec)
        longitude=np.array(longitude)
        latitude=np.array(latitude)
        altitude=np.array(altitude)
        time=np.array(time)  
        
        
        self.canvas = FigureCanvasTkAgg(ex.trajectoire(longitude,latitude,altitude,"Altitude"), master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget (). pack ( side = "bottom" , fill = "both" , expand = True )
        
        self.label = Label(self, text ="Position - Altitude",font=("Calibri",20,'bold','underline'),bg=couleurFond1 , fg=couleurText)
        self.label.pack()
        
        self.widget = [self.label,self.canvas.get_tk_widget ()]
        
    def positionVo(self):
        
        #recuperation des données
        fichier=self.ecran_nomdufichierEntry.get()
        time=ex.recupdonnee(fichier)[0]
        latitude=ex.recupdonnee(fichier)[1]
        longitude=ex.recupdonnee(fichier)[2]
        altitude=ex.recupdonnee(fichier)[3]
        
        timeSec=ex.conversion(time,latitude,longitude,altitude)[3]
        longitude=np.array(longitude)
        latitude=np.array(latitude)
        altitude=np.array(altitude)
        time=np.array(time)  
        X=ex.conversion(time,latitude,longitude,altitude)[0]
        Y=ex.conversion(time,latitude,longitude,altitude)[1]
        Z=ex.conversion(time,latitude,longitude,altitude)[2]
        Vo=ex.Vitesses(X,Y,Z,timeSec,latitude,longitude)[3]
        
        self.label = Label(self, text ="Position - Vitesse absolue",font=("Calibri",20,'bold','underline'),bg=couleurFond1 , fg=couleurText)
        self.label.pack()
        
        self.canvas = FigureCanvasTkAgg(ex.trajectoire(longitude,latitude,Vo,"Vitesse absolue"), master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget (). pack ( side = "bottom" , fill = "both" , expand = True )
        
        self.widget = [self.label,self.canvas.get_tk_widget ()]
    
    def afficheCarte(self):
        
        #recuperation des données
        fichier=self.ecran_nomdufichierEntry.get()
        time=ex.recupdonnee(fichier)[0]
        latitude=ex.recupdonnee(fichier)[1]
        longitude=ex.recupdonnee(fichier)[2]
        altitude=ex.recupdonnee(fichier)[3]
        
        longitude=np.array(longitude)
        latitude=np.array(latitude)
        altitude=np.array(altitude)
        time=np.array(time)  
        X=ex.conversion(time,latitude,longitude,altitude)[0]
        Y=ex.conversion(time,latitude,longitude,altitude)[1]
        ex.Affichage_carte(latitude,longitude)
        
        
    #Fonction qui efface la fenetre dans laquelle la fonction est appelé et affiche l'écran d'acceuil
    def retourAcceuil(self):
        for i in self.widget:
            i.pack_forget()
        self.ecran_acceuil()
        
    def retourAlti(self):
        for i in self.widget:
            i.pack_forget()
        self.positionAlti()
        
    def clearAlti(self):
        for i in self.widget:
            i.pack_forget()
    
    def retourEcran2(self):
        for i in self.widget:
            i.pack_forget()
        self.ecran2()
    
    def retourEcran2bis(self):
        for i in self.widget1:
            i.pack_forget()
        for j in self.widget:
            j.pack_forget()
        self.ecran2()
        
    def detailAlti(self):
        
        
        #recuperation des données
        fichier=self.ecran_nomdufichierEntry.get()
        time=ex.recupdonnee(fichier)[0]
        latitude=ex.recupdonnee(fichier)[1]
        longitude=ex.recupdonnee(fichier)[2]
        altitude=ex.recupdonnee(fichier)[3]
        
        timeSec=ex.conversion(time,latitude,longitude,altitude)[3]
        Vz=ex.Vario(altitude,timeSec)
        longitude=np.array(longitude)
        latitude=np.array(latitude)
        altitude=np.array(altitude)
        time=np.array(time)  
        
        self.label = Label(self, text ="Details sur les variations d'altitudes ",font=("Calibri",20,'bold','underline'),bg=couleurFond1 , fg=couleurText)
        self.label.pack()
        
        self.detail = Label(self, text=ex.pourcentageAltitude(Vz),font=("Calibri",12),bg=couleurFond1 , fg=couleurText )
        self.detail.pack()
        self.canvas = FigureCanvasTkAgg(ex.Altitude(altitude,timeSec), master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget (). pack (side = "bottom", fill = "both" , expand = True )
        
        
        self.widget = [self.detail,self.label,self.canvas.get_tk_widget ()]

    def ecran2(self):
    
        self.clearAcceuil()
        nomdufichier = self.ecran_nomdufichierEntry.get()
        
        self.frame1 = Frame(self, bg='white')
        self.label1 = Label(self.frame1, text=nomdufichier[0:-4], font = ("Calibri",16,'bold') ) 
        self.label1.pack()
        self.frame1.pack(expand=YES)
        
        self.frame2 = Frame(self, padx = 0, pady = 40,bg=couleurFond1)
        self.bouton_affcarte = Button(self.frame2, text= "Afficher sur la carte", command = self.afficheCarte, width = 30, height = 3,  fg= couleurText, bg = couleurFond1)
        self.bouton_affcarte.pack(expand = YES, side=LEFT)
        self.bouton_trajectoire = Button(self.frame2, text = " Trajectoires", command = self.trajectoire, width = 30,height = 3, fg= couleurText , bg = couleurFond1)
        self.bouton_trajectoire.pack(expand= YES, side = RIGHT)
        self.frame2.pack(expand=YES)
        
        self.frame3 = Frame(self, padx = 0, pady = 40, bg= couleurFond1)
        self.bouton_vent = Button(self.frame3, text ="Analyse Thermiques", command = self.ventCap , width = 30 ,height = 3, fg = couleurText, bg = couleurFond1 )
        self.bouton_vent.pack(expand=YES, side = LEFT)
        self.bouton_mcready = Button(self.frame3, text = "Mac Cready", command = self.macCready , width = 30 ,height = 3, fg = couleurText , bg = couleurFond1)
        self.bouton_mcready.pack(expand = YES, side = RIGHT)
        self.frame3.pack(expand=YES)
        
        self.frame4 = Frame(self, padx = 0, pady = 40, bg= couleurFond1)
        self.bouton_tdp = Button(self.frame4, text ="Tour de Piste", command = self.tourDePiste , width = 30 ,height = 3, fg = couleurText, bg = couleurFond1 )
        self.bouton_tdp.pack(expand=YES, side = LEFT)
        self.bouton_finesse = Button(self.frame4, text = "Finesse en vol", command = self.finesse , width = 30 ,height = 3, fg = couleurText , bg = couleurFond1)
        self.bouton_finesse.pack(expand = YES, side = RIGHT)
        self.frame4.pack(expand=YES)
        
        self.frame5 = Frame(self, padx = 0, pady = 10, bg= couleurFond1)
        self.bouton_accueil = Button(self.frame5, text = "Retour", command = self.retourAcceuil, fg = couleurText , bg = couleurFond1 )
        self.bouton_accueil.pack(expand = YES, side = BOTTOM)
        self.frame5.pack()
        
        self.widget = [self.bouton_accueil,self.frame5,self.bouton_finesse,self.label1,self.frame1,self.bouton_affcarte,self.frame2,self.frame3,self.bouton_vent,self.bouton_mcready,self.frame4,self.bouton_tdp]
        
    def macCready(self):
        
        self.clearEcran2()
        
        self.label = Label(self, text ="Mac Cready",font=("Calibri",20,'bold','underline'),bg=couleurFond1 , fg=couleurText, padx=0, pady=20)
        self.label.pack(side = TOP)
        
        fichier=self.ecran_nomdufichierEntry.get()
        time=ex.recupdonnee(fichier)[0]
        latitude=ex.recupdonnee(fichier)[1]
        longitude=ex.recupdonnee(fichier)[2]
        altitude=ex.recupdonnee(fichier)[3]
        timeSec=ex.conversion(time,latitude,longitude,altitude)[3]
        X=ex.conversion(time,latitude,longitude,altitude)[0]
        Y=ex.conversion(time,latitude,longitude,altitude)[1]
        Z=ex.conversion(time,latitude,longitude,altitude)[2]
        Va=ex.Vitesses(X,Y,Z,timeSec,latitude,longitude)[4]   
        Vo=ex.Vitesses(X,Y,Z,timeSec,latitude,longitude)[3]
        vario=ex.Vario(altitude,timeSec)
        longitude=np.array(longitude)
        latitude=np.array(latitude)
        
        self.canvas = FigureCanvasTkAgg(ex.MacCready(timeSec,Vo,vario,Va,longitude,latitude), master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget (). pack ( fill = "both" , expand = True )
        
        self.widget=[self.canvas.get_tk_widget ()]
        
        self.frame2 = Frame(self, bg=couleurFond1)
        self.bouton_accueil = Button(self.frame2, text = "Retour", command = self.retourEcran2bis, fg = couleurText , bg = couleurFond1 )
        self.bouton_accueil.pack(pady = 10)
        self.frame2.pack(side = BOTTOM)
        
        
        
        self.widget1 = [self.frame1,self.frame2,self.label,self.frame3]
    def ventCap(self):
        
        #recuperation des données
        fichier=self.ecran_nomdufichierEntry.get()
        time=ex.recupdonnee(fichier)[0]
        latitude=ex.recupdonnee(fichier)[1]
        longitude=ex.recupdonnee(fichier)[2]
        altitude=ex.recupdonnee(fichier)[3]
        
        timeSec=ex.conversion(time,latitude,longitude,altitude)[3]
        vario=ex.Vario(altitude,timeSec)
        longitude=np.array(longitude)
        latitude=np.array(latitude)
        altitude=np.array(altitude)
        time=np.array(time)  
        Cap=ex.cap(latitude,longitude,timeSec)[0]
        Vsol=ex.cap(latitude,longitude,timeSec)[1]
        DebTherm=ex.rotation(Cap)[0]
        FinTherm=ex.rotation(Cap)[1]
        NumTherm=ex.rotation(Cap)[2]
        Tour=ex.rotation(Cap)[3]
        NbTour=str(len(NumTherm))
        NbTourPython=str(len(NumTherm)-1)
        self.clearEcran2()
        
        self.label = Label(self, text ="Visualisation thermiques",font=("Calibri",20,'bold','underline'),bg=couleurFond1 , fg=couleurText, padx=0, pady=20)
        self.label.pack(side = TOP)
        
        self.frame1 = Frame(self, padx = 0, pady = 10, bg=couleurFond1)
        self.labelThermique = Label(self.frame1,text = "Il y a {} thermiques dans ce vol (numérotée de 0 à {})".format(NbTour,NbTourPython),font=("Calibri",12),bg=couleurFond1 , fg="black" )
        self.labelThermique.pack()
        self.frame1.pack()
        
        self.frame2 = Frame(self, padx = 0, pady = 10, bg=couleurFond1)
        self.labelNbTherm = Label(self.frame2,text = "Saisir le numéro du thermique à visualiser: ",font=("Calibri",12),bg=couleurFond1 , fg="black" )
        self.NbTherm=IntVar()
        self.NbThermEntry = Entry(self.frame2, textvariable = str(self.NbTherm), width=10, fg = "black", bg = 'white')
        self.labelNbTherm.pack()
        self.NbThermEntry.pack()
        self.frame2.pack()
        
        self.frame3 = Frame(self,padx = 0, pady = 10, bg=couleurFond1)
        self.boutonAff = Button(self.frame3, text = "Afficher", command = self.AffThermique, fg = couleurText , bg = couleurFond1)
        self.boutonAff.pack(side=BOTTOM)
        self.frame3.pack()
        
        self.frame4 = Frame(self, bg=couleurFond1)
        self.boutonRetour = Button(self.frame4, text = "Retour", command = self.retourEcran2bis, fg = couleurText , bg = couleurFond1)
        self.boutonRetour.pack(pady = 10)
        self.frame4.pack(side =BOTTOM)
        
        self.widget1 =[self.frame1,self.frame2,self.frame3,self.boutonRetour,self.label,self.frame4]
    
    def tourDePiste(self):
        #utilisateur saisi coord centre piste,longueur piste Toulouse Bourg Saint Bernard
        self.clearEcran2()
        
        self.label = Label(self, text ="Tour de Piste",font=("Calibri",20,'bold','underline'),bg=couleurFond1 , fg=couleurText, padx=0, pady=20)
        self.label.pack(side = TOP)
        
        self.frame1 = Frame(self, padx = 0, pady = 5, bg=couleurFond1)
        self.orientationText = Label(self.frame1, text ="Saisir l'orientation de la piste d'atterrissage ci-contre :",font=("Calibri",12),bg=couleurFond1 , fg="black")
        self.orientationText.pack(expand = YES, side = LEFT)
        self.orientation=DoubleVar()
        self.orientation.set(120)
        
        self.orientationEntry = Entry(self.frame1, textvariable = self.orientation, width=10, fg = "black", bg = 'white')
        self.orientationEntry.pack(expand=YES, padx = 5)
        self.frame1.pack()
        
        self.frame5 = Frame(self, padx = 0, pady = 10, bg=couleurFond1)
        self.longueurText = Label(self.frame5, text ="Saisir la longueur de la piste d'atterrissage ci-contre :",font=("Calibri",12),bg=couleurFond1 , fg="black")
        self.longueurText.pack(expand = YES, side = LEFT)
        self.longueur=DoubleVar()
        self.longueur.set(1000)
        
        self.longueurEntry = Entry(self.frame5, textvariable = self.longueur, width=10, fg = "black", bg = 'white')
        self.longueurEntry.pack(expand=YES, padx = 5)
        self.frame5.pack()
        
        self.frame4 = Frame(self, padx = 0, pady = 10, bg=couleurFond1)
        self.coordText = Label(self.frame4, text ="Saisir les coordonnées de la piste :",font=("Calibri",12),bg=couleurFond1 , fg="black")
        self.coordText.pack(expand = YES, side = LEFT)
        self.coordlat=DoubleVar()
        self.coordlong=DoubleVar()
        self.coordlat.set(1.7272)
        self.coordlong.set(43.6105)
        
        self.coordLatEntry = Entry(self.frame4, textvariable = self.coordlat, width=10, fg = "black", bg = 'white')
        self.coordLatEntry.pack(expand=YES, padx = 5)
        self.coordLongEntry = Entry(self.frame4, textvariable = self.coordlong, width=10, fg = "black", bg = 'white')
        self.coordLongEntry.pack(expand=YES, padx = 5, pady = 1)
        self.frame4.pack()
        
        self.frame2 = Frame(self, padx = 0, pady = 10, bg=couleurFond1)
        
        self.Variable = StringVar()
        
        
        radioBoutonValeur = ['TDPD', 'TDPG']
        etiquette = ['Tour de piste Main Droite', 'Tour de piste Main Gauche']
        
        self.boutonTDP = Radiobutton(self.frame2, text = etiquette[0], variable = self.Variable, value = radioBoutonValeur[0],
                                         selectcolor = couleurFond1, background = couleurFond1, fg = couleurText, indicatoron = 0, width = 30)
        self.boutonTDP.pack(side = RIGHT)
        self.boutonTDP = Radiobutton(self.frame2, text = etiquette[1], variable = self.Variable, value = radioBoutonValeur[1],
                                         selectcolor = couleurFond1, background = couleurFond1, fg = couleurText, indicatoron = 0, width = 30)
        self.boutonTDP.pack(side = RIGHT)
        self.frame2.pack()
        
        self.frame3 = Frame(self, padx = 0, pady = 7, bg=couleurFond1)
        self.boutonAfficher = Button(self.frame3, text = "Afficher", command = self.AffichageTDP, fg = couleurText, bg = couleurFond1 )
        self.boutonAfficher.pack()
        self.frame3.pack()
        
        self.frame6 = Frame(self, bg = couleurFond1)
        self.bouton_accueil = Button(self.frame6, text = "Retour", command = self.retourEcran2bis, fg = couleurText , bg = couleurFond1 )
        self.bouton_accueil.pack(pady = 10)
        self.frame6.pack(side = BOTTOM)
        
        self.widget1 = [self.frame4,self.frame1,self.bouton_accueil,self.boutonTDP,self.frame2,self.frame3,self.frame5,self.label,self.frame6]
   
    def AffichageTDP(self):
        self.clearAlti()
        #recuperation des données
        fichier=self.ecran_nomdufichierEntry.get()
        latitude=ex.recupdonnee(fichier)[1]
        longitude=ex.recupdonnee(fichier)[2]
        longP=float(self.coordlong.get())
        latP=float(self.coordlat.get())
        Lo=float(self.longueur.get())
        d=float(self.orientation.get())
        
        TDP = self.Variable.get()
            
        if TDP != 'TDPG' and TDP != 'TDPD':
            messagebox.showwarning("Erreur de saisie","Veuillez choisir le sens du Tour de piste!")
            
        elif TDP == 'TDPG':
            self.canvas = FigureCanvasTkAgg(ex.TourDePisteG (d,Lo,longP,latP,longitude,latitude), master=self)
            self.canvas.draw()
            self.canvas.get_tk_widget (). pack ( fill = "both" , expand = True )
            self.widget=[self.canvas.get_tk_widget ()]
        elif TDP == 'TDPD':
           self.canvas = FigureCanvasTkAgg(ex.TourDePisteD (d,Lo,longP,latP,longitude,latitude), master=self)
           self.canvas.draw()
           self.canvas.get_tk_widget (). pack ( fill = "both" , expand = True ) 
           
           self.widget=[self.canvas.get_tk_widget ()]
       
    def finesse(self):
        
        self.clearEcran2()
        
        #recuperation des données
        fichier=self.ecran_nomdufichierEntry.get()
        time=ex.recupdonnee(fichier)[0]
        latitude=ex.recupdonnee(fichier)[1]
        longitude=ex.recupdonnee(fichier)[2]
        altitude=ex.recupdonnee(fichier)[3]
        
        X=ex.conversion(time,latitude,longitude,altitude)[0]
        Y=ex.conversion(time,latitude,longitude,altitude)[1]
        longitude=np.array(longitude)
        latitude=np.array(latitude)
        altitude=np.array(altitude)
        X=np.array(X)
        Y=np.array(Y)
        
        self.label = Label(self, text ="Finesse en vol",font=("Calibri",20,'bold','underline'),bg=couleurFond1 , fg=couleurText, padx=0, pady=20)
        self.label.pack(side = TOP)
        
        #Affiche le graphique dans la fenetre --> Changer le backend dans preference en "en ligne"--> Pourquoi le backend Tkinter fait planter la console ?  
        self.canvas = FigureCanvasTkAgg(ex.Finesse(X,Y,altitude,longitude,latitude,"Finesse"), master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget (). pack ( fill = "both" , expand = True )
        
        
        self.frameRetour=Frame(self, padx = 0, pady = 10, bg= couleurFond1)
        self.bouton_retour = Button(self.frameRetour, text="Retour", command = self.retourEcran2, fg = couleurText, bg = couleurFond1)
        self.bouton_retour.pack(side = BOTTOM)
        self.frameRetour.pack()
        
        self.widget = [self.bouton_retour,self.label,self.canvas.get_tk_widget (),self.frameRetour]

    def AffTraj(self,event):
        
        select = self.Cb.get()
        self.clearAlti()
        if select == "Altitude en fonction de la trajectoire":
            self.positionAlti()
        elif select == "Vitesse verticale en fonction de la trajectoire":
            self.positionVz()
        elif select =="Vitesse absolue en fonction de la trajectoire":
            self.positionVo()
        elif select == "Détails variations d'altitude":
            self.detailAlti()
             
            
    def trajectoire(self):
        
        self.clearEcran2()
        
        self.label = Label(self, text ="Trajectoires",font=("Calibri",20,'bold','underline'),bg=couleurFond1 , fg=couleurText, padx=0, pady=20)
        self.label.pack(side = TOP)
        
        self.frame1 = Frame(self, pady = 20, padx = 40, bg = couleurFond1)
        self.Cb = ttk.Combobox(self.frame1,width = 50, values = ["Altitude en fonction de la trajectoire",
                                                      "Vitesse verticale en fonction de la trajectoire",
                                                      "Vitesse absolue en fonction de la trajectoire",
                                                      "Détails variations d'altitude"])
        
        self.Cb.current(0)
        self.Cb.bind("<<ComboboxSelected>>", self.AffTraj)
        
        self.frame1.pack()
        self.Cb.pack(side = LEFT)
        
        self.frame2 = Frame(self, bg = couleurFond1)
        self.retour = Button(self.frame2, text = "Retour", command = self.retourEcran2bis, fg = couleurText, bg= couleurFond1)
        self.retour.pack(pady = 10)
        self.frame2.pack(side = BOTTOM)
        
        self.widget1 = [self.frame1,self.Cb,self.retour,self.label,self.frame2]
    
    def AffThermique(self):
        self.clearAlti()
        #recuperation des données
        fichier=self.ecran_nomdufichierEntry.get()
        time=ex.recupdonnee(fichier)[0]
        latitude=ex.recupdonnee(fichier)[1]
        longitude=ex.recupdonnee(fichier)[2]
        altitude=ex.recupdonnee(fichier)[3]
        
        timeSec=ex.conversion(time,latitude,longitude,altitude)[3]
        vario=ex.Vario(altitude,timeSec)
        longitude=np.array(longitude)
        latitude=np.array(latitude)
        altitude=np.array(altitude)
        time=np.array(time)  
        Cap=ex.cap(latitude,longitude,timeSec)[0]
        
        DebTherm=ex.rotation(Cap)[0]
        FinTherm=ex.rotation(Cap)[1]
        NumTherm=ex.rotation(Cap)[2]
        Tour=ex.rotation(Cap)[3]
        
        num=int(self.NbThermEntry.get())
        self.canvas = FigureCanvasTkAgg(ex.graphThermique(num,DebTherm,FinTherm,latitude,longitude,altitude,vario,Tour,NumTherm), master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget (). pack ( side = "bottom" , fill = "both" , expand = True )
        
        self.widget=[self.canvas.get_tk_widget ()]
        

fenetre = Tk()
interface = Fenetre(fenetre)
interface.mainloop()
