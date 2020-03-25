from Resources.Cit_par import Cit_par_Values
import scipy as np
import control.matlab as ml
import matplotlib.pyplot as plt
import Read
from dynamic import alpha_1, theta_1, u_1, q_1, alpha_2, theta_2, u_2, q_2, phi, r_3, p_3, r_4, p_4, r_5, p_5


#####DEFINITIONS######


def inputcr(delta_values, time_value, t_array, time_ini,
            time_fin):  # (deflections values, time of flight, time of simulation, start time of input, end time of input)
    cell_ini = np.where(time_value == time_ini)[0][0]
    cell_fin = np.where(time_value == time_fin)[0][0]
    values = delta_values[cell_ini:cell_fin]
    delta_values_a = np.array([values])
    delta_values_aa = np.array([i * 0.017455 for i in delta_values_a])
    missing = len(t_array) - len(values)
    zeros = np.zeros((1, missing))
    delta_values_aaa = np.hstack((delta_values_aa, zeros))
    delta_values_array = np.transpose(delta_values_aaa)

    return delta_values_array, cell_ini


####GETTING DATA FOR INPUTS###########

parameters = np.array(
    ['vane_AOA', 'elevator_dte', 'column_fe', 'lh_engine_FMF', 'rh_engine_FMF', 'lh_engine_itt', 'rh_engine_itt',
     'lh_engine_OP', 'rh_engine_OP', 'lh_engine_fan_N1', 'lh_engine_turbine_N2', 'rh_engine_fan_N1',
     'rh_engine_turbine_N2',
     'lh_engine_FU', 'rh_engine_FU', 'delta_a', 'delta_e', 'delta_r', 'Gps_date', 'Gps_utcSec', 'Ahrs1_Roll',
     'Ahrs1_Pitch', 'Fms1_trueHeading', 'Gps_lat', 'Gps_long', 'Ahrs1_bRollRate', 'Ahrs1_bPitchRate', 'Ahrs1_bYawRate',
     'Ahrs1_bLongAcc', 'Ahrs1_bLatAcc', 'Ahrs1_bNormAcc', 'Ahrs1_aHdgAcc', 'Ahrs1_xHdgAcc', 'Ahrs1_VertAcc',
     'Dadc1_sat', 'Dadc1_tat', 'Dadc1_alt', 'Dadc1_bcAlt', 'Dadc1_bcAltMb', 'Dadc1_mach', 'Dadc1_cas', 'Dadc1_tas',
     'Dadc1_altRate', 'measurement_running', 'measurement_n_rdy', 'display_graph_state', 'display_active_screen',
     'time'])

reference_data, reference_headers, reference_descriptions = Read.get_data('ref_data')
flight_data, flight_headers, flight_descriptions = Read.get_data('testflight')

delta_e_index = np.where(parameters == 'delta_e')[0].flat[0]
delta_r_index = np.where(parameters == 'delta_r')[0].flat[0]
delta_a_index = np.where(parameters == 'delta_a')[0].flat[0]
time_index = np.where(parameters == 'time')[0].flat[0]

reference_delta_e = np.array(reference_data[reference_headers[delta_e_index]])
reference_delta_r = np.array(reference_data[reference_headers[delta_r_index]])
reference_delta_a = np.array(reference_data[reference_headers[delta_a_index]])
time = np.array(reference_data[[reference_headers[time_index]]])

flight_delta_e = np.array(flight_data[flight_headers[delta_e_index]])
flight_delta_r = np.array(flight_data[flight_headers[delta_r_index]])
flight_delta_a = np.array(flight_data[flight_headers[delta_a_index]])
time = np.array(reference_data[[reference_headers[time_index]]])


# class ABCDmat():
# from Resources.Cit_par import Cit_par_class
# def __init__(self):
# Cit_par_Values(self)

