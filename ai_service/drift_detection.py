
from river import drift
from sklearn.linear_model import SGDClassifier
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split

# Load dataset
data = load_digits()
X_train, X_test, y_train, y_test = train_test_split(data.data, data.target, test_size=0.2, random_state=42)

# Initialize model and drift detector
model = SGDClassifier()
drift_detector = drift.ADWIN()

# Fit the model with initial data
model.partial_fit(X_train, y_train, classes=np.unique(y_train))

# Monitor model performance and detect drift
for X_batch, y_batch in [(X_test[:10], y_test[:10]), (X_test[10:20], y_test[10:20])]:
    predictions = model.predict(X_batch)
    for pred, truth in zip(predictions, y_batch):
        drift_detector.update(pred != truth)
        if drift_detector.detected_change():
            print("Model drift detected! Retraining is required.")
            # Trigger retraining process here
