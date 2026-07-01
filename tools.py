"""
tools.py

LangChain tools for the HR Attendance and Performance Bot.
Each tool wraps a database query or business logic function.
"""
from performance import evaluate_performance
from langchain.tools import tool

from queries import (
    get_employee,
    get_monthly_attendance,
    get_yearly_attendance,
    count_absents,
    count_lates,
    attendance_percentage,
)


def resolve_employee(employee_name: str):
    """
    Looks up an employee by full or partial name.

    Returns:
        ("not_found", None)            -> no matching employee in the database
        ("ambiguous", [rows...])       -> more than one employee matches
        ("found", row)                 -> exactly one employee matches
    """
    matches = get_employee(employee_name)

    if not matches:
        return "not_found", None
    if len(matches) > 1:
        return "ambiguous", matches
    return "found", matches[0]


def _not_found_message(employee_name: str) -> str:
    return f"Sorry, no employee named '{employee_name}' was found in the company database."


def _ambiguous_message(employee_name: str, matches) -> str:
    names = ", ".join(row["employee_name"] for row in matches)
    return (
        f"Multiple employees match '{employee_name}': {names}. "
        f"Please specify the full name."
    )


@tool
def get_employee_details(employee_name: str):
    """
    Retrieve employee details using the employee name (full or partial).

    Args:
        employee_name: Full or partial name of the employee.

    Returns:
        Employee ID and employee name, or a message if not found / ambiguous.
    """

    status, data = resolve_employee(employee_name)

    if status == "not_found":
        return _not_found_message(employee_name)

    if status == "ambiguous":
        return _ambiguous_message(employee_name, data)

    return data


@tool
def get_total_absents(employee_name: str):
    """
    Returns the total number of absences of an employee.

    Args:
        employee_name: Full or partial name of the employee.
    """

    status, data = resolve_employee(employee_name)

    if status == "not_found":
        return _not_found_message(employee_name)

    if status == "ambiguous":
        return _ambiguous_message(employee_name, data)

    full_name = data["employee_name"]
    total = count_absents(full_name)

    return f"""
        "employee_name": {full_name},
        "total_absents": {total},
    """


@tool
def get_total_lates(employee_name: str):
    """
    Returns the total number of late marks of an employee.

    Args:
        employee_name: Full or partial name of the employee.
    """

    status, data = resolve_employee(employee_name)

    if status == "not_found":
        return _not_found_message(employee_name)

    if status == "ambiguous":
        return _ambiguous_message(employee_name, data)

    full_name = data["employee_name"]
    total = count_lates(full_name)

    return f"""
        "employee_name": {full_name},
        "total_lates": {total},
    """


@tool
def get_monthly_attendance_tool(
    employee_name: str,
    month: int,
    year: int,
):
    """
    Retrieve monthly attendance records for an employee.

    Args:
        employee_name: Employee name (full or partial).
        month: Month number (1-12).
        year: Year.
    """

    status, data = resolve_employee(employee_name)

    if status == "not_found":
        return _not_found_message(employee_name)

    if status == "ambiguous":
        return _ambiguous_message(employee_name, data)

    full_name = data["employee_name"]
    records = get_monthly_attendance(full_name, month, year)

    return f"""
    Employee: {full_name}
    Month: {month}
    Year: {year}
    Present: {records['present']}
    Absent: {records['absent']}
    Late: {records['late']}
    Leave: {records['leave']}
    """


@tool
def get_yearly_attendance_tool(
    employee_name: str,
    year: int,
):
    """
    Retrieve yearly attendance records for an employee.

    Args:
        employee_name: Employee name (full or partial).
        year: Year.
    """

    status, data = resolve_employee(employee_name)

    if status == "not_found":
        return _not_found_message(employee_name)

    if status == "ambiguous":
        return _ambiguous_message(employee_name, data)

    full_name = data["employee_name"]
    records = get_yearly_attendance(full_name, year)

    return f"""
    Employee: {full_name}
    Year: {year}
    Present: {records['present']}
    Absent: {records['absent']}
    Late: {records['late']}
    Leave: {records['leave']}
    """


@tool
def get_attendance_percentage_tool(
    employee_name: str,
    year: int,
):
    """
    Calculate yearly attendance percentage.

    Args:
        employee_name: Employee name (full or partial).
        year: Year.
    """

    status, data = resolve_employee(employee_name)

    if status == "not_found":
        return _not_found_message(employee_name)

    if status == "ambiguous":
        return _ambiguous_message(employee_name, data)

    full_name = data["employee_name"]
    percentage = attendance_percentage(full_name, year)

    return f"""
        "employee_name": {full_name},
        "year": {year},
        "attendance_percentage": {percentage} %,
    """


@tool
def evaluate_employee_performance(
    employee_name: str,
    year: int,
):
    """
    Evaluate employee performance based on yearly attendance.

    Performance Policy:

    >=90%  -> Excellent
    80-89% -> Good
    60-79% -> Needs Improvement
    <60%   -> Poor
    """

    status, data = resolve_employee(employee_name)

    if status == "not_found":
        return _not_found_message(employee_name)

    if status == "ambiguous":
        return _ambiguous_message(employee_name, data)

    full_name = data["employee_name"]
    percentage = attendance_percentage(full_name, year)
    performance = evaluate_performance(percentage)

    return f"""
    Employee: {full_name}
    Year: {year}
    Attendance Percentage: {percentage}
    Performance: {performance['rating']}
    Remark: {performance['remark']}
    """


tools = [
    get_employee_details,
    get_total_absents,
    get_total_lates,
    get_monthly_attendance_tool,
    get_yearly_attendance_tool,
    get_attendance_percentage_tool,
    evaluate_employee_performance,
]