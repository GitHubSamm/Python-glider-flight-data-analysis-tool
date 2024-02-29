# -*- coding: utf-8 -*-
"""
Created on Fri Jan 29 16:19:57 2021

@author: marin
"""

from matplotlib.figure import Figure
import math as m
import matplotlib.pyplot as plt
import numpy as np
import shutil as sh #Bibliothèque pour copier un fichier
import webbrowser
import folium   #Bibliothèque pour créer une carte 
from folium.vector_layers import PolyLine

#Attention de bien convertir le fichier IGC en fichier texte .txt
"""Exctraction des listes et d'autres information sur l'aeronef"""

#Autres fichiers disponibles:
    #2020-06-15-Trace.txt
    #2020-06-13-Trace.txt
    
def recupdonnee(nomdufichier):
    sh.copyfile(nomdufichier,nomdufichier[:-3]+"txt")#copie le fichier igc pour pouvoir le transformer en txt sans l'ecraser
    new=nomdufichier[:-3]+"txt"
    with open(new,'r') as file: #Ouvre le fichier Texte  
        time=[]
        lat=[]
        long=[]
        alti=[]
        date=""
        L=""
        x=0
        
        for lines in file: #Parcour chaques lines du fichier
            L=lines
            if L[0]=="B":   
                #Je selectionne la ligne utile en regardant si elle commence par B (à voir si ça fonctionne pour tous les fichiers)
                time.append(L[1:7])
                lat.append(L[7:15])
                long.append(L[15:24])
                alti.append(int(L[31:35]))
            x+=1
            if x==8:
                date=lines #Utilisé dans la suite du programme pour obtenir la date 
                
    CalRoute=["N","E"]        
    for i in range (len(lat)):
        
        """Enlever le N et E à la fin des coordonnés et transforme en "-" si besoin"""
        """Pour la latitude """
        L=lat[i]
        x=float(L[0:2])+float(L[2:4])/60+float(L[4:7])/60000
        if L[-1]=="N":
              lat[i]=x
              CalRoute[0]="N"
        else:
              lat[i]=-x
              CalRoute[0]="S"
        """Pour la longitude"""     
        G=long[i]
        x=float(G[0:3])+float(G[3:5])/60+float(G[5:8])/60000
        if G[-1]=="E":
            long[i]=x
            CalRoute[1]="E"
        else:
            long[i]=-x
            CalRoute[0]="O"
    return time,lat,long,alti,date

def conversion(time,lat,long,alti):
    
    
        
    
    r=6371000
    X=[]
    Y=[]
    Z=[]
    
   
    
    for i in range (len(lat)):
        
        
            
    
        """Convertion en coordonnée cartesienne"""
        
        X.append(r*np.sin(float(long[i])*m.pi/180)*np.cos(float(lat[i])*m.pi/180))
        Y.append(r*np.sin(float(long[i])*m.pi/180)*np.sin(float(lat[i])*m.pi/180))
        Z.append(r*np.cos(float(long[i])*m.pi/180))
        
    timeSec=[]
    for i in range (len(time)):
        """Convertion du temps en seconde"""
        A=""
        A=time[i]
        timeSec.append(int(A[0:2])*3600+int(A[2:4])*60+int(A[4:6]))
    
        
        
    return X,Y,Z,timeSec

def Vario(alti,timeSec):
    
    vario=[]
    
    for j in range (0,len(timeSec)-1):
        
        diff=int(timeSec[j+1]-timeSec[j])
        
        """Définir le vario en chaque instant"""
        vario.append((float(alti[j+1])-float(alti[j]))/diff) 
    vario.append(0)
    return vario


def temps(time):
    timeSec=[]
    for i in range (len(time)):
        """Convertion du temps en seconde"""
        A=""
        A=time[i]
        timeSec.append(int(A[0:2])*3600+int(A[2:4])*60+int(A[4:6]))
    
    return timeSec