def ABCD(flight, motion):
    rho, m, Cma, CZ0, Cl, hp0, V0, th0, Cmde, S, Sh, Sh_S, lh, c, lh_c, b, bh, A, Ah, Vh_V, ih, rho0, lamda, Temp0, R, g, W, muc, mub, KX2, KZ2, KXZ, KY2, Cmac, CNha, depsda, CX0, CXu, CXa, CXadot, CXq, CXde, CZ0, CZu, CZa, CZadot, CZq, CZde, Cmu, Cmadot, Cmq, CYb, CYbdot, CYp, CYr, CYda, CYdr, Clb, Clp, Clr, Clda, Cldr, Cnb, Cnbdot, Cnp, Cnr, Cnda, Cndr = Cit_par_Values(
        flight, motion)
    
    #These are the parameters that need to be uncommented to obtained the improved PHUGOID
    # CZu = -0.28      #PH
    # Cmq = -8         #PH
    # CXu = -0.004     #PH

    # These are the parameters that need to be uncommented to obtained the improved DUTCH ROLL
    # CYb = -1.35      #DUTCH
    # Cnb = 0.075      #DUTCH
    # Cnr = -0.21      #DUTCH

    ########## ASYMMETRIC EQUATIONS OF MOTION IN STATE-SPACE FORM ##########
    A1 = np.array([[(V0 / b) * (CYb / 2 / mub), (V0 / b) * (Cl / 2 / mub), (V0 / b) * (CYp / 2 / mub),
                    (V0 / b) * (CYr - 4 * mub) / 2 / mub],
                   [0, 0, 2 * V0 / b, 0],
                   [(V0 / b) * ((Clb * KZ2 + Cnb * KXZ) / (4 * mub * (KX2 * KZ2 - KXZ ** 2))), 0,
                    (V0 / b) * ((Clp * KZ2 + Cnp * KXZ) / (4 * mub * (KX2 * KZ2 - KXZ ** 2))),
                    (V0 / b) * ((Clr * KZ2 + Cnr * KXZ) / (4 * mub * (KX2 * KZ2 - KXZ ** 2)))],
                   [(V0 / b) * ((Clb * KXZ + Cnb * KX2) / (4 * mub * (KX2 * KZ2 - KXZ ** 2))), 0,
                    (V0 / b) * ((Clp * KXZ + Cnp * KX2) / (4 * mub * (KX2 * KZ2 - KXZ ** 2))),
                    (V0 / b) * ((Clr * KXZ + Cnr * KX2) / (4 * mub * (KX2 * KZ2 - KXZ ** 2)))]])

    B1 = np.array([[0, (V0 / b) * (CYdr / (2 * mub))],
                   [0, 0],
                   [(V0 / b) * ((Clda * KZ2 + Cnda * KXZ) / (4 * mub * (KX2 * KZ2 - KXZ ** 2))),
                    (V0 / b) * ((Cldr * KZ2 + Cndr * KXZ) / (4 * mub * (KX2 * KZ2 - KXZ ** 2)))],
                   [(V0 / b) * ((Clda * KXZ + Cnda * KX2) / (4 * mub * (KX2 * KZ2 - KXZ ** 2))),
                    (V0 / b) * ((Cldr * KXZ + Cndr * KX2) / (4 * mub * (KX2 * KZ2 - KXZ ** 2)))]])

    C1 = np.identity(4)

    D1 = np.array([[0, 0], [0, 0], [0, 0], [0, 0]])

    ########## SYMMETRIC EQUATIONS OF MOTION IN STATE-SPACE FORM ##########
    A2 = np.array([[(V0 / c) * CXu / (2 * muc), (V0 / c) * CXa / (2 * muc), (V0 / c) * CZ0 / (2 * muc),
                    (V0 / c) * CXq / (2 * muc)],
                   [(V0 / c) * CZu / (2 * muc - CZadot), (V0 / c) * CZa / (2 * muc - CZadot),
                    -(V0 / c) * CX0 / (2 * muc - CZadot), (V0 / c) * (2 * muc + CZq) / (2 * muc - CZadot)],
                   [0, 0, 0, V0 / c],
                   [(V0 / c) * (Cmu + CZu * (Cmadot / (2 * muc - CZadot))) / (2 * muc * KY2),
                    (V0 / c) * (Cma + CZa * (Cmadot / (2 * muc - CZadot))) / (2 * muc * KY2),
                    -(V0 / c) * CX0 * (Cmadot / (2 * muc - CZadot)) / (2 * muc * KY2),
                    (V0 / c) * (Cmq + Cmadot * ((2 * muc + CZq) / (2 * muc - CZadot))) / (2 * muc * KY2)]])

    B2 = np.array([[(V0 / c) * CXde / (2 * muc)],
                   [(V0 / c) * CZde / (2 * muc - CZadot)],
                   [0],
                   [(V0 / c) * (Cmde + CZde * (Cmadot / (2 * muc - CZadot))) / (2 * muc * KY2)]])

    C2 = np.identity(4)

    D2 = np.array([[0], [0], [0], [0]])

    # print(A2)
    # print(B2)
    # print(C2)
    # print(D2)
    sys1 = ml.ss(A1, B1, C1, D1)
    sys2 = ml.ss(A2, B2, C2, D2)
    e1, v = np.linalg.eig(A1)
    e2, v = np.linalg.eig(A2)

    return sys1, sys2, e1, e2


