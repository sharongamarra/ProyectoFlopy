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

#Crea el IMS objeto Flopy
ims = flopy.mf6.ModflowIms(sim, pname="ims", complexity="SIMPLE")

#Crear el objeto de modelo de flujo de agua subterránea Flopy (gwf)
model_nam_file = "{}.nam".format(name)
gwf = flopy.mf6.ModflowGwf(sim, modelname=name, model_nam_file=model_nam_file)

#Crear el paquete de discretización
bot = np.linspace(-H / Nlay, -H, Nlay)
delrow = delcol = L / (N - 1)
dis = flopy.mf6.ModflowGwfdis(
    gwf,
    nlay=Nlay,
    nrow=N,
    ncol=N,
    delr=delrow,
    delc=delcol,
    top=0.0,
    botm=bot,
)

#Crear el IC paquete de condiciones iniciales
start = h1 * np.ones((Nlay, N, N))
ic = flopy.mf6.ModflowGwfic(gwf, pname="ic", strt=start)

#Crear el NPF paquete de flujo
npf = flopy.mf6.ModflowGwfnpf(gwf, icelltype=1, k=k, save_flows=True)

#Crear el CHD paquete de cabeza constante
chd_rec = []
chd_rec.append(((0, int(N / 4), int(N / 4)), h2))
for layer in range(0, Nlay):
    for row_col in range(0, N):
        chd_rec.append(((layer, row_col, 0), h1))
        chd_rec.append(((layer, row_col, N - 1), h1))
        if row_col != 0 and row_col != N - 1:
            chd_rec.append(((layer, 0, row_col), h1))
            chd_rec.append(((layer, N - 1, row_col), h1))
chd = flopy.mf6.ModflowGwfchd(
    gwf,
    maxbound=len(chd_rec),
    stress_period_data=chd_rec,
    save_flows=True,
)
