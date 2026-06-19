from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet


styles = getSampleStyleSheet()


def generate_class_report(results, filename):

    doc = SimpleDocTemplate(
        filename,
        pagesize=A4
    )

    story = []

    title = Paragraph(
        "<b>Student Performance Analytics Report</b>",
        styles["Title"]
    )

    story.append(title)
    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            f"<b>Total Students:</b> {results['total_students']}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Class Average:</b> {results['class_average']}%",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Passed:</b> {results['pass_count']}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Failed:</b> {results['fail_count']}",
            styles["Normal"]
        )
    )

    story.append(Spacer(1, 25))

    story.append(
        Paragraph(
            "<b>Top Performer</b>",
            styles["Heading2"]
        )
    )

    topper = results["topper"]

    story.append(
        Paragraph(
            f"Name: {topper['name']}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"Roll Number: {topper['roll_number']}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"Percentage: {topper['percentage']}%",
            styles["Normal"]
        )
    )

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            "<b>Top 5 Students</b>",
            styles["Heading2"]
        )
    )

    for student in results["top5"]:

        story.append(
            Paragraph(
                f"#{student['rank']} - "
                f"{student['name']} "
                f"({student['percentage']}%)",
                styles["Normal"]
            )
        )

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            "<b>Subject Averages</b>",
            styles["Heading2"]
        )
    )

    for subject, avg in results["subject_averages"].items():

        story.append(
            Paragraph(
                f"{subject}: {avg}",
                styles["Normal"]
            )
        )

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            "<b>Students Requiring Attention</b>",
            styles["Heading2"]
        )
    )

    for student in results["students"]:

        if not student["pass"]:

            story.append(
                Paragraph(
                    f"{student['name']} "
                    f"({student['percentage']}%)",
                    styles["Normal"]
                )
            )

    doc.build(story)


def generate_student_report(student, filename):

    doc = SimpleDocTemplate(
        filename,
        pagesize=A4
    )

    story = []

    story.append(
        Paragraph(
            "<b>Student Performance Report</b>",
            styles["Title"]
        )
    )

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            f"<b>Name:</b> {student['name']}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Roll Number:</b> {student['roll_number']}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Percentage:</b> {student['percentage']}%",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Grade:</b> {student['grade']}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Status:</b> {'PASS' if student['pass'] else 'FAIL'}",
            styles["Normal"]
        )
    )

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            "<b>Subject Wise Marks</b>",
            styles["Heading2"]
        )
    )

    ignore = [
        "name",
        "roll_number",
        "total",
        "percentage",
        "pass",
        "grade"
    ]

    for key, value in student.items():

        if key not in ignore:

            story.append(
                Paragraph(
                    f"{key}: {value}",
                    styles["Normal"]
                )
            )

    doc.build(story)