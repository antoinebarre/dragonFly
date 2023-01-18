""" 
###############################   GRAVITY MODEL  ###############################
"""

""" EXEMPLE GENTRAJ :
CALCUL DU CHAMP DE GRAVITATION TERRESTRE

c	constantes utilisees

	if (tersph) then
	   j2=0.d0
	else
	   j2=1.08263d-3	
	endif

c	calcul de g (grav) dans le repere 1 a partir d'un developpement
c	limite au second ordre du potentiel terrestre
c	U=mu/rho*(1d0-j2*(rt/rho)**2*(3d0*sinphi**2-1d0)/2d0)

	call car2sph(pos,rho,lambda,phi)
	r1=rt/rho
	r2=r1*r1
	sin1=sin(phi)
	sin2=sin1*sin1

	k0=-(mu/rho**3)
	k1=k0*(1d0-1.5d0*j2*r2*(5d0*sin2-1d0))
	k2=k0*(1d0-1.5d0*j2*r2*(5d0*sin2-3d0))

	grav(1)=k1*pos(1)
	grav(2)=k1*pos(2)
	grav(3)=k2*pos(3)



    EXEMPLE MATLAB

    gt(:,1)=-mu./r.^2.*(1+3/2*J2.*(a./r).^2.*(1-5.*(POS_ECEF(:,3)./r).^2)).*POS_ECEF(:,1)./r;
    gt(:,2)=-mu./r.^2.*(1+3/2*J2.*(a./r).^2.*(1-5.*(POS_ECEF(:,3)./r).^2)).*POS_ECEF(:,2)./r;
    gt(:,3)=-mu./r.^2.*(1+3/2*J2.*(a./r).^2.*(3-5.*(POS_ECEF(:,3)./r).^2)).*POS_ECEF(:,3)./r;

"""

#Import Module
from .geography import Position

class Gravite():
    def __init__(self,earthModel:str='WGS84',x_ECEF:float=0,y_ECEF:float=0,z_ECEF:float=0):



        pass

    @classmethod
    def fromECEF(cls,x:float,y:float,z:float):
        pass
    
    @classmethod
    def fromPosition(cls,pos:Position):
        pass

    @staticmethod
    def __calculateGravity(x_ECEF:float,y_ECEF:float,z_ECEF:float):
        pass







def gravite(Position)