import numpy as np 
from scipy.integrate import odeint 
import matplotlib.pyplot as plt 

# SIR model equations 
def SIR_model(y, t, beta, gamma): 
    S, I, R = y 
    dSdt = -beta * S * I 
    dIdt = beta * S * I - gamma * I 
    dRdt = gamma * I 
    return [dSdt, dIdt, dRdt]

# Initial conditions 
S0 = 0.99  # 99% of the population is susceptible at the start
I0 = 0.01  # 1% of the population is infected at the start
R0 = 0.00  # 0% of the population is recovered at the start
y0 = [S0, I0, R0]

# Parameters
beta = 0.3  # Transmission rate
gamma = 0.1  # Recovery rate

# Time vector
t = np.linspace(0, 200, 200)  # Simulate for 200 days

# Solve the SIR model equations using odeint()
solution = odeint(SIR_model, y0, t, args=(beta, gamma))

# Extract results
S, I, R = solution.T

# Plot the results
plt.figure(figsize=(10, 6))
plt.plot(t, S, label='Susceptible')
plt.plot(t, I, label='Infected')
plt.plot(t, R, label='Recovered')
plt.xlabel('Time (days)')
plt.ylabel('Proportion of Population')
plt.title('SIR Model Simulation')
plt.legend()
plt.grid(True)
plt.show()
