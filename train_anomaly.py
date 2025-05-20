from sklearn.ensemble import IsolationForest
import joblib

# Sample normal data for feature extraction (this should be actual, clean request data)
normal_data = [
    # Example of extracted features for normal requests
    [2, 1, 5, 10, 0, 0],  # Adjust based on collected feature data
    [1, 2, 20, 30, 0, 0],
    # More data here...
]

# Train Isolation Forest
model = IsolationForest(contamination=0.01)
model.fit(normal_data)


# Save the model
joblib.dump(model, 'anomaly_detector.joblib')
print("Model trained and saved.")