import os
from typing import List, Dict
from loguru import logger

from .constants import SORT_PARAMS, ROLES_FLAGS, VALID_LEVELS
from .roles import Accountant, Employee, Role
from .exceptions import *
from .db_funcs import *
import abc

# Ensure the logs directory exists for proper logging functionality
if not os.path.exists('logs'):
    os.makedirs('logs')

# Disable logging output to the console
logger.remove(0)

# Add a log file to the project directory
logger.add('logs/app.log', format='{time} | {level} | {message}',
           level='DEBUG', rotation='1 MB', compression='zip', backtrace=True)


class CmdCompleter:
    def __init__(self, options: List[str]) -> None:
        self.options = options

    def complete(self, text: str, state: int) -> str | None:
        response = None
        if state == 0:
            if text:
                self.matches = [s
                                for s in self.options
                                if s and s.startswith(text)]
            else:
                self.matches = self.options[:]

        try:
            response = self.matches[state]
        except IndexError:
            response = None
        return response


def get_command_list() -> List[str]:
    """
    Get the list of available command names.
    """

    return list(CommandParser.COMMANDS.keys())


def clear_screen():
    """
    Clear the console screen.
    """

    os.system('cls' if os.name == 'nt' else 'clear')


class Command(abc.ABC):
    """
    Abstract base class for commands.
    """

    @abc.abstractmethod
    def execute(self, args):
        """
        Executes the command with the given arguments.
        """


class CommandParser:
    """
    CommandParser class is responsible for parsing user input and executing 
    the corresponding command.
    """

    COMMANDS: Dict[str, Command] = {}

    @classmethod
    def register_command(cls, command_name):
        def decorator(command_class):
            cls.COMMANDS[command_name] = command_class
            return command_class
        return decorator

    @staticmethod
    def parse(inpt):
        """
        Parses user input and executes the corresponding command.
        """

        full_cmd = inpt.lower().split()
        cmd = full_cmd[0]
        args = full_cmd[1:]

        if cmd in CommandParser.COMMANDS:
            command_class = CommandParser.COMMANDS[cmd]
            command_class.execute(*args)
        else:
            raise_command_not_found_error()


@CommandParser.register_command('help')
class HelpCommand(Command):
    """
    Command to display a list of available commands.
    """

    @staticmethod
    def execute(*args) -> None:
        """
        Executes the help command.
        """

        if args:
            raise_wrong_number_of_arguments_error()

        print('\nList of available commands:\n')
        for cmd_name, command_class in CommandParser.COMMANDS.items():
            class_doc = command_class.__doc__
            if class_doc:
                command_desc = class_doc.strip()[8:].capitalize()
            print(f"- {cmd_name} - {command_desc}")
        print()


@CommandParser.register_command('clear')
class ClearCommand(Command):
    """
    Command to clear the console screen.
    """

    @staticmethod
    def execute(*args) -> None:
        """
        Executes the clear command.
        """

        if args:
            raise_wrong_number_of_arguments_error()
        os.system('cls' if os.name == 'nt' else 'clear')


@CommandParser.register_command('man')
class ManCommand(Command):
    """
    Command to display the manual for a specific command.
    """

    @staticmethod
    def execute(*args) -> None:
        """
        Executes the man command.
        """

        if len(args) != 1:
            raise_wrong_number_of_arguments_error()

        manual = ManCommand.__read_cmd_manual(args[0])
        if manual:
            print(manual)

    @staticmethod
    def __read_cmd_manual(cmd: str) -> str | None:
        """
        Read the manual content for a specific command.
        """

        if cmd not in CommandParser.COMMANDS:
            raise_command_not_found_error()

        with open(f'organization_simulator_cli/manuals/{cmd}.txt', 'r') as file:
            result = file.read()
            return result


