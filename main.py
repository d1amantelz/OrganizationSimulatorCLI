from cmd_parser import CommandParser
from constants import QUIT_MSGS


def main():

    while True:
        try:

            cm = input('> ').lower()

            if cm == 'clear':
                CommandParser.clear_screen()
                continue
            elif cm in QUIT_MSGS:
                raise KeyboardInterrupt

            CommandParser.parse(cm)

        except (KeyboardInterrupt, UnicodeDecodeError):
            print('\nДо встречи!\n')
            break


if __name__ == '__main__':
    main()
