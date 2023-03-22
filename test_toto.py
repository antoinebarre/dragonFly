import dragonfly

from dragonfly.constants import EarthModel

a = dragonfly.constants.LINE_SIZE
print(a)

ee = dragonfly.constants.EarthModel()
print(ee.earthRotationRate)