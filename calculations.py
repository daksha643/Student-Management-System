def get_grade(marks):

    if marks >= 90:

        return "A+"

    elif marks >= 80:

        return "A"

    elif marks >= 70:

        return "B+"

    elif marks >= 60:

        return "B"

    elif marks >= 50:

        return "C"

    elif marks >= 40:

        return "D"

    else:

        return "F"

 

 

def get_grade_point(marks):

    if marks >= 90:

        return 10

    elif marks >= 80:

        return 9

    elif marks >= 70:

        return 8

    elif marks >= 60:

        return 7

    elif marks >= 50:

        return 6

    elif marks >= 40:

        return 5

    else:

        return 0

 

 

def calculate_sgpa(subjects):

    if not subjects:

        return 0

 

    total_points = 0

    total_credits = 0

 

    for subject in subjects:

        marks = subject[2]

        credits = subject[3]

 

        grade_point = get_grade_point(marks)

 

        total_points += grade_point * credits

        total_credits += credits

 

    if total_credits == 0:

        return 0

 

    return round(total_points / total_credits, 2)