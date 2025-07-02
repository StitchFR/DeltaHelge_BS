
import streamlit as st

TITRES = {
    "T1": "PRICER",
    "titre1":"Titre",
    "titre2": "Titre",
}

ST1= "Texte explique"

LSTPRODUCTS = {
    "P1": "Call",
    "P2": "Put",
    "P3": "Twin win",}

LSTPRODUCTS2 = {
    "P1": "Black Scholes",  
    "P2": "Dupire (Local Volatility)",
    "P3": "Heston (Stochastic Volatility)",
}

nomdelapage = "Pricer"
titrerectangle = "titre rectangle"
nmselectbox1 = "Produit"    
nmselectbox2 = "Modele de pricing"
nmimput1 = "Sous Jacent"
nmimput2 = "Simulation"
nmimput3 = "Periode"


NB_INPUTS = {
    "nmimput1": {"min": 1, "max": 10, "step": 1},        # Sous Jacent
    "nmimput2": {"min": 10, "max": 2000000, "step": 1},   # Simulation
    "nmimput3": {"min": 100, "max": 360*12*24, "step": 1},        # Periode
}

titrerectangle2 =  "Type Produit"


produit1dict = {
    "var1": ["selectbox",100,0,200,1],#type d'objet, valeur initiale, min, max, step
    "var2": ["selectbox", 100, 0, 200, 1],
    "var3": ["selectbox", 100, 0, 200, 1],
}

produit2dict = {
    "var1": ["selectbox",100,0,200,1],#type d'objet, valeur initiale, min, max, step
    "var2": ["selectbox", 100, 0, 200, 1],
    "var3": ["selectbox", 100, 0, 200, 1],
}

produit3dict = {
    "var1": ["selectbox",100,0,200,1],#type d'objet, valeur initiale, min, max, step
    "var2": ["selectbox", 100, 0, 200, 1],
    "var3": ["selectbox", 100, 0, 200, 1],
    "var4": ["selectbox", 100, 0, 200, 1],
    "var5": ["selectbox", 100, 0, 200, 1],
}        

produits_dict = {
    "Produit 1": produit1dict,
    "Produit 2": produit2dict,
    "Produit 3": produit3dict,
}