def Vitesses(X,Y,Z,timeSec,lat,long):
    
    Vx=[]
    Vy=[]
    Vz=[]
    Vo=[]
    Va=[]
    for j in range (0,len(timeSec)-1):
        
        diff=int(timeSec[j+1]-timeSec[j])
        
        
        """Vitesses"""
        Vx.append(abs((float(X[j+1])-float(X[j]))/diff))
        Vy.append(abs((float(Y[j+1])-float(Y[j]))/diff))
        Vz.append(abs((float(Z[j+1])-float(Z[j]))/diff))
        Vo.append((((Vx[j]**2)+(Vy[j]**2)+(Vz[j]**2))**(1/2))*3.6) #Vitesse en km/h
        Va.append((((((lat[j+1]-lat[j])*111)**2)+(((long[j+1]-long[j])*111)**2))**(1/2)*3600)/diff)
    Vo.append(0)
    
    return Vz,Vy,Vz,Vo,Va



def trajectoire(X,Y,Z,Name):
    
    f=plt.figure()
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.title("{} en fonction de la trajectoire".format(Name))
    g=plt.scatter(X, Y, c=Z, edgecolors='none',cmap=plt.get_cmap("jet")) #marker='o' entre c=Z, et edgecolors
    #Pour modifier la couleur http://www.python-simple.com/python-matplotlib/couleurs-matplotlib.php
    plt.subplots_adjust(bottom=0.1, right=0.8, top=0.9)
    cax = plt.axes([0.85, 0.1, 0.075, 0.8])
    plt.colorbar(cax=cax)
    
   
    return f

def Affichage_carte(X,Y):
    
    #Création d'une carte
    map = folium.Map(tiles='OpenStreetMap', zoom_start=10)
    
    D=[X[0],Y[0]]
    A=[X[-1],Y[-1]]
    #Positioner des marqueurs sur cette carte
    folium.Marker(D,popup='Décollage',icon=folium.Icon(color='green')).add_to(map) #Place les différentes positions GPS sur la carte
    folium.Marker(A,popup='Atterissage',icon=folium.Icon(color='red')).add_to(map) 
    
    #Donne les coordonnées en chaque points de la carte 
    map.add_child(folium.LatLngPopup())
    
    coord=[]
    #Tracer une ligne entre ces points 
    for i in range (len(X)):
        coord.append([X[i],Y[i]])
  

    PolyLine(locations=coord, popup='Vol',color="red", weight=1.5, opacity=1).add_to(map)   
    
    #Enregistre et affiche cette carte
    map.save(outfile='Trace.html')     #Enregistre la trace dans le même repertoire que ce programme 
    return webbrowser.open('Trace.html')

def Altitude(altitude,timeSec):
    f=plt.figure()
    plt.plot(timeSec,altitude,"-k")
    plt.xlabel("temps en secondes")
    plt.ylabel("altitude en mètres")
    plt.title("Altitude en fonction du temps")
    return f

def pourcentageAltitude(vario):
    m=0
    d=0
    for i in range(0,len(vario)):
        if vario[i] > 0:
            m +=1
        if vario[i] < 0:
            d += 1
            
    return "Le planeur était en montée {}% du temps de vol et en descente {}% du temps de vol.".format(round((m/len(vario))*100,1),round((d/len(vario))*100,1))

def Finesse(X,Y,alti,lat,long,Name):
    gliste=[]
    Daeroport=[]
    
    for i in range(len(X)):
        
        a = ((X[i]-X[0])**2+(Y[i]-Y[0])**2)**(1/2)    #Calcule la distance entre le planeur et l'aérodrome (position 0)
        Daeroport.append(a)
        
        if alti[i]<=alti[0]:
            gliste.append(0)
        
        else:
            g = Daeroport[i]/(alti[i]-alti[0])
            if g<100:
                gliste.append(g)
            else:
                gliste.append(0)
    plt.ioff()
    f=plt.figure()
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.title("{} en fonction de la trajectoire".format(Name))
    plt.scatter(lat, long, c=gliste, edgecolors='none',cmap=plt.get_cmap("RdYlGn_r")) #marker='o' entre c=Z, et edgecolors
    #Pour modifier la couleur http://www.python-simple.com/python-matplotlib/couleurs-matplotlib.php
    
    plt.subplots_adjust(bottom=0.1, right=0.8, top=0.9)
    cax = plt.axes([0.85, 0.1, 0.075, 0.8])
    plt.colorbar(cax=cax)
    plt.show()
    
    return f

