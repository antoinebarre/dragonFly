import numpy as np
import logging
import dragonfly
from rich.logging import RichHandler


# Define logging
logger = logging.getLogger(__name__)

# the handler determines where the logs go: stdout/file
shell_handler = RichHandler()
file_handler = logging.FileHandler("debug.log", mode="w")

logger.setLevel(logging.DEBUG)
shell_handler.setLevel(logging.DEBUG)
file_handler.setLevel(logging.DEBUG)

# the formatter determines what our logs will look like
fmt_shell = '%(message)s'
fmt_file = '%(levelname)s %(asctime)s [%(filename)s:%(funcName)s:%(lineno)d] %(message)s'

shell_formatter = logging.Formatter(fmt_shell)
file_formatter = logging.Formatter(fmt_file)

# here we hook everything together
shell_handler.setFormatter(shell_formatter)
file_handler.setFormatter(file_formatter)

logger.addHandler(shell_handler)
logger.addHandler(file_handler)


# initial Condition
logger.info("get the initial position")
Pos0 = dragonfly.geography.Position.fromLLA(
    lat=np.deg2rad(45),
    long=0,
    alt=0
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
logger.info("get dcm_ecef2ned")
M2 = dragonfly.geography.dcm_ecef2ned(np.deg2rad(45), 0)

# Calculate V within NED
V_NED = M.T@V0

print(V_NED)

