import streamlit as st
import pandas as pd

# Dataset 
@st.cache_data
def load_data():
    return pd.read_csv("scentelligence_mini_db.csv", encoding='latin1')
df = load_data()
st.write("🧠 CSV Columns:", df.columns.tolist())

st.set_page_config(page_title="Scentelligence - Personalized Fragrance Recommender", layout="centered")
st.title("🧠 Scentelligence")
st.subheader("Your personalized scent advisor")
st.markdown("Answer a few quick questions and get 3 fragrance recommendations tailored to your body, mood, and style.")

# Questionnaire
with st.form("quiz_form"):
    st.markdown("### 1. What's your skin type?")
    skin_type = st.radio("", ["Oily", "Dry", "Combination", "Normal"])

    st.markdown("### 2. How warm does your skin usually feel?")
    skin_temp = st.radio("", ["Cool", "Neutral", "Warm"])

    st.markdown("### 3. How active are you during the day?")
    activity = st.radio("", ["Low", "Moderate", "High"])

    st.markdown("### 4. What's your personality vibe?")
    personality = st.radio("", ["Bold", "Classic", "Creative", "Reserved"])

    st.markdown("### 5. What mood should your scent evoke?")
    mood = st.radio("", ["Confident", "Romantic", "Fresh", "Grounded", "Inviting"])

    st.markdown("### 6. Where do you plan to wear this scent?")
    use_case = st.radio("", ["Everyday", "Date Night", "Office", "Special Event", "Club/Party"])

    st.markdown("### 7. Which season should it perform best in?")
    season = st.radio("", ["All Year", "Summer", "Winter", "Spring", "Fall"])

    st.markdown("### 8. How long should it last?")
    longevity = st.radio("", ["4-6 hours", "6-10 hours", "All day (12h+)"])

    submitted = st.form_submit_button("🔍 Get My Recommendations")

# Matching Logic
if submitted:
    st.markdown("---")
    st.header("🎯 Your Personalized Scent Matches")

    filtered = df.copy()

    if skin_type == "Oily":
        filtered = filtered[~filtered["Base Notes"].str.contains("vanilla|tonka", case=False, na=False)]

    if activity == "High":
        filtered = filtered[filtered["Longevity"].str.contains("Long", na=False)]

    if use_case == "Date Night":
        filtered = filtered[filtered["Use Case"].str.contains("Date", na=False)]
    elif use_case == "Office":
        filtered = filtered[filtered["Use Case"].str.contains("Work|Office", na=False)]

    if season != "All Year":
        filtered = filtered[filtered["Seasonality"].str.contains(season, na=False)]

    if mood != "Fresh":
        filtered = filtered[filtered["Mood"].str.contains(mood, na=False)]

    top_matches = filtered.sample(n=min(3, len(filtered))) if len(filtered) > 0 else pd.DataFrame()

    if not top_matches.empty:
        for i, row in top_matches.iterrows():
            st.subheader(f"{row['Name']} by {row['Brand']}")
            st.markdown(f"**Top Notes**: {row['Top Notes']}  ")
            st.markdown(f"**Heart Notes**: {row['Heart Notes']}  ")
            st.markdown(f"**Base Notes**: {row['Base Notes']}  ")
            st.markdown(f"**Longevity**: {row['Longevity']} | **Mood**: {row['Mood']} | **Season**: {row['Seasonality']}")
            st.markdown(f"[View Product]({row['Product URL']})")
            st.markdown("---")
    else:
        st.warning("Sorry, we couldn’t find a perfect match based on your inputs. Try adjusting a few answers.")
