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

"""def detect_anomalies(data_stream, window_size=100, threshold=3):
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
        yield point, abs(z_score) > threshold"""
def detect_anomalies(data_stream, window_size=100, threshold=3):
    data_window = deque(maxlen=window_size)  # Sliding window

    def mad(data):
        """Calculate the Median Absolute Deviation (MAD) as a robust alternative to standard deviation."""
        median = np.median(data)
        return np.median(np.abs(data - median))
    
    # Initialize is_anomaly to False at the start
    is_anomaly = False
    
    for point in data_stream:
        data_window.append(point)
        
        # Only start calculating anomalies when the window is full
        if len(data_window) == window_size:
            mean = np.mean(data_window)
            std = np.std(data_window)
            mad_value = mad(data_window)
            
            # Choose the more robust measure (MAD or standard deviation) if std is too small
            if std > 0:
                z_score = (point - mean) / std
            else:
                z_score = 0
            
            # Adjust threshold dynamically based on MAD
            dynamic_threshold = threshold + (mad_value / std) if std > 0 else threshold
            
            # Detect anomaly based on z_score threshold
            is_anomaly = abs(z_score) > dynamic_threshold
            
            if is_anomaly:
                print(f"Anomaly detected: {point}, z-score: {z_score}, threshold: {dynamic_threshold}")
        
        # Yield the point and the anomaly flag (True or False)
        yield point, is_anomaly


# Step 6: Visualization of Data Stream and Anomalies

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

# Step 7: Simulate Data and Run the Detection with Visualization
data_stream = data_stream_simulation(size=400)  # Simulate 200 data points
anomalous_data_stream = detect_anomalies(data_stream)
visualize_stream(anomalous_data_stream)


