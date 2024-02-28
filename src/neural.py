import json
import tensorflow as tf
from sklearn.model_selection import StratifiedKFold
import numpy as np
from embedding import sentence_embedding

def create_cnn(vector_size):
    model = tf.keras.Sequential([
        # Start with Conv1D or Dense layer, adjusted for input shape
        tf.keras.layers.Conv1D(filters=128, kernel_size=5, activation='relu', input_shape=(vector_size, 1)),
        tf.keras.layers.GlobalMaxPooling1D(),
        tf.keras.layers.Dense(10, activation='relu'),
        tf.keras.layers.Dense(2, activation='softmax')
    ])

    metrics = ["accuracy", tf.keras.metrics.Precision(), tf.keras.metrics.Recall(), tf.keras.metrics.F1Score(average='micro', threshold=0.5, name='f1_score'), tf.keras.metrics.AUC()]

    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=metrics)
    return model

def create_multiple_cnn(vector_size):
    model = tf.keras.Sequential([
        tf.keras.layers.Conv1D(filters=64, kernel_size=3, activation='relu', input_shape=(266, vector_size)),
        tf.keras.layers.Conv1D(filters=32, kernel_size=3, activation='relu'),
        tf.keras.layers.MaxPooling1D(pool_size=3),
        tf.keras.layers.Conv1D(filters=16, kernel_size=3, activation='relu'),
        tf.keras.layers.Conv1D(filters=8, kernel_size=3, activation='relu'),
        tf.keras.layers.GlobalAveragePooling1D(),
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])

    metrics = ["accuracy", tf.keras.metrics.Precision(), tf.keras.metrics.Recall(), tf.keras.metrics.F1Score(average='micro', threshold=0.5, name='f1_score'), tf.keras.metrics.AUC()]

    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=metrics)
    return model

def create_lstm(vector_size):
    model = tf.keras.Sequential([
        tf.keras.layers.LSTM(200, input_shape=(266, vector_size), return_sequences=False),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])
    
    metrics = ["accuracy", tf.keras.metrics.Precision(), tf.keras.metrics.Recall(), tf.keras.metrics.F1Score(average='micro', threshold=0.5, name='f1_score'), tf.keras.metrics.AUC()]

    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=metrics)
    return model

def train_cnn(model, name, X_train, y_train, number, epochs=5, batch_size=32):
    y_train_numerical = np.array(y_train).astype('float32')

    k = 5
    kf = StratifiedKFold(n_splits=k, shuffle=True, random_state=42)

    metrics_per_epoch = {'accuracy': [], 'precision': [], 'recall': [], 'f1_score': [], 'auc': []}

    fold = 1
    for train_index, test_index in kf.split(X_train, y_train):
        X_train_fold, X_val_fold = X_train[train_index], X_train[test_index]
        y_train_fold, y_val_fold = y_train_numerical[train_index], y_train_numerical[test_index]


        print(f'Training for fold {fold}')
        history = model.fit(X_train_fold, y_train_fold, epochs=epochs, batch_size=batch_size, validation_data=(X_val_fold, y_val_fold))

        metrics_with_epoch = ['precision', 'recall', 'auc']

        for metric in metrics_per_epoch.keys():
            if metric in metrics_with_epoch:
                metric_name = f'val_{metric}' if number == 1 else f'val_{metric}_{number-1}'
            else:
                metric_name = f'val_{metric}'

            for key in history.history.keys():
                if key.startswith(metric_name):
                    metrics_per_epoch[metric].append(history.history[key][-1])
                    break

        fold += 1

    avg_metrics = {metric: np.mean(values) for metric, values in metrics_per_epoch.items()}
    model.save(f"./Models/CNN/{name}")
    return {'name': name, 'metrics': avg_metrics}



def train_lstm(model, name, X_train, y_train, number, epochs=5, batch_size=32):
    y_train_numerical = np.array(y_train).astype('float32')
    print(y_train_numerical)
    k = 5
    kf = StratifiedKFold(n_splits=k, shuffle=True, random_state=42)

    metrics_per_epoch = {'accuracy': [], 'precision': [], 'recall': [], 'f1_score': [], 'auc': []}

    fold = 1
    for train_index, test_index in kf.split(X_train, y_train):
        X_train_fold, X_val_fold = X_train[train_index], X_train[test_index]
        y_train_fold, y_val_fold = y_train_numerical[train_index], y_train_numerical[test_index]

        print(f'Training for fold {fold}')


        history = model.fit(X_train_fold, y_train_fold, epochs=epochs, batch_size=batch_size, validation_data=(X_val_fold, y_val_fold))
        
        metrics_with_epoch = ['precision', 'recall', 'auc']

        for metric in metrics_per_epoch.keys():
            if metric in metrics_with_epoch:
                metric_name = f'val_{metric}' if number == 1 else f'val_{metric}_{number-1}'
            else:
                metric_name = f'val_{metric}'

            for key in history.history.keys():
                if key.startswith(metric_name):
                    metrics_per_epoch[metric].append(history.history[key][-1])
                    break

        fold += 1
    
    avg_metrics = {metric: np.mean(values) for metric, values in metrics_per_epoch.items()}
    model.save(f"./Models/LSTM/{name}")
    return {'name': name, 'metrics': avg_metrics}

def sentiment_num(sentiment):
    if sentiment == "Negative":
        return 0
    else:
        return 1

def predict_sentiment(model, input_data):
    true_label = ["Negative", "Positive"]
    
    # Ensure the input_data is in the correct shape for the LSTM model
    # The expected shape is (1, 266, 150) for a single prediction
    if input_data.ndim == 2:  # If the input_data is just (266, 150)
        input_data = np.expand_dims(input_data, axis=0)  # Reshape it to (1, 266, 150)
    
    score = model.predict(input_data)
    print(score)
    
    # Since the output layer uses sigmoid activation, interpret the score directly
    predicted_label_index = int(score >= 0.5)  # Convert boolean to int directly without using argmax
    predicted_label = true_label[predicted_label_index]
    return predicted_label


if __name__ == "__main__":
    print("In neural network")