# EIGENVALUES ########## with the stationary flight conditions of short period


########## STATE SPACE MODEL ##########

# short period
sys, sys_sp_r, e1_sp_r, e2_sp_r = ABCD(1, 1)
sys, sys_sp_f, e1_sp_f, e2_sp_f = ABCD(2, 1)

# phugoid
sys, sys_ph_r, e1_ph_r, e2_ph_r = ABCD(1, 2)
sys, sys_ph_f, e1_ph_f, e2_ph_f = ABCD(2, 2)

# dutch roll
sys_dr_r, sys, e1_dr_r, e2_dr_r = ABCD(1, 3)
sys_dr_f, sys, e1_dr_f, e2_dr_f = ABCD(2, 3)

# aperiodic
sys_ap_r, sys, e1_ap_r, e2_ap_r = ABCD(1, 4)
sys_ap_f, sys, e1_ap_f, e2_ap_f = ABCD(2, 4)

# spiral
sys_spir_r, sys, e1_spir_r, e2_spir_r = ABCD(1, 5)
sys_spir_f, sys, e1_spir_f, e2_spir_f = ABCD(2, 5)

########### SIMULATION OF EIGENMOTIONS########
dt = 0.1

# Short Period
t1 = np.arange(0, 15, dt)
t_ini = 3634
t_fin = 3636

u1, cell = inputcr(reference_delta_e, time, t1, 3633, 3648)

y1_r, T1_r, x1_r = ml.lsim(sys_sp_r, u1, t1)

u1_f, celli_1 = inputcr(flight_delta_e, time, t1, 3156, 3171)

y1_f, T1_f, x1_f = ml.lsim(sys_sp_f, u1_f, t1)

# Phugoid
t2 = np.arange(0, 150, dt)

u2, cell = inputcr(reference_delta_e, time, t2, 3237, 3247)

y2_r, T2_r, x2_r = ml.lsim(sys_ph_r, u2, t2)

u2_f, celli_2 = inputcr(flight_delta_e, time, t2, 3235, 3249)

y2_f, T2_f, x2_f = ml.lsim(sys_ph_f, u2_f, t2)

# Dutch Roll
t3 = np.arange(0, 30, dt)

u3_t, cell = inputcr(reference_delta_r, time, t3, 3717, 3727)

u3 = np.hstack((np.zeros((len(t3), 1)), u3_t))

y3_r, T3_r, x3_r = ml.lsim(sys_dr_r, u3, t3)

u3_t_f, celli_3 = inputcr(flight_delta_r, time, t3, 3527, 3537)

u3_f = np.hstack((np.zeros((len(t3), 1)), u3_t_f))

y3_f, T3_f, x3_f = ml.lsim(sys_dr_f, u3_f, t3)

# Aperiodic roll
t4 = np.arange(0, 30, dt)

u4_t1_r, cell = inputcr(reference_delta_a, time, t4, 3550, 3570)

u4_t2_r, cell = inputcr(flight_delta_r, time, t4, 3550, 3570)

u4 = np.hstack((u4_t1_r, u4_t2_r))

y4_r, T4_r, x4_r = ml.lsim(sys_ap_r, u4, t4)

u4_t1_f, celli_4 = inputcr(flight_delta_a, time, t4, 3607, 3627)

u4_t2_f, celli_4 = inputcr(flight_delta_r, time, t4, 3607, 3627)

u4_f = np.hstack((u4_t1_f, u4_t2_f))

y4_f, T4_f, x4_f = ml.lsim(sys_ap_f, u4_f, t4)

# Spiral
t5 = np.arange(0, 140, dt)

