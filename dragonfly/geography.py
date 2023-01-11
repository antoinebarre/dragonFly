"""SUBMODULE GEOGRAPHY
    This module contains all the geographic utilities for the DragonFlly application


LIST OF CLASSES:
    - Position : geographic position classes
"""

#MODULES IMPORT
from dataclasses import dataclass


class Position:
    """Class for the management of ECEF position
    """

    def __init__(self,x:float,y:float,z:float):
        """create a Position object based on ECEF coordinates

        Args:
            x (float): x coordinates in ECEF
            y (float): y coordinates in ECEF
            z (float): z coordinates in ECEF
        """
        self.x = x
        self.y = y
        self.z = z

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        try:
            self._x = float(value)
        except TypeError:
            raise TypeError('"x" shall be a scalar not a list or a tuple')
        except ValueError:
            raise ValueError('"x" shall be a number') from None

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        try:
            self._y = float(value)
        except TypeError:
            raise TypeError('"y" shall be a scalar not a list or a tuple')
        except ValueError:
            raise ValueError('"y" shall be a number') from None
    
    @property
    def z(self):
        return self._z

    @z.setter
    def z(self, value):
        try:
            self._z = float(value)
        except TypeError:
            raise TypeError('"z" shall be a scalar not a list or a tuple')
        except ValueError:
            raise ValueError('"z" shall be a number') from None


    @classmethod
    def fromList(cls,data:list):

        #check if nested list:
        if any(isinstance(ix, list) for ix in data):
            return Position.__fromNestedList(data)
        else:
            return Position.__from1DList(data)
  
    @classmethod
    def __from1DList(cls,data:list):
        """PRIVATE METHOD : create Position from a 1D list"""
        #IO VERIFICATION
        if not isinstance(data,list):
            raise TypeError(f"data shall be a list  [current: {type(data)}] ")
        if len(data)!=3:
            raise ValueError(f"data shall be a list of 3 elements [current: {len(data)}] ")
        
        return Position(data[0],data[1],data[2])

    @classmethod
    def __fromNestedList(cls,datas:list):
        """PRIVATE METHOD : create Position from a Nested list"""

        if not isinstance(datas,list):
            raise TypeError(f"data shall be a list  [current: {type(datas)}] ")

        newObj = [Position.__from1DList(data) for data in datas]
        return newObj

