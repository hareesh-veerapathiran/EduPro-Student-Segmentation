import pandas as pd
import pickle

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans


def train_cluster():

    df = pd.read_csv("outputs/learner_profiles.csv")

    # Remove non-numeric columns except UserID
    numeric_df = df.select_dtypes(include=["int64", "float64"])

    # Keep UserID separately
    user_ids = df["UserID"]

    # Scale features
    scaler = StandardScaler()
    scaled = scaler.fit_transform(numeric_df.drop("UserID", axis=1, errors="ignore"))

    # Train model
    kmeans = KMeans(
        n_clusters=4,
        random_state=42,
        n_init=10
    )

    clusters = kmeans.fit_predict(scaled)

    # Add cluster column
    df["cluster"] = clusters

    # Save updated profiles
    df.to_csv(
        "outputs/learner_profiles.csv",
        index=False
    )

    # Save model
    pickle.dump(
        kmeans,
        open("models/kmeans.pkl", "wb")
    )

    pickle.dump(
        scaler,
        open("models/scaler.pkl", "wb")
    )

    print("Clustering complete")


if __name__ == "__main__":
    train_cluster()