u5_t1_r, cell = inputcr(reference_delta_a, time, t5, 3912, 3932)

u5_t2_r, cell = inputcr(reference_delta_r, time, t5, 3912, 3932)

u5 = np.hstack((u5_t1_r, u5_t2_r))

y5_r, T5_r, x5_r = ml.lsim(sys_spir_r, u5, t5)

u5_t1_f, celli_5 = inputcr(flight_delta_a, time, t5, 3667, 3687)

u5_t2_f, celli_5 = inputcr(flight_delta_r, time, t5, 3667, 3687)

u5_f = np.hstack((u5_t1_f, u5_t2_f))

y5_f, T5_f, x5_f = ml.lsim(sys_spir_f, u5_f, t5)

##########PLOTS OF RESPONSES###########
# Short Period
plt.style.use('seaborn-darkgrid')


fig1, (axs2, axs3, axs4, axs5) = plt.subplots(4, sharex=True)
fig1.suptitle('Short Period Response', fontsize=20, fontweight='bold')

axs2.plot(T1_f, u_1[celli_1:(celli_1+len(t1))], '--', label='Actual Response')
axs2.plot(T1_f, y1_f[:, 0], 'r', label='Flight data')


l1, = axs3.plot(T1_f, alpha_1[celli_1:(celli_1+len(t1))], '--', label='Actual Response')
l2, = axs3.plot(T1_f, y1_f[:, 1], 'r', label='Flight data')


axs4.plot(T1_f, theta_1[celli_1:(celli_1+len(t1))], '--', label='Actual Response')
axs4.plot(T1_f, y1_f[:, 2], 'r', label='Flight data')


axs5.plot(T1_f, q_1[celli_1:(celli_1+len(t1))], '--', label='Actual Response')
axs5.plot(T1_f, y1_f[:, 3], 'r', label='Flight data')


axs2.set_title('Velocity along x-axis', fontsize=16)
axs2.set_ylabel('u [-]', fontsize=16)
axs2.tick_params(axis='both', which='major', labelsize=12)


axs3.set_title('Angle of Attack', fontsize=16)
axs3.set_ylabel(' \u03B1 [-]', fontsize=16)
axs3.tick_params(axis='both', which='major', labelsize=12)


axs4.set_title('Pitch Angle', fontsize=16)
axs4.set_ylabel('\u03B8 [-]', fontsize=16)
axs4.tick_params(axis='both', which='major', labelsize=12)


axs5.set_title('Pitch Rate', fontsize=16)
axs5.set_ylabel('qc/V[-]', fontsize=16)
axs5.tick_params(axis='both', which='major', labelsize=12)


plt.xlabel('Time [s]')

legend1 = fig1.legend([l1, l2], ['Actual Response', 'Numerical Response'],
                      loc='center right', framealpha=1, frameon=True, fontsize=16)
plt.subplots_adjust(right=0.75)
fig1.align_labels()

plt.xlabel('Time [s]', fontsize=16)
frame1 = legend1.get_frame()

frame1.set_facecolor('0.90')
frame1.set_edgecolor('black')

# Errors
sp_e1 = np.transpose(u_1[celli_1:(celli_1+len(t1))]) - np.transpose(y1_f[:, 0])
sp_mean1 = np.mean(sp_e1)
sp_std1 = np.std(sp_e1)
sp_std1_mean = sp_std1/sp_mean1

sp_e2 = np.transpose(alpha_1[celli_1:(celli_1+len(t1))]) - np.transpose(y1_f[:, 1])
sp_mean2 = np.mean(sp_e2)
sp_std2 = np.std(sp_e2)
sp_std2_mean = sp_std2/sp_mean2


sp_e3 = np.transpose(theta_1[celli_1:(celli_1+len(t1))]) - np.transpose(y1_f[:, 2])
sp_mean3 = np.mean(sp_e3)
sp_std3 = np.std(sp_e3)
sp_std3_mean = sp_std2/sp_mean3


sp_e4 = np.transpose(q_1[celli_1:(celli_1+len(t1))]) - np.transpose(y1_f[:, 3])
sp_mean4 = np.mean(sp_e4)
sp_std4 = np.std(sp_e4)
sp_std4_mean = sp_std4/sp_mean4


