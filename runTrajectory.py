import numpy as np
import logging
import dragonfly
from rich.logging import RichHandler


logger = dragonfly.utils.createLogging("debug.log")


# initial Condition
logger.info("get the initial position")
Pos0 = dragonfly.geography.Position.fromLLA(
    lat=np.deg2rad(45),
    long=0,
    alt=0,
    ellipsoid="spherical"
)

logger.info("get initial velocity")
V0 = np.array([100, 0, 0])

# calculate the NED2VEHICLE
logger.info("get angle2dcm")
M = dragonfly.geography.angle2dcm(
    np.deg2rad(90),
    np.deg2rad(45),
    0
)

# Calculate the ECEF2NED
logger.info("get dcm_ecef2ned\n pouet pouet")
M2 = dragonfly.geography.dcm_ecef2ned(np.deg2rad(45), 0)

# Calculate V within NED
V_NED = M.T@V0

print(V_NED)

# calculate gravity
g = dragonfly.gravity.Gravity(Pos0.x,Pos0.y,Pos0.z,earthModel="spherical")



import scipy.integrate

g = 9.81

def forces(t, state):
    g_vec = np.array([0, -g])  # metres per second
    dstate = state.copy()
    dstate[:2] = state[2:]  # vitesse
    dstate[2:] = g_vec  # accélération

    return dstate


state0 = np.array([0.0, 100.0, 100.0, 100.0])
t = np.arange(0.0, 100, 0.1)

model = scipy.integrate.RK45(forces, t.min(), state0, t.max(),max_step = 0.01, atol=6.8e-16, rtol=2.5e-12)

tc = model.t
alt = model.y[1]

print(alt)

while tc < t.max() and alt >=0 :
    model.step()
    tc = model.t
    alt = model.y[1]
    x = model.y
    print("time: ", tc, "altitude : ", x[1])


def touche_le_sol(t, y, *args):
    return y[1]


touche_le_sol.terminal = True

sol = scipy.integrate.solve_ivp(
    forces,
    (t.min(), t.max()),
    state0,
    t_eval=t,
    events=touche_le_sol,
)
print("toto")
print(sol.y[:][1])
