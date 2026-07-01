from sqlalchemy import text
from database import get_connection


def get_employee(employee_name):
    query = text("""
        SELECT DISTINCT
            employee_id,
            employee_name
        FROM attendence
        WHERE employee_name ILIKE :name
    """)

    with get_connection() as conn:
        result = conn.execute(query, {"name": f"%{employee_name}%"})
        return result.mappings().all()


def get_monthly_attendance(employee_name, month, year):

    query = text("""
        SELECT
            COUNT(*) FILTER (WHERE status='Present') AS present,
            COUNT(*) FILTER (WHERE status='Absent') AS absent,
            COUNT(*) FILTER (WHERE status='Late') AS late,
            COUNT(*) FILTER (WHERE status='Leave') AS leave
        FROM attendence
        WHERE
            employee_name ILIKE :name
            AND EXTRACT(MONTH FROM date) = :month
            AND EXTRACT(YEAR FROM date) = :year
    """)

    with get_connection() as conn:
        result = conn.execute(
            query, {"name": f"%{employee_name}%", "month": month, "year": year}
        )
        return result.mappings().first()


def get_yearly_attendance(employee_name, year):

    query = text("""
        SELECT
            COUNT(*) FILTER (WHERE status='Present') AS present,
            COUNT(*) FILTER (WHERE status='Absent') AS absent,
            COUNT(*) FILTER (WHERE status='Late') AS late,
            COUNT(*) FILTER (WHERE status='Leave') AS leave
        FROM attendence
        WHERE
            employee_name ILIKE :name
            AND EXTRACT(YEAR FROM date)=:year
    """)

    with get_connection() as conn:
        result = conn.execute(query, {"name": f"%{employee_name}%", "year": year})
        return result.mappings().first()


def count_absents(employee_name):

    query = text("""
        SELECT COUNT(*)
        FROM attendence

        WHERE
            employee_name ILIKE :name
            AND status='Absent'
    """)

    with get_connection() as conn:
        result = conn.execute(query, {"name": f"%{employee_name}%"})
        return result.scalar()


def count_lates(employee_name):

    query = text("""
        SELECT COUNT(*)
        FROM attendence

        WHERE
            employee_name ILIKE :name
            AND status='Late'
    """)

    with get_connection() as conn:
        result = conn.execute(query, {"name": f"%{employee_name}%"})
        return result.scalar()


def attendance_percentage(employee_name, year):

    query = text("""
        SELECT

            COUNT(*) AS total_days,

            SUM(
                CASE
                    WHEN status='Present'
                    THEN 1
                    ELSE 0
                END
            ) AS present_days

        FROM attendence

        WHERE
            employee_name ILIKE :name
            AND EXTRACT(YEAR FROM date)=:year
    """)

    with get_connection() as conn:
        result = conn.execute(query, {"name": f"%{employee_name}%", "year": year})

        row = result.mappings().first()

        if row["total_days"] == 0:
            return 0

        return round(row["present_days"] / row["total_days"] * 100, 2)