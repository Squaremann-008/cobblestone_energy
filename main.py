import numpy as np
import time
from collections import deque
import matplotlib.pyplot as plt

# Function to simulate a data stream
def data_stream_simulation(size=1000, noise_level=0.1, anomaly_chance=0.01, delay=0.1):
    """
    Simulates a data stream with sinusoidal pattern, random noise, and occasional anomalies.

    :param size: Number of data points to simulate
    :param noise_level: Standard deviation of the random noise
    :param anomaly_chance: Probability of generating an anomaly at each point
    :param delay: Delay in seconds between generating each data point
    :return: Generator yielding the simulated data points
    """
    if size <= 0:
        raise ValueError("Size must be a positive integer")
    if not (0 <= anomaly_chance <= 1):
        raise ValueError("Anomaly chance must be between 0 and 1")

    for i in range(size):
        seasonal_pattern = np.sin(i / 50) * 10
        noise = np.random.normal(0, noise_level)
        if np.random.rand() < anomaly_chance:
            yield seasonal_pattern + noise + 50  # Large spike as anomaly
        else:
            yield seasonal_pattern + noise
        if delay > 0:
            time.sleep(delay)  # Simulate real-time delay


#Function to detect anomalies
def detect_anomalies(data_stream, window_size=50, threshold=3):
    """
    Detects anomalies in a data stream using Z-score method.

    :param data_stream: Generator yielding data points
    :param window_size: Number of data points to use in the sliding window
    :param threshold: Z-score threshold to consider a point as an anomaly
    :return: Generator yielding data points and anomaly flags (True if anomaly)
    """
    if window_size <= 0:
        raise ValueError("Window size must be a positive integer")
    if threshold <= 0:
        raise ValueError("Threshold must be a positive number")

    data_window = deque(maxlen=window_size)  # Sliding window
    z_score = 0  # Initialize z_score at the beginning
    
    for point in data_stream:
        data_window.append(point)
        
        # Only start calculating anomalies when the window is full
        if len(data_window) == window_size:
            mean = np.mean(data_window)
            std = np.std(data_window)
            
            # Safely calculate z_score only if std > 0
            if std > 0:
                z_score = (point - mean) / std
            else:
                z_score = 0  # If std is zero, there's no variation
            
            # Detect anomaly based on z_score threshold
            if abs(z_score) > threshold:
                print(f"Anomaly detected: {point}")
        
        # Yield the point and the anomaly flag (True or False)
        yield point, abs(z_score) > threshold

# Visualization of Data Stream and Anomalies

def visualize_stream(data_stream):
    plt.ion()  # Turn on interactive mode
    fig, ax = plt.subplots()
    x_data, y_data = [], []
    anomaly_markers = []

    line, = ax.plot([], [], label="Data Stream")
    scatter = ax.scatter([], [], color='r', label="Anomaly")

    for idx, (point, is_anomaly) in enumerate(data_stream):
        x_data.append(idx)
        y_data.append(point)
        
        # Update the data stream line
        line.set_data(x_data, y_data)
        ax.relim()  # Adjust limits to fit the new data
        ax.autoscale_view()

        # Update the anomalies
        if is_anomaly:
            anomaly_markers.append((idx, point))
            scatter.set_offsets(anomaly_markers)

        ax.legend()
        plt.pause(0.01)

#Simulate Data and Run the Detection with Visualization
data_stream = data_stream_simulation(size=400)  # Simulate 200 data points
anomalous_data_stream = detect_anomalies(data_stream)
visualize_stream(anomalous_data_stream)


