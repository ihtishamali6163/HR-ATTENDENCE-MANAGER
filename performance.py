def evaluate_performance(attendance_percentage):

    if attendance_percentage >= 90:
        return {"rating": "Excellent", "remark": "Outstanding attendance."}

    elif attendance_percentage >= 80:
        return {"rating": "Good", "remark": "Consistent attendance."}

    elif attendance_percentage >= 60:
        return {"rating": "Needs Improvement", "remark": "Attendance should improve."}

    else:
        return {"rating": "Poor", "remark": "Attendance is below expectations."}
