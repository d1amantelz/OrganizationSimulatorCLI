from typing import Type


QUIT_MSGS = {'quit', 'q', 'exit', 'ex'}
BASE_SALARY = 50_000
SORT_PARAMS = ('id', 'name', 'surname', 'age')
ROLES_FLAGS = ('f', 'b', 't', 'r', 'a')


class SalaryCoefficients:
    FRONTENDER = 1.0
    BACKENDER = 1.75
    TEAM_LEADER = 2.0
    RECRUITER = 1.5
    ACCOUNTANT = 1.0


def format_error_message(cls: Type) -> Type:
    for error_attribute, error_msg in cls.__dict__.items():
        if error_attribute.endswith('Error') and isinstance(error_msg, str):
            setattr(cls, error_attribute,
                    f'\n[{error_attribute}]: {error_msg}\n')
    return cls


@format_error_message
class Exceptions:
    ArgumentError = 'Неверное количество аргументов для команды.'
    CommandNotFoundError = 'Такой командой не существует.'
    IncorrectFlagError = 'Ошибка в написании флага для команды.'
    IncorrectIdError = 'Неверный идентификатор сотрудника.'
    IncorrectArgumentsError = 'Ошибка при написании аргументов.'
