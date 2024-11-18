import numpy as np
import matplotlib.pyplot as plt

def generate_swaying_data(duration=120, frequency=0.3, damping=0.03, sampling_rate=100):
    """
    Generates swaying data to mimic the movement of a payload after rocket separation.
    
    Parameters:
    - duration (float): Total duration of the data in seconds.
    - frequency (float): Base frequency of the oscillation in Hz.
    - damping (float): Damping coefficient (higher values dampen faster).
    - sampling_rate (int): Number of samples per second.
    
    Returns:
    - data (list of tuples): List of (radian, time) pairs.
    """
    # Generate time points
    times = np.linspace(0, duration, int(sampling_rate * duration))
    
    # Generate damped sinusoidal oscillation
    amplitude = np.exp(-damping * times)   # Damping envelope
    sway_angles = 0.5 * amplitude * np.sin(2 * np.pi * frequency * times)  # Oscillation in radians
    
    
    return sway_angles, times

time,radian = generate_swaying_data()

plt.figure(figsize=(10, 5))
plt.plot(radian, time, color="blue", label="Sway Angle")
plt.xlabel("Time (s)")
plt.ylabel("Angle (rad)")
plt.title("Simulated Payload Swaying Data")
plt.grid()
plt.legend()
plt.show()