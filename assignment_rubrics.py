from typing import List, Dict, Union
from canvasapi import Canvas
from config import PROD_KEY, PROD_URL
from pprint import pprint

# This is a script to grab and analyze assignment rubrics and assignment scores. 

def build_assignment_rubric_results(canvas: Canvas, course_id: int, assignment_id: int) -> List[Dict]:
    """ Look up rubric results for a specific Canvas assignment

    :param canvas: <Canvas> instance
    :param course_id: Valid Canvas course ID
    :param assignment_id: Valid Canvas assignment ID

    :return: Named dictionary of outcomes and rubric results for an assignment
    :rtype: dict of list of ints
    """
    course = canvas.get_course(course_id)
    assignment = course.get_assignment(assignment_id)

    rubric = assignment.rubric

    # build a list to use as headers in the view
    columns = []

    for criteria in rubric:
        if "outcome_id" in criteria:

            column = {}
            column["id"] = criteria["id"]
            column["name"] = criteria["description"]
            column["outcome_id"] = criteria["outcome_id"]
            columns.append(column)

    # Create a list to store all results
    student_results = get_assignment_scores(canvas, assignment)

    return {"columns": columns, "student_results": student_results}

def get_assignment_scores(canvas, assignment):
    """ Request assignment scores from Canvas

    :param assignment: <Assignment> instance
    :type assignment: Class

    :return: A list of student dicts with results for the assigment
    :rtype: list of dict
    """
    student_results = []

    # Get submissions for the assignment to get rubric evaluation
    submissions = assignment.get_submissions(include=("rubric_assessment", "user"))

    for submission in list(submissions):

        student_result = {}
        student_result["id"] = submission.user_id
        student_result["name"] = submission.user["sortable_name"]
        student_result["score"] = submission.score
        if hasattr(submission, "rubric_assessment"):
            student_result["rubric"] = submission.rubric_assessment
        student_results.append(student_result)

    student_results = sorted(student_results, key=lambda x: x["name"].split(" "))

    return student_results

def main():
    canvas = Canvas(PROD_URL, PROD_KEY)

    data = build_assignment_rubric_results(canvas, 36756, 176135)

    pprint(data)

if __name__ == "__main__":
    main()