import json
import os
from datetime import datetime


# -------------------------------------------------
# CREATE LOCAL STUDY PLAN
# -------------------------------------------------

def create_local_plan(goal, subjects, days, hours_per_day, important_topics=""):
    """
    Creates a personalized study plan locally.
    No API key is required.
    """

    subject_list = [
        subject.strip()
        for subject in subjects.split(",")
        if subject.strip()
    ]

    # Parse important topics
    topics_by_subject = {}

    if important_topics.strip():

        lines = important_topics.splitlines()

        for line in lines:

            if ":" in line:

                subject, topics = line.split(":", 1)

                subject = subject.strip()
                topics = topics.strip()

                topic_list = [
                    topic.strip()
                    for topic in topics.split(",")
                    if topic.strip()
                ]

                topics_by_subject[subject.lower()] = topic_list

    # Default topics if user does not provide them
    default_topics = {
        "python": [
            "Variables and Data Types",
            "Control Flow",
            "Functions",
            "Lists and Dictionaries",
            "Object-Oriented Programming",
            "Exception Handling",
            "File Handling"
        ],

        "dbms": [
            "ER Model",
            "Relational Model",
            "SQL",
            "Joins",
            "Normalization",
            "Transactions",
            "Indexing"
        ],

        "java": [
            "Variables and Data Types",
            "Control Statements",
            "Classes and Objects",
            "Inheritance",
            "Polymorphism",
            "Exception Handling",
            "Collections"
        ],

        "c": [
            "Variables and Data Types",
            "Functions",
            "Arrays",
            "Pointers",
            "Structures",
            "File Handling"
        ],

        "c++": [
            "Classes and Objects",
            "Inheritance",
            "Polymorphism",
            "Templates",
            "STL",
            "Exception Handling"
        ]
    }

    # Build topic list for every subject
    subject_topics = {}

    for subject in subject_list:

        key = subject.lower()

        if key in topics_by_subject:
            subject_topics[subject] = topics_by_subject[key]

        elif key in default_topics:
            subject_topics[subject] = default_topics[key]

        else:
            subject_topics[subject] = [
                "Important Concepts",
                "Core Topics",
                "Practice Questions",
                "Revision",
                "Previous Questions"
            ]

    plan = []

    total_subjects = len(subject_list)

    # Create tasks for each day
    for day_number in range(1, days + 1):

        daily_tasks = []

        # Number of subjects that can normally fit in one day
        subjects_per_day = min(
            total_subjects,
            max(1, hours_per_day)
        )

        # Rotate subjects between days
        for i in range(subjects_per_day):

            subject_index = (
                (day_number - 1) * subjects_per_day + i
            ) % total_subjects

            subject = subject_list[subject_index]

            topics = subject_topics[subject]

            topic_index = (
                day_number - 1 + i
            ) % len(topics)

            topic = topics[topic_index]

            # Determine task type
            if day_number <= max(2, days // 3):

                task_type = (
                    f"Study and understand {topic}"
                )

                priority = "High"

            elif day_number <= max(3, (days * 2) // 3):

                task_type = (
                    f"Practice questions on {topic}"
                )

                priority = "High"

            else:

                task_type = (
                    f"Revise {topic} and solve exam questions"
                )

                priority = "Medium"

            task = {
                "subject": subject,
                "topic": topic,
                "task": task_type,
                "priority": priority,
                "hours": 1,
                "completed": False
            }

            daily_tasks.append(task)

        plan.append({
            "day": day_number,
            "tasks": daily_tasks
        })

    return {
        "goal": goal,
        "subjects": subject_list,
        "days": days,
        "hours_per_day": hours_per_day,
        "important_topics": topics_by_subject,
        "plan": plan,
        "created_at": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    }


# -------------------------------------------------
# EVALUATE PLAN
# -------------------------------------------------

def evaluate_plan(plan):

    evaluation = []

    valid = True

    for day in plan["plan"]:

        total_hours = sum(
            task["hours"]
            for task in day["tasks"]
        )

        if total_hours <= plan["hours_per_day"]:

            status = "OK"

        else:

            status = "Exceeds available time"
            valid = False

        evaluation.append({
            "day": day["day"],
            "hours": total_hours,
            "status": status
        })

    return valid, evaluation


# -------------------------------------------------
# SAVE PLAN
# -------------------------------------------------

def save_plan(plan):

    history_file = "plan_history.json"

    history = []

    if os.path.exists(history_file):

        try:

            with open(
                history_file,
                "r",
                encoding="utf-8"
            ) as file:

                history = json.load(file)

        except (json.JSONDecodeError, OSError):

            history = []

    history.append(plan)

    # Keep only the latest 20 plans
    history = history[-20:]

    with open(
        history_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            history,
            file,
            indent=4
        )


# -------------------------------------------------
# LOAD HISTORY
# -------------------------------------------------

def load_history():

    history_file = "plan_history.json"

    if not os.path.exists(history_file):
        return []

    try:

        with open(
            history_file,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except (json.JSONDecodeError, OSError):

        return []