sp_std_tot = np.sqrt(sp_std1**2 + sp_std2**2 + sp_std3**2 + sp_std4**2)
sp_std_tot_mean = np.sqrt(sp_std1_mean**2 + sp_std2_mean**2 + sp_std3_mean**2 + sp_std4_mean**2)



# Phugoid

fig2, (axs2, axs3, axs4, axs5) = plt.subplots(4, sharex=True)
fig2.suptitle('Phugoid Response', fontsize=20, fontweight='bold')
axs2.plot(T2_f, u_2[celli_2:(celli_2+len(t2))], '--', label='Actual Response')
axs2.plot(T2_f, y2_f[:, 0], 'r', label='Flight data')

l1, = axs3.plot(T2_f, alpha_2[celli_2:(celli_2+len(t2))], '--', label='Actual Response')
l2, = axs3.plot(T2_f, y2_f[:, 1], 'r', label='Flight data')

axs4.plot(T2_f, theta_2[celli_2:(celli_2+len(t2))], '--', label='Actual Response')
axs4.plot(T2_f, y2_f[:, 2], 'r', label='Flight data')

axs5.plot(T2_f, q_2[celli_2:(celli_2+len(t2))], '--', label='Actual Response')
axs5.plot(T2_f, y2_f[:, 3], 'r', label='Flight data')


axs2.set_title('Velocity along x-axis', fontsize=16)
axs2.set_ylabel('u [-]', fontsize=16)
axs2.tick_params(axis='both', which='major', labelsize=12)


axs3.set_title('Angle of Attack', fontsize=16)
axs3.set_ylabel(' \u03B1 [-]', fontsize=16)
axs3.tick_params(axis='both', which='major', labelsize=12)

axs4.set_title('Pitch Angle', fontsize=16)
axs4.set_ylabel('\u03B8 [-]', fontsize=16)
axs4.tick_params(axis='both', which='major', labelsize=12)


axs5.set_title('Pitch Rate', fontsize=16)
axs5.set_ylabel('qc/V[-]', fontsize=16)
axs5.tick_params(axis='both', which='major', labelsize=12)


plt.xlabel('Time [s]')

legend2 = fig2.legend([l1, l2], ['Actual Response', 'Numerical Response'],
                      loc='center right', framealpha=1, frameon=True, fontsize=16)
plt.subplots_adjust(right=0.75)
fig2.align_labels()

plt.xlabel('Time [s]', fontsize=14)
frame2 = legend2.get_frame()

frame2.set_facecolor('0.90')
frame2.set_edgecolor('black')

# Errors
ph_e1 = np.transpose(u_2[celli_2:(celli_2+len(t2))]) - np.transpose(y2_f[:, 0])
ph_mean1 = np.mean(ph_e1)
ph_std1 = np.std(ph_e1)
ph_std1_mean = ph_std1/ph_mean1

ph_e2 = np.transpose(alpha_2[celli_2:(celli_2+len(t2))]) - np.transpose(y2_f[:, 1])
ph_mean2 = np.mean(ph_e2)
ph_std2 = np.std(ph_e2)
ph_std2_mean = ph_std2/ph_mean2


ph_e3 = np.transpose(theta_2[celli_2:(celli_2+len(t2))]) - np.transpose(y2_f[:, 2])
ph_mean3 = np.mean(ph_e3)
ph_std3 = np.std(ph_e3)
ph_std3_mean = ph_std3/ph_mean3


ph_e4 = np.transpose(q_2[celli_2:(celli_2+len(t2))]) - np.transpose(y2_f[:, 3])
ph_mean4 = np.mean(ph_e4)
ph_std4 = np.std(ph_e4)
ph_std4_mean = ph_std4/ph_mean4


ph_std_tot = np.sqrt(ph_std1**2 + ph_std2**2 + ph_std3**2 + ph_std4**2)
ph_std_tot_mean = np.sqrt(ph_std1_mean**2 + ph_std2_mean**2 + ph_std3_mean**2 + ph_std4_mean**2)

# Dutch Roll

fig3, (axs3, axs4, axs5) = plt.subplots(3, sharex=True)
fig3.suptitle('Dutch Roll Response', fontsize=20, fontweight='bold')
l1, = axs3.plot(T3_f, phi[celli_3:(celli_3+len(t3))], '--', label='Actual Response')
l2, = axs3.plot(T3_f, y3_f[:, 1], 'r', label='Flight data')