def cap(lat,long,timeSec):
    Vsol=[]
    Cap=[]
    for j in range (0,len(timeSec)-1):
        
        diff=int(timeSec[j+1]-timeSec[j])
        
    for j in range (len(lat)-1):
        
        Dlat=lat[j+1]-lat[j] # =Dot Product
        Dlong=long[j+1]-long[j] # =Cross Product
        
        length=(Dlat**2+Dlong**2)**(1/2)
        
        Distance=1852*60*m.acos(m.sin(long[j])*m.sin(long[j+1])+m.cos(long[j])*m.cos(long[j+1])*m.cos(Dlat))
        Vsol.append(Distance*3.6/diff) #En km/h
        
        if Dlong<0:
            if length!=0:
                Cap.append(360-m.acos(Dlat/length)*180/m.pi)
        else:
            if length!=0:
                Cap.append(m.acos(Dlat/length)*180/m.pi)

    return Cap,Vsol

def VentGeneral(Cap,Vsol):
    # print(min(Vsol),Cap[Vsol.index(min(Vsol))])
    # print(max(Vsol),Cap[Vsol.index(max(Vsol))])
    Text="Vent de {} km/h venant du cap {}".format(round((min(Vsol)+max(Vsol))/2,1),round(Cap[Vsol.index(min(Vsol))],1))
    return Text

def VentThermique(num,Vsol,DebTherm,FinTherm,Cap,lat,long): #Compris entre 0 et len(NumTherm)
    x=Vsol[DebTherm[num]:FinTherm[num]]
    y=Cap[DebTherm[num]:FinTherm[num]]
    plt.scatter(y,x)
    plt.title('Vitesse du vent en km/h en fonction du Cap')
    plt.xlabel('Cap')
    plt.ylabel('Vitesse Sol')    
    print("Vent de {} km/h venant du cap {}° pour le thermique {}".format(round((min(x)+max(x))/2,1),round(y[x.index(min(x))],1),num))
    print("Aux coordonées GPS {}°lat; {}°long".format(lat[DebTherm[num]],long[DebTherm[num]]))
    return plt.show()


"""Affichage graphique des rotations et une approximation du centre du thermique"""
def graphThermique(num,DebTherm,FinTherm,lat,long,alti,vario,Tour,NumTherm): #Compris entre 0 et len(NumTherm)
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    
    x=lat[DebTherm[num]:FinTherm[num]]
    y=long[DebTherm[num]:FinTherm[num]]
    z=alti[DebTherm[num]:FinTherm[num]]
    a=vario[DebTherm[num]:FinTherm[num]]
    #Premier Grpahique avec le vol
    ax.scatter(x, y, z, c=a, cmap=plt.get_cmap("winter"))
    
    #Thermique
    W=[]
    U=[]
    V=[]
    a=Tour.index(DebTherm[num]) 
    for t in range(0,NumTherm[num]-1):
        W.append(sum(alti[Tour[a+t]:Tour[a+t+1]])/len(alti[Tour[a+t]:Tour[a+t+1]]))
    
        tempLat=[]
        tempLong=[]
        S=0
        for T in range(Tour[a+t],Tour[a+t+1]):
            if vario[T]>0:
                S+=vario[T]
                if lat[T]<=0 and lat[T]*vario[T]>=0:
                    tempLat.append(-lat[T]*vario[T])
                else:
                    tempLat.append(lat[T]*vario[T]) 
                if long[T]<=0 and long[T]*vario[T]>=0:
                    tempLong.append(-long[T]*vario[T])
                else:
                    tempLong.append(long[T]*vario[T])
        if sum(tempLat)>0 or sum(tempLong)>0:
            U.append(sum(tempLat)/S)
            V.append(sum(tempLong)/S)
        else: 
            del W[-1]
        
    ax.scatter(U, V, W, c='r')
    plt.plot(U,V,W,c='r')
    
    ax.set_title(("Thermique numéro {} sur {}, comprenant {} rotations").format(num,len(NumTherm)-1,NumTherm[num]))
    ax.set_xlabel("latitude")
    ax.set_ylabel("longitude")
    ax.set_zlabel("altitude")
    return fig

