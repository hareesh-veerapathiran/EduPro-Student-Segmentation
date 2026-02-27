import streamlit as st
import pandas as pd
import plotly.express as px


profiles = pd.read_csv(
    "outputs/learner_profiles.csv"
)

recommendations = pd.read_csv(
    "outputs/recommendations.csv"
)

st.title("EduPro Personalization Dashboard")


user = st.selectbox(
    "Select User",
    profiles.UserID
)


user_data = profiles[
    profiles.UserID == user
]


cluster = int(user_data.cluster.values[0])


st.subheader("Learner Profile")

st.write(user_data)


st.subheader("Cluster")

st.write(cluster)


st.subheader("Recommended Courses")

rec = recommendations[
    recommendations.cluster == cluster
]

st.dataframe(rec)


st.subheader("Cluster Visualization")

fig = px.scatter(

    profiles,
    x="total_courses",
    y="total_spent",
    color="cluster"

)

st.plotly_chart(fig)