import pandas as pd


def generate_recommendations():

    profiles = pd.read_csv(
        "outputs/learner_profiles.csv"
    )

    courses = pd.read_csv(
        "data/courses.csv"
    )

    transactions = pd.read_csv(
        "data/transactions.csv"
    )

    df = transactions.merge(
        courses,
        on="CourseID"
    )

    recommendations = []

    for cluster in profiles["cluster"].unique():

        users = profiles[
            profiles.cluster == cluster
        ].UserID

        cluster_df = df[
            df.UserID.isin(users)
        ]

        top_courses = cluster_df.groupby(
            "CourseID"
        ).agg(

            avg_rating=("CourseRating","mean"),
            enrollments=("CourseID","count")

        ).sort_values(
            ["avg_rating","enrollments"],
            ascending=False
        ).head(5).reset_index()

        top_courses["cluster"] = cluster

        recommendations.append(top_courses)

    rec_df = pd.concat(recommendations)

    rec_df.to_csv(
        "outputs/recommendations.csv",
        index=False
    )

    print("Recommendations generated")


if __name__ == "__main__":
    generate_recommendations()