@CommandParser.register_command('list')
class ListCommand(Command):
    """
    Command to list employees with optional sorting and filtering.
    """

    @staticmethod
    def execute(*args: str) -> None:
        """
        Executes the list command.
        """

        sort_param = None
        role_flags = []

        for param in args:
            if param.startswith('--sort='):
                sort_param = param[7:]
                if sort_param not in SORT_PARAMS:
                    raise_incorrect_flag_error()
            elif param.startswith('-'):
                role_flag = param[1:]
                if role_flag not in ROLES_FLAGS:
                    raise_incorrect_flag_error()
                role_flags.append(role_flag)
            else:
                raise_incorrect_flag_error()

        employees = fetch_all_employees()

        if role_flags:
            filtered_employees = []
            for role_flag in role_flags:
                role = ListCommand.get_role_from_flag(role_flag)
                if role is not None:
                    filtered_employees.extend(fetch_employees_by_role(role))
            employees = filtered_employees

        print_employees_table(employees, sort_param)

    @staticmethod
    def get_role_from_flag(role_flag: str) -> Role | None:
        match role_flag:
            case 'f':
                return Role.FRONTENDER
            case 'b':
                return Role.BACKENDER
            case 't':
                return Role.TEAM_LEADER
            case 'r':
                return Role.RECRUITER
            case 'a':
                return Role.ACCOUNTANT
            case _:
                return None


@CommandParser.register_command('calculate')
class CalculateCommand(Command):
    """
    Command to calculate the salary for a specific employee.
    """

    @staticmethod
    def execute(*args: str) -> None:
        """
        Executes the calculate command.
        """

        if len(args) != 1:
            raise_wrong_number_of_arguments_error()

        employee_id = int(args[0])
        result = fetch_employee_by_id(employee_id)

        if result is None:
            raise_incorrect_employee_id_error()

        print(
            f'\nEmployee: {result[1]} {result[2]}'
            f'\nSalary: ${Accountant.calculate_salary(result):,}\n')


@CommandParser.register_command('add')
class AddCommand(Command):
    """
    Command to add a new employee to the database.
    """

    @staticmethod
    def execute(*args: str) -> None:
        """
        Executes the add command.
        """

        if len(args) != 6:
            raise_wrong_number_of_arguments_error()

        name, surname = args[0], args[1]
        age = int(args[2])
        phone_number, bank_card_number = args[3], args[4]
        role_str = args[5].upper()

        if not hasattr(Role, role_str):
            raise_incorrect_arguments_error()

        role = getattr(Role, role_str)
        employee = Employee(
            name,
            surname,
            age,
            phone_number,
            bank_card_number,
            role)

        insert_into_db(employee)
        logger.success(
            'Employee has been successfully added to the database!')
        print(
            '\nEmployee has been successfully added to the database!\n')


@CommandParser.register_command('remove')
class RemoveCommand(Command):
    """
    Command to remove an employee from the database.
    """

    @staticmethod
    def execute(*args: str) -> None:
        """
        Executes the remove command.
        """

        if len(args) != 1:
            raise_wrong_number_of_arguments_error()

        employee_id = int(args[0])
        result = fetch_employee_by_id(employee_id)

        if result is None:
            raise_incorrect_employee_id_error()

        remove_employee_by_id(employee_id)
        logger.success('Employee has been successfully removed!')
        print('\nEmployee has been successfully removed!\n')


@CommandParser.register_command('read_comment')
class ReadCommentCommand(Command):
    """
    Command to read the comment for a specific employee.
    """

    @staticmethod
    def execute(*args: str) -> None:
        """
        Executes the read_comment command.
        """

        if len(args) != 1:
            raise_wrong_number_of_arguments_error()

        employee_id = int(args[0])
        result = fetch_employee_by_id(employee_id)

        if result is None:
            raise_incorrect_employee_id_error()

        print(
            f'\nComment Content: \n\n{ReadCommentCommand.__read_comment(*result[:3])}\n')

    @staticmethod
    def __read_comment(_id: int, name: str, surname: str) -> str:
        """
        Read the comment content for a specific employee.
        """

        with open(f'organization_simulator_cli/comments/{_id}_{name}_{surname}.txt') as file:
            return file.read()