def rotation(Cap):
    Tour=[]
    Var=0
    Test=[]
    for k in range (0,len(Cap)-1):
        
            if abs(Cap[k+1]-Cap[k])>180:
                if Cap[k+1]>Cap[k]:
                    Var=Var+Cap[k]+360-Cap[k+1]
                if Cap[k]>Cap[k+1]:
                    Var=Var+Cap[k+1]+360-Cap[k]
                    
            else:
                if Cap[k+1]>Cap[k]:
                    Var=Var+abs(Cap[k+1]-Cap[k])
                if Cap[k+1]<=Cap[k]:
                    Var=Var-abs(Cap[k+1]-Cap[k])
            Test.append(Var)
                
            if Var>=360:
                Var=Var-360
                Tour.append(k)
            if Var<-360:
                Var+=360
                Tour.append(k)               
        
    DebTherm=[]  
    FinTherm=[]
    NumTherm=[]
    x=0
    while x<(len(Tour)-2):
        if Tour[x+1]-Tour[x]<60:
            debut=Tour[x]
            nbrTour=0
            while Tour[x+1]-Tour[x]<60 and x<(len(Tour)-2):
                nbrTour+=1
                x+=1   
            fin=Tour[x]
            DebTherm.append(debut)
            FinTherm.append(fin)
            NumTherm.append(nbrTour)
    
        else:
            x+=1

    return DebTherm,FinTherm,NumTherm,Tour

def TourDePisteG (d,Lo,longP,latP,long,lat):

    #d=120 #direction de la piste
    a=180-d
    o=(a*m.pi)/180
    Lo=Lo*10**2 #longueur piste
    la=80*10**2 #largeur piste
    D=800*10**2 #distance entre les 2 angles du tour de piste
    x=100*10**2 #largeur tour de piste
    #coordonnees centre de la piste
    
    #tour de piste avec piste sur la droite
    X=[(-1/2)*((Lo**2+la**2)**(1/2))*(-1)*m.sin(o-m.atan(la/Lo)),(1/2)*((Lo**2+la**2)**(1/2))*m.sin(o+m.atan(la/Lo)),(-1/2)*((Lo**2+la**2)**(1/2))*m.sin(o-m.atan(la/Lo)),(1/2)*((Lo**2+la**2)**(1/2))*(-1)*m.sin(o+m.atan(la/Lo)),(-1/2)*((Lo**2+la**2)**(1/2))*(-1)*m.sin(o-m.atan(la/Lo))]
    Y=[(1/2)*((Lo**2+la**2)**(1/2))*(-1)*m.cos(o-m.atan(la/Lo)),(-1/2)*((Lo**2+la**2)**(1/2))*m.cos(o+m.atan(la/Lo)), (1/2)*((Lo**2+la**2)**(1/2))*m.cos(o-m.atan(la/Lo)), (-1/2)*((Lo**2+la**2)**(1/2))*(-1)*m.cos(o+m.atan(la/Lo)),(1/2)*((Lo**2+la**2)**(1/2))*(-1)*m.cos(o-m.atan(la/Lo))]
    for i in range (len(X)):
        Y[i]=longP+m.asin(Y[i]/6371000)
        X[i]=latP+m.asin(X[i]/(6371000*m.cos(Y[i])))
        
    E1=[(Lo/2)*m.sin(o),-(Lo/2)*m.cos(o)] #point d'aboutissement
    E1[1]=longP+m.asin(E1[1]/6371000)
    E1[0]=latP+m.asin(E1[0]/(6371000*m.cos(E1[1])))
    
    
    TX=[(((D-(x/2))**2)**(1/2))*m.sin(o-(m.pi/2)),(((D+Lo/2-x/2)**2+(D-(x/2))**2)**(1/2))*m.sin(o-m.atan((D-(x/2))/(D+Lo/2-x/2))),(((D+Lo/2-x/2)**2+(x/2)**2)**(1/2))*m.sin(o-m.atan((x/2)/(D+Lo/2-x/2))),(((Lo/2)**2+(x/2)**2)**(1/2))*m.sin(o-m.atan((x/2)/(Lo/2))),(((Lo/2)**2+(x/2)**2)**(1/2))*m.sin(o+m.atan((x/2)/(Lo/2))),(((D+(Lo/2)+x/2)**2+(x/2)**2)**(1/2))*m.sin(o+m.atan((x/2)/(D+(Lo/2)+x/2))),(((D+(Lo/2)+x/2)**2+(D+(x/2))**2)**(1/2))*m.sin(o-m.atan((D+(x/2))/(D+(Lo/2)+x/2))),(((D+(x/2))**2)**(1/2))*m.sin(o-(m.pi/2))]
    TY=[-(((D-(x/2))**2)**(1/2))*m.cos(o-(m.pi/2)),-(((D+Lo/2-x/2)**2+(D-(x/2))**2)**(1/2))*m.cos(o-m.atan((D-(x/2))/(D+Lo/2-x/2))),-(((D+Lo/2-x/2)**2+(x/2)**2)**(1/2))*m.cos(o-m.atan((x/2)/(D+Lo/2-x/2))),-(((Lo/2)**2+(x/2)**2)**(1/2))*m.cos(o-m.atan((x/2)/(Lo/2))),-(((Lo/2)**2+(x/2)**2)**(1/2))*m.cos(o+m.atan((x/2)/(Lo/2))),-(((D+(Lo/2)+x/2)**2+(x/2)**2)**(1/2))*m.cos(o+m.atan((x/2)/(D+(Lo/2)+x/2))),-(((D+(Lo/2)+x/2)**2+(D+(x/2))**2)**(1/2))*m.cos(o-m.atan((D+(x/2))/(D+(Lo/2)+x/2))),-(((D+(x/2))**2)**(1/2))*m.cos(o-(m.pi/2))]
    for i in range (len(TX)):
        TY[i]=longP+m.asin(TY[i]/6371000)
        TX[i]=latP+m.asin(TX[i]/(6371000*m.cos(TY[i])))
        
    fig=plt.figure()
    plt.plot(X,Y,"-g")
    plt.plot(E1[0],E1[1],'.r')
    plt.plot(TX,TY,'k',linestyle = 'dashed')
    plt.plot(long[-80:-1],lat[-80:-1],'-m')
    plt.title('Tour de piste')

    return fig