axs4.plot(T3_f, p_3[celli_3:(celli_3+len(t3))], '--', label='Reference data')
axs4.plot(T3_f, y3_f[:, 2], 'r', label='Flight data')

axs5.plot(T3_f, r_3[celli_3:(celli_3+len(t3))], '--', label='Reference data')
axs5.plot(T3_f, y3_f[:, 3], 'r', label='Flight data')


axs3.set_title('Roll Angle', fontsize=16)
axs3.set_ylabel('\u03C6 [-]', fontsize=16)
axs3.tick_params(axis='both', which='major', labelsize=12)


axs4.set_title('Roll Rate', fontsize=16)
axs4.set_ylabel(' pb/V[-]', fontsize=16)
axs4.tick_params(axis='both', which='major', labelsize=12)


axs5.set_title('Yaw Rate', fontsize=16)
axs5.set_ylabel('rb/V[-]', fontsize=16)
axs5.tick_params(axis='both', which='major', labelsize=12)


legend3 = fig3.legend([l1, l2], ['Actual Response', 'Numerical Response'],
                      loc='center right', framealpha=1, frameon=True, fontsize=16)
plt.subplots_adjust(right=0.75)
fig3.align_labels()

plt.xlabel('Time [s]', fontsize=16)
frame3 = legend3.get_frame()

frame3.set_facecolor('0.90')
frame3.set_edgecolor('black')

dr_e1 = np.transpose(phi[celli_3:(celli_3+len(t3))]) - np.transpose(y3_f[:, 1])
dr_mean1 = np.mean(dr_e1)
dr_std1 = np.std(dr_e1)
dr_std1_mean = dr_std1/dr_mean1

dr_e2 = np.transpose(p_3[celli_3:(celli_3+len(t3))]) - np.transpose(y3_f[:, 2])
dr_mean2 = np.mean(dr_e2)
dr_std2 = np.std(dr_e2)
dr_std2_mean = dr_std2/dr_mean2


dr_e3 = np.transpose(r_3[celli_3:(celli_3+len(t3))]) - np.transpose(y3_f[:, 3])
dr_mean3 = np.mean(dr_e3)
dr_std3 = np.std(dr_e3)
dr_std3_mean = dr_std3/dr_mean3

dr_std_tot = np.sqrt(dr_std1**2 + dr_std2**2 + dr_std3**2)
dr_std_tot_mean = np.sqrt(dr_std1_mean**2 + dr_std2_mean**2 + dr_std3_mean**2)


# Aperiodic Roll


fig4, (axs3, axs4, axs5) = plt.subplots(3, sharex=True)
fig4.suptitle('Aperiodic Roll Response', fontsize=20, fontweight='bold')
l1, = axs3.plot(T4_f, phi[celli_4:(celli_4+len(t4))], '--', label='Actual Response')
l2, = axs3.plot(T4_f, y4_f[:, 1], 'r', label='Flight data')

axs4.plot(T4_f, p_4[celli_4:(celli_4+len(t4))], '--', label='Reference data')
axs4.plot(T4_f, y4_f[:, 2], 'r', label='Flight data')

axs5.plot(T4_f, r_4[celli_4:(celli_4+len(t4))], '--', label='Reference data')
axs5.plot(T4_f, y4_f[:, 3], 'r', label='Flight data')


axs3.set_title('Roll Angle', fontsize=16)
axs3.set_ylabel('\u03C6 [-]', fontsize=16)
axs3.tick_params(axis='both', which='major', labelsize=12)


axs4.set_title('Roll Rate', fontsize=16)
axs4.set_ylabel(' pb/V[-]', fontsize=16)
axs4.tick_params(axis='both', which='major', labelsize=12)


axs5.set_title('Yaw Rate', fontsize=16)
axs5.set_ylabel('rb/V[-]', fontsize=16)
axs5.tick_params(axis='both', which='major', labelsize=12)


legend4 = fig4.legend([l1, l2], ['Actual Response', 'Numerical Response'],
                      loc='center right', framealpha=1, frameon=True, fontsize=16)
plt.subplots_adjust(right=0.75)
fig4.align_labels()

plt.xlabel('Time [s]', fontsize=16)
frame4 = legend4.get_frame()

