import numpy as np
import time
from collections import deque
import matplotlib.pyplot as plt

# Function to simulate a data stream
def data_stream_simulation(size=1000, noise_level=0.1, anomaly_chance=0.01):
    for i in range(size):
        # Simulate seasonality (sinusoidal pattern)
        seasonal_pattern = np.sin(i / 50) * 10
        # Add random noise
        noise = np.random.normal(0, noise_level)
        # Simulate anomaly with a small chance
        if np.random.rand() < anomaly_chance:
            yield seasonal_pattern + noise + 50  # large spike as anomaly
        else:
            yield seasonal_pattern + noise
        time.sleep(0.1)  # simulating real-time delay

def detect_anomalies(data_stream, window_size=100, threshold=3):
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


# Step 6: Visualization of Data Stream and Anomalies
def visualize_stream(data_stream):
    plt.ion()  # Turn on interactive mode
    fig, ax = plt.subplots()
    x_data, y_data = [], []
    anomaly_markers = []
    
    for idx, (point, is_anomaly) in enumerate(data_stream):
        x_data.append(idx)
        y_data.append(point)
        ax.clear()
        ax.plot(x_data, y_data, label="Data Stream")
        if is_anomaly:
            anomaly_markers.append((idx, point))
            ax.scatter(*zip(*anomaly_markers), color='r', label="Anomaly")
        ax.legend()
        plt.pause(0.01)

# Step 7: Simulate Data and Run the Detection with Visualization
data_stream = data_stream_simulation(size=200)  # Simulate 200 data points
anomalous_data_stream = detect_anomalies(data_stream)
visualize_stream(anomalous_data_stream)