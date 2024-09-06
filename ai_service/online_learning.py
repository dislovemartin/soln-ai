
from sklearn.linear_model import SGDClassifier
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split

# Load dataset
data = load_digits()
X_train, X_test, y_train, y_test = train_test_split(data.data, data.target, test_size=0.2, random_state=42)

# Initialize online learning model
model = SGDClassifier()

# Fit the model with initial data
model.partial_fit(X_train, y_train, classes=np.unique(y_train))

# Simulate incoming data stream for online updates
incoming_data_stream = [(X_train[:10], y_train[:10]), (X_train[10:20], y_train[10:20])]  # Example batches

for X_batch, y_batch in incoming_data_stream:
    model.partial_fit(X_batch, y_batch)  # Incremental updates with new data

# Test the model
accuracy = model.score(X_test, y_test)
print(f"Model Accuracy after online learning: {accuracy}")
