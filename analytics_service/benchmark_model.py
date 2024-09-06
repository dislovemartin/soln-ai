
import psycopg2
from datetime import datetime

# Function to store model performance metrics in PostgreSQL
def store_performance_metrics(model_name, accuracy, precision, recall, f1_score):
    conn = psycopg2.connect(
        dbname="your_db_name", user="your_username", password="your_password", host="localhost"
    )
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO model_performance (model_name, accuracy, precision, recall, f1_score, timestamp)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (model_name, accuracy, precision, recall, f1_score, datetime.now()))
    
    conn.commit()
    cursor.close()
    conn.close()

# Function to benchmark the new model against the last model stored in the database
def benchmark_model(new_model_metrics):
    conn = psycopg2.connect(
        dbname="your_db_name", user="your_username", password="your_password", host="localhost"
    )
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT accuracy, precision, recall, f1_score
        FROM model_performance
        ORDER BY timestamp DESC LIMIT 1
    """ )
    last_model = cursor.fetchone()
    
    conn.commit()
    cursor.close()
    conn.close()

    # Compare accuracy (or other metrics) to determine if the new model is better
    if new_model_metrics['accuracy'] > last_model[0]:
        return True
    return False

# Example usage:
new_model_metrics = {"accuracy": 0.96, "precision": 0.93, "recall": 0.92, "f1_score": 0.94}
if benchmark_model(new_model_metrics):
    print("New model outperforms the last model. Ready for deployment.")
    store_performance_metrics("model_v3", new_model_metrics['accuracy'], new_model_metrics['precision'],
                              new_model_metrics['recall'], new_model_metrics['f1_score'])
else:
    print("New model underperforms. Deployment rejected.")