def TourDePisteD (d,Lo,longP,latP,long,lat):

    #d=120 #direction de la piste
    a=180-d
    o=(a*m.pi)/180
    Lo=Lo*10**2 #longueur piste
    la=80*10**2 #largeur piste
    D=800*10**2 #distance entre les 2 angles du tour de piste
    x=100*10**2 #largeur tour de piste
    
    #tour de piste avec piste sur la droite
    X=[(-1/2)*((Lo**2+la**2)**(1/2))*(-1)*m.sin(o+m.atan(la/Lo)),(1/2)*((Lo**2+la**2)**(1/2))*m.sin(o-m.atan(la/Lo)),(-1/2)*((Lo**2+la**2)**(1/2))*m.sin(o+m.atan(la/Lo)),(1/2)*((Lo**2+la**2)**(1/2))*(-1)*m.sin(o-m.atan(la/Lo)),(-1/2)*((Lo**2+la**2)**(1/2))*(-1)*m.sin(o+m.atan(la/Lo))]
    Y=[(1/2)*((Lo**2+la**2)**(1/2))*(-1)*m.cos(o+m.atan(la/Lo)),(-1/2)*((Lo**2+la**2)**(1/2))*m.cos(o-m.atan(la/Lo)), (1/2)*((Lo**2+la**2)**(1/2))*m.cos(o+m.atan(la/Lo)), (-1/2)*((Lo**2+la**2)**(1/2))*(-1)*m.cos(o-m.atan(la/Lo)),(1/2)*((Lo**2+la**2)**(1/2))*(-1)*m.cos(o+m.atan(la/Lo))]
    for i in range (len(X)):
        Y[i]=longP+m.asin(Y[i]/6371000)
        X[i]=latP+m.asin(X[i]/(6371000*m.cos(Y[i])))
        
    E1=[(Lo/2)*m.sin(o),-(Lo/2)*m.cos(o)] #point d'aboutissement
    E1[1]=longP+m.asin(E1[1]/6371000)
    E1[0]=latP+m.asin(E1[0]/(6371000*m.cos(E1[1])))
    
    TX=[(((D-(x/2))**2)**(1/2))*m.sin(o+(m.pi/2)),(((D+Lo/2-x/2)**2+(D-(x/2))**2)**(1/2))*m.sin(o+m.atan((D-(x/2))/(D+Lo/2-x/2))),(((D+Lo/2-x/2)**2+(x/2)**2)**(1/2))*m.sin(o+m.atan((x/2)/(D+Lo/2-x/2))),(((Lo/2)**2+(x/2)**2)**(1/2))*m.sin(o+m.atan((x/2)/(Lo/2))),(((Lo/2)**2+(x/2)**2)**(1/2))*m.sin(o-m.atan((x/2)/(Lo/2))),(((D+(Lo/2)+x/2)**2+(x/2)**2)**(1/2))*m.sin(o-m.atan((x/2)/(D+(Lo/2)+x/2))),(((D+(Lo/2)+x/2)**2+(D+(x/2))**2)**(1/2))*m.sin(o+m.atan((D+(x/2))/(D+(Lo/2)+x/2))),(((D+(x/2))**2)**(1/2))*m.sin(o+(m.pi/2))]
    TY=[-(((D-(x/2))**2)**(1/2))*m.cos(o+(m.pi/2)),-(((D+Lo/2-x/2)**2+(D-(x/2))**2)**(1/2))*m.cos(o+m.atan((D-(x/2))/(D+Lo/2-x/2))),-(((D+Lo/2-x/2)**2+(x/2)**2)**(1/2))*m.cos(o+m.atan((x/2)/(D+Lo/2-x/2))),-(((Lo/2)**2+(x/2)**2)**(1/2))*m.cos(o+m.atan((x/2)/(Lo/2))),-(((Lo/2)**2+(x/2)**2)**(1/2))*m.cos(o-m.atan((x/2)/(Lo/2))),-(((D+(Lo/2)+x/2)**2+(x/2)**2)**(1/2))*m.cos(o-m.atan((x/2)/(D+(Lo/2)+x/2))),-(((D+(Lo/2)+x/2)**2+(D+(x/2))**2)**(1/2))*m.cos(o+m.atan((D+(x/2))/(D+(Lo/2)+x/2))),-(((D+(x/2))**2)**(1/2))*m.cos(o+(m.pi/2))]
    for i in range (len(TX)):
        TY[i]=longP+m.asin(TY[i]/6371000)
        TX[i]=latP+m.asin(TX[i]/(6371000*m.cos(TY[i])))
    
    fig = plt.figure()
    plt.plot(X,Y,"-g")
    plt.plot(E1[0],E1[1],'.r')
    plt.plot(TX,TY,'k',linestyle = 'dashed')
    plt.plot(long[-80:-1],lat[-80:-1],'-m')
    plt.title('Tour de piste')

    return fig

