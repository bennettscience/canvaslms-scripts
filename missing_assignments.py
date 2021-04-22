from config import PROD_URL, PROD_KEY
from canvasapi import Canvas
import csv
import concurrent.futures
import re
from functools import partial


canvas = Canvas(PROD_URL, PROD_KEY)
course = canvas.get_course(000000)  # set your course ID
assignments = len(list(course.get_assignments()))
writer = csv.writer(open("your_report.csv", "w"))

# Set a conditional filter on assignments returend.
filter_results = True

"""
Create a CSV report of missing assignments for all users in a course.
"""


def main():
    sections = course.get_sections()

    writer.writerow(
        ["Name", "Email", "Building", "Last Activity", "# Missing", "Missing"]
    )

    for section in sections:
        enrollments = section.get_enrollments(state="active", type="StudentEnrollment")

        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:

            data = []
            job = partial(process_user, section=section)

            results = [executor.submit(job, enrollment) for enrollment in enrollments]

            for f in concurrent.futures.as_completed(results):
                data.append(f.result())
                print(f"Processed {len(data)} in {len(list(enrollments))} at {section}")

        writer.writerows(data)


def process_user(enrollment, section):
    """Handle getting assignments for a single user

    Args:
        enrollment (canvasapi.enrollment.Enrollment): Canvas <Enrollment> object
        section (canvasapi.section.Section): Canvas <Section> object

    Returns:
        [list]: formatted list for writing to the CSV
    """
    missing = get_user_missing(section, enrollment.user["id"])

    login = course.get_user(enrollment.user["id"]).login_id

    regex = re.compile("@")

    if regex.search(login) is None:
        email = f"{login}@elkhart.k12.in.us"
    else:
        email = login

    return [
        enrollment.user["sortable_name"],
        email,
        section.name,
        enrollment.last_activity_at,
        len(missing),
        ", ".join(missing),
    ]


def get_user_missing(section, user_id):
    """Get the missing assignments for the user in a section

    Args:
        section (canvasapi.section.Section): Canvas <Section> object
        user_id (int): user ID to request assignments for

    Returns:
        [type]: [description]
    """
    submissions = section.get_multiple_submissions(
        student_ids=[user_id],
        include=["assignment", "submission_history"],
        workflow_state="unsubmitted",
    )

    if filter_results:
        filtered = filter(submissions)

        missing_list = [
            item.assignment["name"]
            for item in filtered
            if item.workflow_state == "unsubmitted" and item.excused is not True
        ]
    else:
        missing_list = [
            item.assignment["name"]
            for item in submissions
            if item.workflow_state == "unsubmitted" and item.excused is not True
        ]

    return missing_list


def filter(submissions):
    """Filter submission in the assignment list based on a criteria.
        As written, this looks at the assignment title
    Args:
        submissions (list): List of Canvas assignments

    Returns:
        [list]
    """
    # Filter based on any criteria.
    allowed = ["Criteria 1", "Criteria 2"]

    # Check for the criteria in the assignment name.
    # You can filter based on any key in the assignment object
    filtered = [
        item
        for item in submissions
        if any(word in item.assignment["name"] for word in allowed)
    ]
    return filtered


if __name__ == "__main__":
    main()
