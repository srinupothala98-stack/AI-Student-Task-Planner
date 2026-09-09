import streamlit as st

from agent import (
    create_local_plan,
    evaluate_plan,
    save_plan,
    load_history
)


# =================================================
# PAGE CONFIGURATION
# =================================================

st.set_page_config(
    page_title="AI Student Task Planner",
    page_icon="📚",
    layout="wide"
)


# =================================================
# SESSION STATE
# =================================================

if "plan" not in st.session_state:
    st.session_state.plan = None


# =================================================
# HEADER
# =================================================

st.title("📚 AI Student Task Planner")

st.caption(
    "Create a personalized study schedule with important topics, "
    "priorities, progress tracking and plan evaluation."
)


# =================================================
# SIDEBAR
# =================================================

st.sidebar.header("🎓 Student Information")


goal = st.sidebar.text_area(
    "Study Goal",
    "Prepare for my semester examinations."
)


subjects = st.sidebar.text_area(
    "Subjects",
    "Python, DBMS, Java",
    help="Enter subjects separated by commas."
)


st.sidebar.markdown("### ⭐ Important Topics")

st.sidebar.caption(
    "Enter important topics for each subject. "
    "Use one subject per line."
)


important_topics = st.sidebar.text_area(
    "Important Topics",
    """Python: Variables and Data Types, Functions, OOP, Exception Handling
DBMS: SQL, Joins, Normalization, Transactions
Java: OOP, Inheritance, Interfaces, Collections""",
    height=150
)


days = st.sidebar.number_input(
    "Number of Days",
    min_value=1,
    max_value=60,
    value=7,
    step=1
)


hours = st.sidebar.number_input(
    "Study Hours Per Day",
    min_value=1,
    max_value=12,
    value=3,
    step=1
)


# =================================================
# GENERATE PLAN
# =================================================

if st.sidebar.button(
    "🚀 Generate Study Plan",
    use_container_width=True
):

    if not goal.strip():

        st.sidebar.error(
            "Please enter a study goal."
        )

    elif not subjects.strip():

        st.sidebar.error(
            "Please enter at least one subject."
        )

    else:

        with st.spinner(
            "🤖 Planning your personalized study plan..."
        ):

            plan = create_local_plan(
                goal=goal,
                subjects=subjects,
                days=days,
                hours_per_day=hours,
                important_topics=important_topics
            )

            valid, evaluation = evaluate_plan(plan)

            plan["evaluation"] = evaluation

            st.session_state.plan = plan

            save_plan(plan)

        st.success(
            "✅ Study plan generated successfully!"
        )


# =================================================
# MAIN DASHBOARD
# =================================================

