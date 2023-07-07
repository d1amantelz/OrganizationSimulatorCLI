import os
from loguru import logger


@staticmethod
def create_comment(_id: int, name: str, surname: str) -> None:
    with open(f'comments/{_id}_{name}_{surname}.txt', 'w') as file:
        logger.success(
            'An empty comment for new employee (↓) has been successfully created!')

@staticmethod
def delete_comment(_id: int, name: str, surname: str) -> None:
    os.remove(f'comments/{_id}_{name}_{surname}.txt')
    logger.success(
        'A comment for the employee (↓) has been successfully deleted!')
