#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 19 16:03:52 2024

@author: tfrn
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv(
    '/home/tfrn/Documents/Stage_TDV/test_bathy_Beauduc/sondeur_insitu_comparaison.csv', delimiter=';', decimal=',')

delta = data.Sondeur - data.Mesure
std = np.std(delta)
mean = np.mean(delta)

fig, ax = plt.subplots()
ax.scatter(data.Sondeur, data.Mesure )
ax.set_xlabel('Sondeur')
ax.set_ylabel('Mesures in situ')
ax.grid('on')

fig, ax = plt.subplots()
ax.boxplot(delta)
ax.set_title('Repartition statistique de $\\Delta$ Sondeur - Insitu')
