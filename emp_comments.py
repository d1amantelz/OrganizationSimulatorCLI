import os


def create_comment(_id: int, name: str, surname: str) -> None:
    with open(f'comments/{_id}_{name}_{surname}.txt', 'w') as file:
        pass


def delete_comment(_id: int, name: str, surname: str) -> None:
    os.remove(f'comments/{_id}_{name}_{surname}.txt')


def read_comment(_id: int, name: str, surname: str) -> str:
    with open(f'comments/{_id}_{name}_{surname}.txt') as file:
        return file.read()


def clear_comment(_id: int, name: str, surname: str) -> None:
    with open(f'comments/{_id}_{name}_{surname}.txt', 'w') as file:
        pass


def set_comment(_id: int, name: str, surname: str, comment: str) -> None:
    with open(f'comments/{_id}_{name}_{surname}.txt', 'w') as file:
        file.write(comment)