@CommandParser.register_command('clear_comment')
class ClearCommentCommand(Command):
    """
    Command to clear the comment for a specific employee.
    """

    @staticmethod
    def execute(*args: str) -> None:
        """
        Executes the clear_comment command.
        """

        if len(args) != 1:
            raise_wrong_number_of_arguments_error()

        employee_id = int(args[0])
        employee_data = fetch_employee_by_id(employee_id)

        if employee_data is None:
            raise_incorrect_employee_id_error()

        ClearCommentCommand.__clear_comment(*employee_data[:3])
        print('\nComment has been successfully cleared!\n')

    @staticmethod
    def __clear_comment(_id: int, name: str, surname: str) -> None:
        """
        Clear the comment for a specific employee.
        """

        with open(f'organization_simulator_cli/comments/{_id}_{name}_{surname}.txt', 'w') as f:
            logger.success('Comment has been successfully cleared!')


@CommandParser.register_command('set_comment')
class SetCommentCommand(Command):
    """
    Command to set or change the comment for a specific employee.
    """

    @staticmethod
    def execute(*args: str) -> None:
        """
        Executes the set_comment command.
        """

        if len(args) != 1:
            raise_wrong_number_of_arguments_error()

        employee_id = int(args[0])
        employee_data = fetch_employee_by_id(employee_id)

        if employee_data is None:
            raise_incorrect_employee_id_error()

        comment = input('\nEnter a comment: \n\n')
        SetCommentCommand.__set_comment(_id=employee_id,
                                        name=employee_data[1],
                                        surname=employee_data[2],
                                        comment=comment)
        print('\nComment has been successfully changed!\n')

    @staticmethod
    def __set_comment(_id: int, name: str, surname: str, comment: str) -> None:
        """
        Set or change the comment for a specific employee.
        """

        with open(f'organization_simulator_cli/comments/{_id}_{name}_{surname}.txt', 'w') as file:
            file.write(comment)
            logger.success('Comment has been successfully changed!')


@CommandParser.register_command('logs')
class LogsCommand(Command):
    """
    Command to manage the application logs.
    """

    @staticmethod
    def execute(*args: str) -> None:
        """
        Executes the logs command.
        """

        if len(args) != 1:
            raise_wrong_number_of_arguments_error()

        try:
            last_lines = int(args[0])
            LogsCommand.__show_last_logs(last_lines)
            return
        except ValueError:
            pass

        if args[0] == 'clear':
            LogsCommand.__clear_logs()
            return

        if args[0].startswith('--level='):
            level = args[0][8:].upper()
            if level not in VALID_LEVELS:
                raise_incorrect_log_level_error()
            LogsCommand.__filter_logs_by_level(level)
            return

        raise_incorrect_arguments_error()

    @staticmethod
    def __show_last_logs(last_lines: int) -> None:
        """
        Show the last n lines of the logs.
        """

        with open('logs/app.log', 'r') as file:
            print()
            lines = file.readlines()
            start_index = max(0, len(lines) - last_lines)
            logs_exist = False
            for line in lines[start_index:]:
                print(line.strip())
                logs_exist = True

            if not logs_exist:
                print('No logs yet.')
            print()

    @staticmethod
    def __clear_logs() -> None:
        """
        Clear the application logs.
        """

        open('logs/app.log', 'w').close()
        print('\nLogs have been successfully cleared!\n')

    @staticmethod
    def __filter_logs_by_level(level: str) -> None:
        """
        Filter the logs by the specified log level.
        """

        with open('logs/app.log', 'r') as file:
            print()
            found_level = False
            for line in file:
                if level.lower() in line.lower():
                    print(line.strip())
                    found_level = True

            if not found_level:
                print(f'No logs found with level "{level}"')
            print()


@CommandParser.register_command('game')
class GameCommand(Command):
    pass
