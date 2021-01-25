import os
import numpy as np
import matplotlib.pyplot as plt
import flopy

#Datos del modelo
name = "tutorial01_mf6"
h1 = 100
h2 = 90
Nlay = 10
N = 101
L = 400.0
H = 50.0
k = 1.0
#Crear objeto de simulación (busca la carpeta especializada para guardar los archivos)
sim = flopy.mf6.MFSimulation(
    sim_name=name, exe_name="C:\12-DIPLOMADO\Programas\mf6.2.0\bin", version="mf6", sim_ws="workspace"
)

#Crea el TDIS objeto Flopy
tdis = flopy.mf6.ModflowTdis(
    sim, pname="tdis", time_units="DAYS", nper=1, perioddata=[(1.0, 1, 1.0)]
)