if st.session_state.plan:

    plan = st.session_state.plan

    st.divider()

    st.header("📊 Study Plan Overview")


    # -------------------------------------------------
    # SUMMARY METRICS
    # -------------------------------------------------

    total_tasks = sum(
        len(day["tasks"])
        for day in plan["plan"]
    )


    completed_tasks = sum(
        1
        for day in plan["plan"]
        for task in day["tasks"]
        if task.get("completed", False)
    )


    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.metric(
            "🎯 Goal",
            "Exam Preparation"
        )


    with col2:

        st.metric(
            "📅 Days",
            plan["days"]
        )


    with col3:

        st.metric(
            "⏰ Hours / Day",
            plan["hours_per_day"]
        )


    with col4:

        st.metric(
            "📝 Total Tasks",
            total_tasks
        )


    # =================================================
    # IMPORTANT TOPICS
    # =================================================

    st.subheader("⭐ Important Topics")


    if plan.get("important_topics"):

        for subject, topics in plan["important_topics"].items():

            st.markdown(
                f"**📘 {subject.title()}**"
            )

            st.write(
                " • ".join(topics)
            )

    else:

        st.info(
            "No custom important topics were provided."
        )


    # =================================================
    # DAILY PLAN
    # =================================================

    st.subheader("📅 Personalized Daily Plan")


    for day in plan["plan"]:

        with st.expander(
            f"📌 Day {day['day']}",
            expanded=(day["day"] == 1)
        ):

            for task_index, task in enumerate(
                day["tasks"]
            ):

                st.markdown(
                    f"### 📚 {task['subject']}"
                )

                col1, col2, col3 = st.columns(
                    [2, 4, 1]
                )


                with col1:

                    st.markdown(
                        "**Important Topic**"
                    )

                    st.write(
                        task["topic"]
                    )


                with col2:

                    st.markdown(
                        "**Task**"
                    )

                    st.write(
                        task["task"]
                    )


                with col3:

                    st.markdown(
                        "**Priority**"
                    )

                    priority = task["priority"]


                    if priority == "High":

                        st.error(
                            "🔴 High"
                        )

                    elif priority == "Medium":

                        st.warning(
                            "🟡 Medium"
                        )

                    else:

                        st.info(
                            "🟢 Low"
                        )


                st.write(
                    f"⏱️ **{task['hours']} hour**"
                )


                completed = st.checkbox(
                    "✅ Mark task as completed",
                    value=task.get(
                        "completed",
                        False
                    ),
                    key=(
                        f"day_{day['day']}"
                        f"_task_{task_index}"
                    )
                )


                task["completed"] = completed


                st.divider()


    # =================================================
    # PROGRESS
    # =================================================

    st.subheader("📈 Your Progress")


    completed_tasks = sum(
        1
        for day in plan["plan"]
        for task in day["tasks"]
        if task.get("completed", False)
    )


    if total_tasks > 0:

        progress = (
            completed_tasks / total_tasks
        )

        st.progress(progress)

        percentage = int(
            progress * 100
        )

        st.write(
            f"### {percentage}% Complete"
        )

        st.write(
            f"Completed **{completed_tasks} "
            f"/ {total_tasks} tasks**"
        )


        if percentage == 100:

            st.success(
                "🎉 Excellent! You completed "
                "your entire study plan!"
            )

        elif percentage >= 75:

            st.success(
                "🔥 Great progress! Keep going!"
            )

        elif percentage >= 50:

            st.info(
                "💪 You are halfway there!"
            )

        else:

            st.warning(
                "📖 Keep studying consistently!"
            )


    # =================================================
    # PLAN EVALUATION
    # =================================================

    st.subheader("🔍 Plan Evaluation")


    valid, evaluation = evaluate_plan(
        plan
    )


    if valid:

        st.success(
            "✅ All days are within the available "
            "study-time limit."
        )

    else:

        st.warning(
            "⚠️ Some days exceed the available "
            "study time."
        )


    for result in evaluation:

        if result["status"] == "OK":

            st.write(
                f"Day {result['day']}: "
                f"{result['hours']} hours — "
                f"✅ {result['status']}"
            )

        else:

            st.write(
                f"Day {result['day']}: "
                f"{result['hours']} hours — "
                f"⚠️ {result['status']}"
            )


    # =================================================
    # STUDY RECOMMENDATIONS
    # =================================================

    st.subheader("🎯 Study Recommendations")


    recommendations = [
        "Complete high-priority topics first.",
        "Practice questions after learning each concept.",
        "Revise important topics regularly.",
        "Use previous exam questions for practice.",
        "Take short breaks between study sessions.",
        "Keep the final study days mainly for revision."
    ]


    for recommendation in recommendations:

        st.write(
            f"• {recommendation}"
        )


    # =================================================
    # MOTIVATION
    # =================================================

    st.info(
        "💡 Stay consistent. Small progress every day "
        "leads to strong exam preparation."
    )


# =================================================
# PLAN MEMORY / HISTORY
# =================================================

st.divider()

st.subheader("🧠 Plan Memory")


history = load_history()


if history:

    st.write(
        f"Previous plans stored: "
        f"**{len(history)}**"
    )


    for index, old_plan in enumerate(
        reversed(history[-5:])
    ):

        created_at = old_plan.get(
            "created_at",
            "Unknown date"
        )

        old_days = old_plan.get(
            "days",
            0
        )


        st.write(
            f"📋 Plan {index + 1}: "
            f"{created_at} — "
            f"{old_days} days"
        )


else:

    st.write(
        "No previous plans saved yet."
    )