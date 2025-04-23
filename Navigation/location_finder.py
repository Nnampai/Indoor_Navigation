import pandas as pd
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.neighbors import KNeighborsClassifier
import random
import config

def load_csv_data():
    return pd.read_csv(config.CSV_FILENAME)

def evaluate_knn_model(k=1, test_frac=0.3):
    data = load_csv_data()
    x = data[['RSSI1', 'RSSI2', 'RSSI3']]
    y = data['location']

    random_state = random.randint(0, 99999)
    print(f"Random_state = {random_state}")

    # Random test set (fraction per class)
    test_df = data.groupby('location', group_keys=False).sample(frac=test_frac, random_state=random_state) # 92853
    train_df = data.drop(test_df.index)

    # Split feature and label
    x_train = train_df[['RSSI1', 'RSSI2', 'RSSI3']]
    y_train = train_df['location']
    x_test = test_df[['RSSI1', 'RSSI2', 'RSSI3']]
    y_test = test_df['location']

    # Train and predict
    model = KNeighborsClassifier(n_neighbors=k)
    model.fit(x_train, y_train)
    y_predict = model.predict(x_test)

    # Accuracy & Confusion matrix
    acc = accuracy_score(y_test, y_predict)
    cm = confusion_matrix(y_test, y_predict, labels=sorted(data['location'].unique()))

    return acc, cm

def find_location(rssi1, rssi2, rssi3, k=1):
    data = load_csv_data()

    # Prepare data
    X = data[['RSSI1', 'RSSI2', 'RSSI3']] # feature
    y = data['location']                  # label

    # Create and train KNN model
    knn = KNeighborsClassifier(n_neighbors=k)
    knn.fit(X, y)

    predicted_location = knn.predict([[rssi1, rssi2, rssi3]])[0]

    return predicted_location

def find_best_k():
    for i in range(1,21):
        acc, cm = evaluate_knn_model(k=i, test_frac=0.3)
        print(f"K = {i}, KNN Accuracy: {acc}")

if __name__ == "__main__":
    #acc_knn, cm_knn = evaluate_knn_model(k=1, test_size=0.3)
    acc_knn, cm_knn = evaluate_knn_model(k=1, test_frac=0.3)
    print("KNN Accuracy:", acc_knn)
    labels = sorted(load_csv_data()['location'].unique())
    cm_knn = pd.DataFrame(cm_knn, index=[f"Actual: {label}" for label in labels], columns=[label for label in labels])
    print("KNN Confusion Matrix: \n                       Predict\n", cm_knn)
    # find_best_k()