import enum
from constants import BASE_SALARY, SalaryCoefficients


class Role(enum.Enum):
    FRONTENDER = 'Frontender'
    BACKENDER = 'Backender'
    TEAM_LEADER = 'Team_Leader'
    RECRUITER = 'Recruiter'
    ACCOUNTANT = 'Accountant'


class Employee:
    def __init__(self, name: str,
                 surname: str,
                 age: int,
                 phone_number: str,
                 bank_card_number: str,
                 major: Role):
        self.name = name.capitalize()
        self.surname = surname.capitalize()
        self.age = age
        self.phone_number = phone_number
        self.bank_card_number = bank_card_number
        self.major = major

    def __repr__(self) -> str:
        return f'{self.major.name}({self.name!r}, {self.surname!r}, {self.age})'

    def __str__(self) -> str:
        return f'{self.surname} {self.name[0]}.'


class Accountant(Employee):
    @staticmethod
    def calculate_salary(employee: tuple) -> int:
        coefficient = getattr(SalaryCoefficients, employee[-1])
        total_salary = BASE_SALARY * coefficient
        return int(total_salary)

    @staticmethod
    def pay_salary(employee: Employee) -> None:
        pass


class FrontendDeveloper(Employee):
    def develop_frontend(self) -> None:
        # Разработка frontend
        pass


class BackendDeveloper(Employee):
    def develop_backend(self) -> None:
        # Разработка backend
        pass


class TeamLead(Employee):
    def manage_team(self) -> None:
        # Управление командой
        pass


class Recruiter(Employee):
    def hire_employee(self, new_employee: Employee) -> None:
        pass


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
