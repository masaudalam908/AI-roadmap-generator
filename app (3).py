import os
import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI Roadmap Generator", page_icon="🎓")
st.title("🎓 AI Learning Roadmap Generator")

api_key = os.environ.get("GROQ_API_KEY")
if not api_key:
    st.error("GROQ_API_KEY is not set. Add it as an environment variable and restart the app.")
    st.stop()

client = Groq(api_key=api_key)

topic = st.text_input("What do you want to learn?", placeholder="e.g. Machine Learning")
level = st.selectbox("Your current level", ["Beginner", "Intermediate", "Advanced"])
weeks = st.number_input("Time available (weeks)", min_value=1, max_value=104, value=8)
hours = st.slider("Hours per week", 1, 40, 8)
file = st.file_uploader(
    "Optional: upload a .txt file (syllabus, resume, notes)", type=["txt"]
)

if st.button("Generate Roadmap"):
    if not topic.strip():
        st.warning("Please enter a topic.")
    else:
        extra = ""
        if file:
            extra = "\n\nUser's uploaded context:\n" + file.read().decode(
                "utf-8", errors="ignore"
            )[:4000]

        prompt = f"""Create a detailed learning roadmap for: {topic}
Skill level: {level}
Total time: {weeks} weeks, {hours} hours/week.{extra}

Format in Markdown:
1. A short overview and the goal
2. Week-by-week plan (topics, tasks, hands-on practice)
3. Recommended free resources (courses, books, docs)
4. 2-3 portfolio projects
5. Final checklist to confirm mastery"""

        with st.spinner("Building your roadmap..."):
            try:
                resp = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are an expert learning-path designer.",
                        },
                        {"role": "user", "content": prompt},
                    ],
                    temperature=0.5,
                )
                roadmap = resp.choices[0].message.content
                st.markdown(roadmap)
                st.download_button(
                    "Download roadmap", roadmap, file_name="roadmap.md"
                )
            except Exception as e:
                st.error(f"Something went wrong: {e}")
