import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

# Initialize the figure and axes
fig, (ax_main, ax_emi, ax_ert) = plt.subplots(3, 1, figsize=(10, 8), gridspec_kw={'height_ratios': [3, 1, 1]})

# Setting up the main plot (rubble, human body, drone)
ax_main.set_xlim(0, 10)
ax_main.set_ylim(0, 10)
ax_main.set_title('Drone Detection System')
ax_main.set_xlabel('X-Position')
ax_main.set_ylabel('Altitude')
ax_main.plot([4], [0], 'yo', markersize=12, label='Human Body')  # Human body
ax_main.plot([2, 6], [0, 0], 'ks', markersize=20, alpha=0.5, label='Rubble')  # Rubble

drone, = ax_main.plot([], [], 'bo-', markersize=10, label='Drone')
ert_probe_1, = ax_main.plot([], [], 'ro', markersize=6, label='ERT Probe 1')
ert_probe_2, = ax_main.plot([], [], 'ro', markersize=6, label='ERT Probe 2')

# Initialize EMI plot
ax_emi.set_xlim(0, 10)
ax_emi.set_ylim(0, 1)
ax_emi.set_title('EMI Anomaly Detection')
ax_emi.set_ylabel('EMI Signal')
emi_signal_line, = ax_emi.plot([], [], 'g-', label='EMI Signal')

# Initialize ERT plot
ax_ert.set_xlim(0, 10)
ax_ert.set_ylim(0, 10)
ax_ert.set_title('ERT Detection')
ax_ert.set_xlabel('X-Position')
ax_ert.set_ylabel('ERT Signal')
ert_signal_line, = ax_ert.plot([], [], 'r-', label='ERT Signal')

# Adding the legends
ax_main.legend(loc='upper left')
ax_emi.legend(loc='upper left')
ax_ert.legend(loc='upper left')

# Data for the EMI and ERT signals
x_data = np.linspace(0, 10, 100)
emi_signal = np.exp(-((x_data - 4) ** 2) / 0.5)  # Simulating an EMI anomaly near x=4
ert_signal = np.exp(-((x_data - 4) ** 2) / 0.2) * 10  # Simulating a stronger ERT signal near x=4

# Define the update function for animation
def update(frame):
    x_drone = frame
    y_drone = 8 if frame < 5 else 2  # Drone descends after detecting the EMI anomaly

    # Update drone position
    drone.set_data([x_drone], [y_drone])

    # Update EMI signal
    emi_signal_line.set_data(x_data[:int(frame * 10)], emi_signal[:int(frame * 10)])

    # Deploy ERT probes when EMI anomaly is detected and drone descends
    if frame >= 5:
        ert_probe_1.set_data([4], [0])
        ert_probe_2.set_data([4.2], [0])
        ert_signal_line.set_data(x_data[:int(frame * 10)], ert_signal[:int(frame * 10)])
    else:
        ert_probe_1.set_data([np.nan], [np.nan])
        ert_probe_2.set_data([np.nan], [np.nan])
        ert_signal_line.set_data([np.nan], [np.nan])

    return drone, emi_signal_line, ert_probe_1, ert_probe_2, ert_signal_line

# Create animation
ani = animation.FuncAnimation(fig, update, frames=np.linspace(0, 10, 100), blit=True)

ani.save('drone_detection_system.mp4', writer='ffmpeg', fps=5)


# Show animation
plt.tight_layout()
plt.show()
