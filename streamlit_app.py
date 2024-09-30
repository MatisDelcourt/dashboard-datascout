import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from components import accueil, index_performance, radar_pizza, scatter_plot

# Barre latérale pour la navigation
st.sidebar.title("Navigation")
selection = st.sidebar.radio("Aller à", ["Accueil", "Index de performance", "Index de similarité", 
                                         "Radar Comparaison", "Radar Pizza", "Scatter Plot", 
                                         "Beeswarm", "Shotmap"])

# Gestion des pages
if selection == "Accueil":
    accueil.show()

elif selection == "Index de performance":
    index_performance.show()

elif selection == "Radar Pizza":
    radar_pizza.show()

elif selection == "Scatter Plot":
    scatter_plot.show()