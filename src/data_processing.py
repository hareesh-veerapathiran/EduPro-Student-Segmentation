import pandas as pd


# Load data from Excel file
def load_data():

    file_path = "data/EduProOnlinePlatform.xlsx"

    # Read sheet names automatically
    excel_file = pd.ExcelFile(file_path, engine="openpyxl")
    print("Available sheets:", excel_file.sheet_names)

    # CHANGE these names if your sheet names differ
    users = pd.read_excel(
        file_path,
        sheet_name="Users",
        engine="openpyxl"
    )

    courses = pd.read_excel(
        file_path,
        sheet_name="Courses",
        engine="openpyxl"
    )

    transactions = pd.read_excel(
        file_path,
        sheet_name="Transactions",
        engine="openpyxl"
    )

    # Merge all data
    df = transactions.merge(courses, on="CourseID")
    df = df.merge(users, on="UserID")

    return df, users


# Create learner profiles
def create_learner_profiles():

    df, users = load_data()

    # Map course level to numeric
    level_map = {
        "Beginner": 1,
        "Intermediate": 2,
        "Advanced": 3
    }

    df["level_num"] = df["CourseLevel"].map(level_map)

    # Aggregate learner features
    profile = df.groupby("UserID").agg(

        total_courses=("CourseID", "count"),
        avg_rating=("CourseRating", "mean"),
        total_spent=("Amount", "sum"),
        diversity_score=("CourseCategory", "nunique"),
        avg_level=("level_num", "mean")

    ).reset_index()

    # Find preferred category
    preferred = df.groupby(
        ["UserID", "CourseCategory"]
    ).size().reset_index(name="count")

    preferred = preferred.loc[
        preferred.groupby("UserID")["count"].idxmax()
    ]

    profile = profile.merge(
        preferred[["UserID", "CourseCategory"]],
        on="UserID"
    )

    # Merge demographics
    profile = profile.merge(users, on="UserID")

    # Rename column
    profile.rename(
        columns={"CourseCategory": "preferred_category"},
        inplace=True
    )

    # Save output
    profile.to_csv(
        "outputs/learner_profiles.csv",
        index=False
    )

    print("Learner profiles created successfully!")


# Run script
if __name__ == "__main__":
    create_learner_profiles()