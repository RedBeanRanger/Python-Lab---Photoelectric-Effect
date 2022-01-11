# -*- coding: utf-8 -*-
"""
Created on Mon Nov  1 15:30:56 2021

@author: angel
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.constants import c

# Exercise 1, Graph V_stop with the frequency of light to determine
# Planck's constant
# Work function
# Cutoff frequency

wavelength, w_err, vStop = np.loadtxt(r"C:\Users\angel\Desktop\Docs\PHY244\PhotoelectricEffect\PhotoelectricExercise1.csv", 
                                      unpack = True, skiprows = 1, delimiter = ",")

"""
print(wavelength)
print(w_err)
print(vStop)
"""
electron_charge = 1.602*10**-19

err = np.ones(len(wavelength))
err = err*.001 # error in precision
print("The largest relative error in V_stop is: ", max(err/vStop))
print("The largest absolute error in V_Stop is: ", max(err))

w_err_percentage = w_err/wavelength # the relative error in wavelength

wavelength = wavelength * (10**-9) # Convert wavelength from nanometers into meters
frequency = c/wavelength # obtain frequency from wavelength. 
                         # Frequency of light = speed of light/wavelength
f_err = w_err_percentage*frequency # uncertainty in frequency

print("The largest relative error in frequency is: ", max(w_err_percentage))
print("The largest absolute error in frequency is: ", max(f_err))

plt.errorbar(frequency, vStop, yerr = err, xerr = f_err, ls = "none", marker = "o", label = "Raw Data")
plt.ylabel("Stopping voltage (V)")
plt.xlabel("Frequency (Hertz)")
plt.legend()


model_curve = []
def v_stop_model_function(frequency, planck_constant, fCutoff):
    #return v_stop given frequency, planck's constant, and frequency cutoff
    return (planck_constant/electron_charge) * (frequency - fCutoff)

popt, pcov = curve_fit(v_stop_model_function, xdata = frequency, ydata = vStop,
                       p0 = [6.62*10**-34, 5.8*10**14])
#popt, pcov = curve_fit(v_stop_model_function, xdata = frequency, ydata = vStop)
# p0 is estimates of planck's constant and work function to help with the curve
# I am using the work function of iron (4.5 eV) for my reference cutoff frequency
print("Planck's constant according to curve fit is:", popt[0])
print("Cutoff frequency according to curve fit is:", popt[1])

for i in range(0, len(frequency)):
    model_curve.append(v_stop_model_function(frequency[i], popt[0], popt[1]))

#print(model_curve)

# Reduced chi squared calculation
def redChiSquared(measured_data, predicted_data, err):
    # returns chiSquared value
    # takes in arrays of measured_data, predicted_data, and err
    # assume the arrays have the same length
    sum = 0
    for x in range(0, len(measured_data)):
        #sum += ((10**(measured_data[x]) - 10**(predicted_data[x])) / 10**(err[x]))**2
        sum += (((measured_data[x]) - (predicted_data[x])) / (err[x]))**2
    return sum/(len(measured_data) - 2)

print("The reduced chi squared value using error in stopping voltage is: ",
      redChiSquared(vStop, model_curve, err))

print("The reduced chi squared value using error in frequency is: ",
      redChiSquared(vStop, model_curve, f_err))
    
plt.title("V_Stop Over Frequency")
plt.errorbar(frequency, model_curve, label = "Curve Fit")
plt.legend()

plt.show()

    