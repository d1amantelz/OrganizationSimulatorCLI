import os
from pathlib import Path

from constants import Exceptions, SORT_PARAMS, ROLES_FLAGS
from db_funcs import *
from roles import Accountant, Employee, Role, get_role_from_flag
from emp_comments import read_comment, clear_comment, set_comment


class CommandParser:
    @staticmethod
    def parse(inpt: str) -> None:
        """ Парсинг переданных команд на корректность,
            а также их исполнение. """

        if not inpt:
            return

        full_cmd = inpt.lower().split()
        cmd = full_cmd[0]

        match cmd:
            case 'help':
                CommandParser.__parse_help_cmd()
            case 'list':
                CommandParser.__parse_list_cmd(full_cmd)
            case 'man':
                CommandParser.__parse_man_cmd(full_cmd)
            case 'calculate':
                CommandParser.__parse_calculate_cmd(full_cmd)
            case 'add':
                CommandParser.__parse_add_cmd(full_cmd)
            case 'remove':
                CommandParser.__parse_remove_cmd(full_cmd)
            case 'read_comment':
                CommandParser.__parse_read_comment_cmd(full_cmd)
            case 'clear_comment':
                CommandParser.__parse_clear_comment_cmd(full_cmd)
            case 'set_comment':
                CommandParser.__parse_set_comment_cmd(full_cmd)
            case _:
                print(Exceptions.CommandNotFoundError)

    @staticmethod
    def __parse_help_cmd() -> None:

        print('\nСписок доступных команд:')
        manuals_dir = Path('manuals')

        for file_path in manuals_dir.iterdir():
            if file_path.is_file():
                command_name = file_path.stem
                with file_path.open() as manual_file:
                    _, second_line = manual_file.readline(), manual_file.readline()
                    command_description = second_line.strip().capitalize()
                    print(f'~ {command_name} - {command_description}')

        print()

    @staticmethod
    def clear_screen() -> None:
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def __read_cmd_manual(cmd: str) -> str:
        try:
            with open(f'manuals/{cmd}.txt') as file:
                result = file.read()
                return result
        except FileNotFoundError:
            return Exceptions.CommandNotFoundError

    @staticmethod
    def __parse_man_cmd(full_cmd: List[str]) -> None:
        if len(full_cmd) != 2:
            print(Exceptions.ArgumentError)
            return

        print(CommandParser.__read_cmd_manual(full_cmd[1]))

    @staticmethod
    def __parse_list_cmd(full_cmd: List[str]) -> None:
        sort_param = None
        role_flags = []

        for param in full_cmd[1:]:
            if param.startswith('--sort='):
                sort_param = param[7:]
                if sort_param not in SORT_PARAMS:
                    print(Exceptions.IncorrectFlagError)
                    return
            elif param.startswith('-'):
                role_flag = param[1:]
                if role_flag not in ROLES_FLAGS:
                    print(Exceptions.IncorrectFlagError)
                    return
                role_flags.append(role_flag)
            else:
                print(Exceptions.IncorrectFlagError)
                return

        employees = fetch_all_employees()

        if role_flags:
            filtered_employees = []
            for role_flag in role_flags:
                role = get_role_from_flag(role_flag)
                if role is not None:
                    filtered_employees.extend(fetch_employees_by_role(role))
            employees = filtered_employees

        print_employees_table(employees, sort_param)

    @staticmethod
    def __parse_calculate_cmd(full_cmd: List[str]) -> None:
        if len(full_cmd) != 2:
            print(Exceptions.ArgumentError)
            return

        try:
            employee_id = int(full_cmd[1])
            result = fetch_employee_by_id(employee_id)

            if result is None:
                raise ValueError

            print(
                f'\nСотрудник: {result[1]} {result[2]}'
                f'\nЗарплата составляет: {Accountant.calculate_salary(result):,}р.\n')

        except ValueError:
            print(Exceptions.IncorrectIdError)
            return

    @staticmethod
    def __parse_add_cmd(full_cmd: List[str]) -> None:
        if len(full_cmd) != 7:
            print(Exceptions.ArgumentError)
            return

        try:
            name, surname = full_cmd[1], full_cmd[2]
            age = int(full_cmd[3])
            phone_number, bank_card_number = full_cmd[4], full_cmd[5]
            role_str = full_cmd[6].upper()

            if not hasattr(Role, role_str):
                raise KeyError

            role = getattr(Role, role_str)
            employee = Employee(
                name,
                surname,
                age,
                phone_number,
                bank_card_number,
                role)
            insert_into_db(employee)
            print('\nСотрудник был успешно добавлен в БД!\n')

        except (ValueError, KeyError) as e:
            print(e)
            print(Exceptions.IncorrectArgumentsError)

    @staticmethod
    def __parse_remove_cmd(full_cmd: List[str]) -> None:
        if len(full_cmd) != 2:
            print(Exceptions.ArgumentError)
            return

        try:
            employee_id = int(full_cmd[1])
            result = fetch_employee_by_id(employee_id)

            if result is None:
                raise KeyError

            remove_employee_by_id(employee_id)
            print('\nСотрудник был успешно удален!\n')

        except (ValueError, KeyError):
            print(Exceptions.IncorrectIdError)

    @staticmethod
    def __parse_read_comment_cmd(full_cmd: List[str]) -> None:
        if len(full_cmd) != 2:
            print(Exceptions.ArgumentError)
            return

        try:
            employee_id = int(full_cmd[1])
            employee_comment = read_comment(
                *fetch_employee_by_id(employee_id)[:3])
            print(f'\nСодержимое комментария: \n\n{employee_comment}\n')

        except (TypeError, ValueError):
            print(Exceptions.IncorrectIdError)

    @staticmethod
    def __parse_clear_comment_cmd(full_cmd: List[str]) -> None:
        if len(full_cmd) != 2:
            print(Exceptions.ArgumentError)
            return

        try:
            employee_id = int(full_cmd[1])
            clear_comment(*fetch_employee_by_id(employee_id)[:3])
            print('\nКомментарий был успешно удален!\n')

        except (TypeError, ValueError):
            print(Exceptions.IncorrectIdError)

    @staticmethod
    def __parse_set_comment_cmd(full_cmd: List[str]) -> None:
        if len(full_cmd) != 2:
            print(Exceptions.ArgumentError)
            return

        try:
            employee_id = int(full_cmd[1])
            comment = input('\nВведите комментарий: \n\n')
            employee_data = fetch_employee_by_id(employee_id)
            set_comment(
                employee_data[0],  # id
                employee_data[1],  # name
                employee_data[2],  # surname
                comment=comment)
            print('\nКомментарий был успешно изменен!\n')

        except (TypeError, ValueError):
            print(Exceptions.IncorrectIdError)