def MacCready(timeSec,Vo,vario,Va,long,lat) :
            
    cadrant=[70,80,90,100,110,120,130,140]
    v_opti=Vo
    for j in range(0,len(v_opti)):
        if -0.5 < vario[j] <= 0:
            v_opti[j] = cadrant[0]
        if -1 < vario[j] <= -0.5:
            v_opti[j] = cadrant[1]
        if -2 < vario[j] <=-1:
            v_opti[j] = cadrant[2]
        if -3 < vario[j] <= -2:
            v_opti[j] = cadrant[3]
        if -4 < vario[j] <= -3:
            v_opti[j] = cadrant[4]
        if -5 < vario[j] <= -4:
            v_opti[j] = cadrant[5]
        if -6 < vario[j] <= -5:
            v_opti[j] = cadrant[6]
        if -7 < vario[j] <= -6:
            v_opti[j] = cadrant[7]
            
    
    V_diff=[]
    for k in range(0,len(Va)):
        if vario[k] <=0:
            V_diff.append(abs(Va[k]-v_opti[k]))
        else:
            V_diff.append(0)
    V_diff.append(0) 
    
    fig = plt.figure()
    plt.scatter(long, lat, c=V_diff, edgecolors='none', cmap=plt.get_cmap("jet"))  
    #cax = plt.axes([0.85, 0.1, 0.075, 0.8])
    plt.colorbar()#cax=cax)
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.title("Ecart absolu par rapport au Mac Cready")
    
    return fig