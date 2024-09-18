# Z-Score Algorithm for Anomaly Detection

## Overview

The Z-score algorithm is a simple and efficient method for detecting anomalies in data streams. It uses statistical properties like the mean and standard deviation within a fixed-size sliding window to determine how far a data point deviates from the norm. Points with high deviations, based on a predefined threshold, are flagged as anomalies.

## How It Works

1. **Sliding Window:** A fixed-size window of recent data points is maintained (e.g., 50 points).
2. **Z-Score Calculation:** The Z-score is calculated for each new point:
   \[
   Z = \frac{(X - \mu)}{\sigma}
   \]
   - \( X \): Current data point.
   - \( \mu \): Mean of the data in the window.
   - \( \sigma \): Standard deviation of the data in the window.
3. **Anomaly Detection:** If the absolute value of the Z-score exceeds a specified threshold (e.g., 3), the point is flagged as an anomaly.

## Speed and Efficiency

### Efficiency

- **Space Complexity:** \( O(n) \), where \( n \) is the window size.
- **Time Complexity:** \( O(n) \) per point, primarily for computing the mean and standard deviation.

### Real-Time Detection

- **Quick Response:** The algorithm processes each point as it arrives, making it effective for real-time applications.
- **Low Overhead:** Constant memory and computation requirements make it well-suited for continuous data streams.

### Effectiveness

- The Z-score method is highly effective at detecting sudden, large deviations in data (e.g., spikes).
- By adjusting the window size and threshold, it can balance sensitivity and stability, making it adaptable to various anomaly detection tasks.
