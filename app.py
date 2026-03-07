import os
os.environ["LLM_PROVIDER"] = "real"
import streamlit as st
from src.main import run_pipeline
import pandas as pd

st.title("AI Scheduling Constraint Solver")

st.write(
    "Describe your scheduling problem in natural language."
)

user_input = st.text_area(
    "Scheduling Problem",
    height=200
)
st.markdown("### Example problems")

st.code("""
We have 4 workers.
There are 3 shifts: morning, evening, night.
Each shift needs 1 worker.
""")

st.code("""
We have 2 workers.
There are 3 shifts: morning, evening, night.
Each shift needs 1 worker.
""")

if st.button("Solve Scheduling Problem"):
  with st.spinner("Solving scheduling problem..."):
    result = run_pipeline(user_input)
    if result is None:
        st.error("Could not parse your input. Please try again with more detail.")
        st.stop()

    if result.get("needs_clarification"):
        st.warning("🤖 Clarification Needed:")
        st.write(result["clarification_question"])
        st.stop()

    st.subheader("Feasibility")

    if result["feasible"]:
        st.success("Schedule is feasible")
    else:
        st.error("Scheduling problem is infeasible")

    if result["feasible"]:

        st.subheader("Generated Schedule")

        schedule = result["schedule"]

        rows = []
        for shift, workers in schedule.items():
            for w in workers:
                rows.append({"Shift": shift.capitalize(), "Worker": w})

        df = pd.DataFrame(rows)

        st.table(df)

    else:

        st.subheader("Conflict Explanation")

        st.write(result["conflict"])

    st.subheader("Constraint Explanation")

    st.write(result["explanation"])
    st.subheader("Utilization")

    st.write(result["utilization"])