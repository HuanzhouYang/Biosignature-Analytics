import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Define function for calculations
def plot_signals(alpha=0.3, tau2=0.2, tau3=0.2, r_values=(0.2, 0.4, 0.6, 0.8), width=1000, height=70):
    z = np.linspace(1, 100, 100)
    k3 = z.copy()
    cdf3 = z.copy()
    pdf3 = z.copy()

    # Calculate pdf3 and cdf3, ensuring pdf3 is non-negative
    for i in range(100):
        pdf3[i] = max(1 - (i - height)**2 / width, 0)
        cdf3[i] = np.sum(pdf3[:i + 1])

    # Normalize cdf3 so that it reaches tau3 at the top
    cdf3 = cdf3 / cdf3[-1] * tau3

    # Calculate k3
    for i in range(100):
        k3[i] = cdf3[i] / z[i]

    # Plot pdf3 vs z
    plt.figure(figsize=(12, 8))
    plt.subplot(2, 1, 1)
    plt.plot(pdf3, z, label='pdf3 vs z', color='b')
    plt.xlabel("Ozone Concentration PDF")
    plt.ylabel("Non-dimensional Geometric Height")
    plt.title("PDF of Ozone Concentration")
    plt.grid(True)
    plt.legend()

    # Plot k3 vs z
    plt.subplot(2, 1, 2)

    # Loop over different r values
    for r in r_values:
        z = np.linspace(0, 100, 100)
        k2 = tau2 / 100

        # Calculate sig_clear and sig_cloud
        sig_clear = alpha * np.exp(-tau2) * (1 - np.exp(-tau3))
        sig_cloud = (
            r * np.exp(-(tau2 - k2 * z)) * (1 - np.exp(-(tau3 - k3 * z)))
            + (1 - r)**2 * alpha * np.exp(-tau2)
            * (1 / (1 - alpha * r * np.exp(-k2 * z)) - np.exp(-tau3) / (1 - alpha * r * np.exp(-(k3 + k2) * z)))
        )

        # Plot sig_cloud vs z
        plt.plot(sig_cloud / sig_clear - 1, z, label=f'r = {r}')

    # Add labels and title
    plt.axvline(0, color='k', linestyle='--')
    plt.title('Non-dimensional Parameter Test')
    plt.xlabel('Signal Relative Difference')
    plt.ylabel('Scaled z')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


# Add Streamlit sliders for user interaction
alpha = st.slider('Alpha', 0.1, 1.0, 0.3, step=0.05)
tau2 = st.slider('Tau2', 0.05, 1.0, 0.2, step=0.05)
tau3 = st.slider('Tau3', 0.05, 1.0, 0.2, step=0.05)
width = st.slider('Width', 1, 1000, 1000)
height = st.slider('Height', 0, 100, 70)
r_values = st.multiselect('r values', [0.2, 0.4, 0.6, 0.8], default=[0.2, 0.4, 0.6, 0.8])

# Plot with given parameters
plot_signals(alpha, tau2, tau3, r_values, width, height)

