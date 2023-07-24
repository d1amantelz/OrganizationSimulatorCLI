import sqlite3 as sql
import prettytable
from typing import List, Tuple, Any, Optional


import os
from loguru import logger
from .roles import Employee, Role
from .emp_comments import create_comment, delete_comment
from .constants import SORT_PARAMS


def insert_into_db(__employee: Employee) -> None:
    if check_employee_exists(__employee):
        msg = 'This employee already exists in the database!'
        print(msg)
        logger.warning(msg)
        return

    with sql.connect('company.db') as con:
        cur = con.cursor()
        cur.execute(
            """ INSERT INTO employees VALUES (?, ?, ?, ?, ?, ?) """,
            (__employee.name,
             __employee.surname,
             __employee.age,
             __employee.phone_number,
             __employee.bank_card_number,
             __employee.major.value.upper()))

    create_comment(
        get_employee_id_from_obj(__employee),
        __employee.name,
        __employee.surname)


def get_employee_id_from_obj(__employee: Employee) -> int:
    with sql.connect('company.db') as con:
        cur = con.cursor()
        cur.execute(""" SELECT rowid FROM employees
                        WHERE name = ?
                        AND surname = ?
                        AND age = ? """,
                    (__employee.name, __employee.surname, __employee.age))
        employee_id = cur.fetchone()[0]
        return employee_id


def fetch_all_employees() -> List[Tuple[Any, ...]]:
    with sql.connect('company.db') as con:
        cur = con.cursor()
        cur.execute('SELECT rowid, * FROM employees ')
        return cur.fetchall()


def print_employees_table(
        employees: List[Tuple[Any, ...]], sort: Optional[str] = None) -> None:

    if sort is None or sort not in SORT_PARAMS:
        sort = 'id'

    table = prettytable.PrettyTable()
    table.field_names = [
        'ID',
        'Name',
        'Surname',
        'Age',
        'Phone Number',
        'Bank Card Number',
        'Major'
    ]

    employees.sort(key=lambda x: x[SORT_PARAMS.index(sort)])

    for employee in employees:
        table.add_row([*employee])

    print('\n' + table.get_string() + '\n')


def check_employee_exists(__employee: Employee) -> bool:
    with sql.connect('company.db') as con:
        cur = con.cursor()
        cur.execute("""
                SELECT COUNT(*) FROM employees
                WHERE name = ? AND surname = ?
                AND age = ? AND phone_number = ? """,
                    (__employee.name,
                     __employee.surname,
                     __employee.age,
                     __employee.phone_number))
        count = cur.fetchone()[0]

    return count > 0


def fetch_employee_by_id(__id: int) -> Tuple[Any, ...]:
    with sql.connect('company.db') as con:
        cur = con.cursor()
        cur.execute(
            """ SELECT rowid, * FROM employees WHERE rowid = ? """, (__id,))
        return cur.fetchone()


def remove_employee_by_id(__id: int) -> None:
    with sql.connect('company.db') as con:
        cur = con.cursor()
        cur.execute(
            """ SELECT name, surname FROM employees WHERE rowid = ? """, (__id,))
        name, surname = cur.fetchone()
        cur.execute(""" DELETE FROM employees WHERE rowid = ? """, (__id,))

    delete_comment(__id, name, surname)


def fetch_employees_by_role(__employee_role: Role) -> List[Tuple[Any, ...]]:
    with sql.connect('company.db') as con:
        cur = con.cursor()
        cur.execute("""
                SELECT rowid, * FROM employees
                WHERE major = ? """,
                    (__employee_role.value.upper(),))
        return cur.fetchall()