frame4.set_facecolor('0.90')
frame4.set_edgecolor('black')


ar_e1 = np.transpose(phi[celli_4:(celli_4+len(t4))]) - np.transpose(y4_f[:, 1])
ar_mean1 = np.mean(ar_e1)
ar_std1 = np.std(ar_e1)
ar_std1_mean = ar_std1/ar_mean1 

ar_e2 = np.transpose(p_4[celli_4:(celli_4+len(t4))]) - np.transpose(y4_f[:, 2])
ar_mean2 = np.mean(ar_e2)
ar_std2 = np.std(ar_e2)
ar_std2_mean = ar_std2/ar_mean2

ar_e3 = np.transpose(r_4[celli_4:(celli_4+len(t4))]) - np.transpose(y4_f[:, 3])
ar_mean3 = np.mean(ar_e3)
ar_std3 = np.std(ar_e3)
ar_std3_mean = ar_std3/ar_mean3


ar_std_tot = np.sqrt(ar_std1**2 + ar_std2**2 + ar_std3**2)
ar_std_tot_mean = np.sqrt(ar_std1_mean**2 + ar_std2_mean**2 + ar_std3_mean**2)


# spiral

fig5, (axs3, axs4, axs5) = plt.subplots(3, sharex=True)
fig5.suptitle('Spiral Dive Response', fontsize=16, fontweight='bold')

l1, = axs3.plot(T5_f, phi[celli_5:(celli_5+len(t5))], '--', label='Actual Response')
l2, = axs3.plot(T5_f, y5_f[:, 1], 'r', label='Flight data')

axs4.plot(T5_f, p_5[celli_5:(celli_5+len(t5))], '--', label='Reference data')
axs4.plot(T5_f, y5_f[:, 2], 'r', label='Flight data')

axs5.plot(T5_f, r_5[celli_5:(celli_5+len(t5))], '--', label='Reference data')
axs5.plot(T5_f, y5_f[:, 3], 'r', label='Flight data')


axs3.set_title('Roll Angle', fontsize=16)
axs3.set_ylabel('\u03C6 [-]', fontsize=16)
axs3.tick_params(axis='both', which='major', labelsize=12)


axs4.set_title('Roll Rate', fontsize=16)
axs4.set_ylabel(' pb/V[-]', fontsize=16)
axs4.tick_params(axis='both', which='major', labelsize=12)


axs5.set_title('Yaw Rate', fontsize=16)
axs5.set_ylabel('rb/V[-]', fontsize=16)
axs4.tick_params(axis='both', which='major', labelsize=12)


legend5 = fig5.legend([l1, l2], ['Actual Response', 'Numerical Response'],
                      loc='center right', framealpha=1, frameon=True, fontsize=16)
plt.subplots_adjust(right=0.75)
fig5.align_labels()

plt.xlabel('Time [s]', fontsize=16)
frame5 = legend5.get_frame()

frame5.set_facecolor('0.90')
frame5.set_edgecolor('black')


spiral_e1 = np.transpose(phi[celli_5:(celli_5+len(t5))]) - np.transpose(y5_f[:, 1])
spiral_mean1 = np.mean(spiral_e1)
spiral_std1 = np.std(spiral_e1)
spiral_std1_mean = spiral_std1/spiral_mean1



spiral_e2 = np.transpose(p_5[celli_5:(celli_5+len(t5))]) - np.transpose(y5_f[:, 2])
spiral_mean2 = np.mean(spiral_e2)
spiral_std2 = np.std(spiral_e2)
spiral_std2_mean = spiral_std2/spiral_mean2


spiral_e3 = np.transpose(r_5[celli_5:(celli_5+len(t5))]) - np.transpose(y5_f[:, 3])
spiral_mean3 = np.mean(spiral_e3)
spiral_std3 = np.std(spiral_e3)
spiral_std3_mean = spiral_std3/spiral_mean3


spiral_std_tot = np.sqrt(spiral_std1**2 + spiral_std2**2 + spiral_std3**2)
spiral_std_tot_mean = np.sqrt(spiral_std1_mean**2 + spiral_std2_mean**2 + spiral_std3_mean**2)



###### Print Commands ##########

plt.show()

#print(e1, v2)

#print(e2, v2)
