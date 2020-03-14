from Resources.Cit_par import *
from math import *
import cmath
Cl=1
import numpy as np



#empty lists to fill with values
lambdas     = []
lambdas_real = []
lambdas_imag = []
t_half      = []
taus        = []
periods     = []
no_per_half = []
log_decr    = []
damp_ratio  = []


#========================SYMMETRIC-MOTIONS=============================

#--------------------------SHORT-PERIOD----------------------------
A_sp = 2 * muc * KY2**2 * (2 * muc - CZadot)
B_sp = - 2 * muc * KY2**2 * CZa - (2 * muc + CZq) * Cmadot - (2 * muc - CZadot) * Cmq
C_sp = CZa * Cmq - (2 * muc + CZq) * Cma

Eig_val_short_period_real = (-B_sp) / (2 * A_sp)
Eig_val_short_period_imag = sqrt(4 * A_sp * C_sp - B_sp**2) / (2 * A_sp)
Eig_val_short_period_1 = complex(Eig_val_short_period_real, Eig_val_short_period_imag)
Eig_val_short_period_2 = complex(Eig_val_short_period_real, -1*Eig_val_short_period_imag)
lambdas.append(Eig_val_short_period_1)
lambdas.append(Eig_val_short_period_2)
lambdas_real.append(Eig_val_short_period_real)
lambdas_imag.append(Eig_val_short_period_imag)



#--------------------------PHUGOID---------------------------------------------------------
A_ph = 2 * muc * (CZa * Cmq - 2 * muc * Cma)
B_ph = 2 * muc * (CXu * Cma - Cmu * CXa) + Cmq * (CZu * CXa - CXu * CZa)
C_ph = CZ0 * (Cmu * CZa - CZu * Cma)

Eig_val_phugoid_real = (-B_ph) / (2 * A_ph)
Eig_val_phugoid_img = cmath.sqrt(4 * A_ph * C_ph - B_ph**2) / (2 * A_ph)
Eig_val_phugoid_1 = complex(Eig_val_phugoid_real, Eig_val_phugoid_img)
Eig_val_phugoid_2 = complex(Eig_val_phugoid_real, -1*Eig_val_phugoid_img)
lambdas.append(Eig_val_phugoid_1)
lambdas.append(Eig_val_phugoid_2)
lambdas_real.append(Eig_val_phugoid_real)
lambdas_imag.append(abs(Eig_val_phugoid_img))




#============================ASYMMETRIC- MOTIONS========================================



#--------------------Aperiodic roll----------------------
lambda_aroll = Clp/(4*mub*KX2)
lambda_aroll_comp = complex(Clp/(4*mub*KX2))
print('Eigenvalue corresponding to aperiodic roll=', lambda_aroll_comp)
lambdas.append(lambda_aroll_comp)
lambdas_real.append(lambda_aroll)



#---------------------Dutch roll--------------------------
#lambda_droll_1=(2*(Cnr+2*KZ2*CYb)+ sqrt(64*KZ2*(4*mub*Cnb+CYb*Cnr)-4*(Cnr+2*KZ2*CYb)**2))/(16*mub*KZ2)
#lambda_droll_2= (2*(Cnr+2*KZ2*CYb)- sqrt(64*KZ2*(4*mub*Cnb+CYb*Cnr)-4*(Cnr+2*KZ2*CYb)**2))/(16*mub*KZ2)

#lambdas.append(lambda_droll_1)
#lambdas.append(lambda_droll_2)
A_droll= 8*mub**2*KZ2
B_droll = -2*mub*(Cnr+ 2*KZ2*CYb)
C_droll = 4*mub*Cnb+CYb*Cnr
disc_droll = B_droll**2-4*A_droll*C_droll
lambda_droll_real = -B_droll/(2*A_droll)
lambda_droll_imag = cmath.sqrt(disc_droll)/(2*A_droll)
print('Eigenvalues corresponding to dutch roll=', [lambda_droll_real+lambda_droll_imag])
lambdas.append(lambda_droll_real+lambda_droll_imag)
lambdas.append(lambda_droll_real-lambda_droll_imag)
lambdas_real.append(lambda_droll_real)

lambdas_imag.append(abs(lambda_droll_imag))
#----------------------Spiral motion----------------------------------
lambda_spiral= (2*Cl*(Clb*Cnr-Cnb*Clr))/(Clp*(CYb*Cnr+4*mub*Cnb)-Cnp*(CYb*Clr+4*mub*Clb))

lambda_spiral_comp= complex((2*Cl*(Clb*Cnr-Cnb*Clr))/(Clp*(CYb*Cnr+4*mub*Cnb)-Cnp*(CYb*Clr+4*mub*Clb)))
print('Eigenvalues corresponding to spiral motion=', lambda_spiral)
lambdas.append(lambda_spiral_comp)
lambdas_real.append(lambda_spiral)
#--------------Time to half the amplitude---------------


def tau(y):
    return -1*c/(Vh_V*y)
#def per(z):
 #   return 2*pi*c/()

for i in lambdas:
    taus.append(tau(i))
print('Times to reach half amplitude=',t_half)
print('The time constants=', taus)

#----------------------Characteristics-------------------------

#------------Half time-----------------
#applies to all eigenvalues
def thalf(x):
    return log(0.5, e) * c / (x * Vh_V) ### The velocity needs to be changed for every eigenmotion, the speed is taken at the beginning of the motion
for i in lambdas_real:
    t_half.append(thalf(i))

#----------Period---------------------
#applies to complex eigvalues only

def per(z):
    return 2*pi*c/(z*Vh_V)#again the velocity needs to be appended
for j in lambdas_imag:
    periods.append(per(j))

#-----------Time constant------------------
#only applies to real eigenvalues
tau_aperiod = -1*c/lambda_aroll
tau_spiral = -1*c/lambda_spiral
taus.append(tau_aperiod)
taus.append(tau_spiral)

#----------C half values--------------
#only applies to motions that have an imaginary part
c_half_shawty = t_half[0]/periods[0]
c_half_phugoid= t_half[1]/periods[1]
c_half_droll = t_half[3]/periods[2]
no_per_half.append(c_half_shawty)
no_per_half.append(c_half_phugoid)
no_per_half.append(c_half_droll)

#-----------Logarithmic decrement---------
#only applies to motions that have an imaginary part
dec_shawty = lambdas_real[0]*Vh_V*periods[0]/c
dec_phugoid = lambdas_real[1]*Vh_V*periods[1]/c
dec_droll = lambdas_real[3]*Vh_V*periods[2]/c
log_decr.append(dec_shawty)
log_decr.append(dec_phugoid)
log_decr.append(dec_droll)

#-----------Damping ratio------------------
#only applies to motions that have an imaginary part
damp_shawty = -1*lambdas[0].real/abs(lambdas[0])
damp_phugoid = -1*lambdas[2].real/abs(lambdas[2])
damp_droll = -1*lambda_droll_real/abs(lambda_droll_real+lambda_droll_imag)
damp_ratio.append(damp_shawty)
damp_ratio.append(damp_phugoid)
damp_ratio.append(damp_droll)

