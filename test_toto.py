import dragonfly

from dragonfly.constant import EarthModel

a = dragonfly.constant.LINE_SIZE
print(a)

ee = dragonfly.constant.EarthModel()
print(ee.earthRotationRate)