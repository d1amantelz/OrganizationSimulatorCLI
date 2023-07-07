from typing import NoReturn


class WrongNumberOfArgumentsError(Exception):
    pass


class IncorrectEmployeeIdError(Exception):
    pass


class IncorrectFlagError(Exception):
    pass


class IncorrectArgumentsError(Exception):
    pass


class CommandNotFoundError(Exception):
    pass


class IncorrectLogLevelError(Exception):
    pass

    
def raise_wrong_number_of_arguments_error() -> NoReturn:
    raise WrongNumberOfArgumentsError(
        'Invalid number of arguments for the command!')


def raise_incorrect_employee_id_error() -> NoReturn:
    raise IncorrectEmployeeIdError('Invalid Employee ID!')


def raise_incorrect_flag_error() -> NoReturn:
    raise IncorrectFlagError('Invalid flag for this command!')


def raise_incorrect_arguments_error() -> NoReturn:
    raise IncorrectArgumentsError('Invalid arguments for this command!')


def raise_command_not_found_error() -> NoReturn:
    raise CommandNotFoundError('Command not found!')


def raise_incorrect_log_level_error() -> NoReturn:
    raise IncorrectLogLevelError('Invalid log level!')