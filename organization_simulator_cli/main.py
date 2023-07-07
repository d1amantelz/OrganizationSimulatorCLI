import readline
from .cmd_parser import CommandParser, CmdCompleter, get_command_list, clear_screen
from loguru import logger


def main() -> None:
    """
    The main function that reads the user input and processes the commands.
    """

    readline.set_completer(CmdCompleter(get_command_list()).complete)
    readline.parse_and_bind('tab: complete')

    while True:
        try:

            command_input = input('> ').strip()
            if command_input == 'exit':
                raise KeyboardInterrupt
            if command_input == 'clear':
                clear_screen()
                continue
            CommandParser.parse(command_input)

        except (UnicodeDecodeError, KeyboardInterrupt):
            print('\nSee you next time!\n')
            break

        except Exception as e:
            logger.error(f'An error occurred: {str(e).capitalize()}')
            print(f'\nERROR: {str(e).capitalize()}')
            print('NOTE: To view the manual for a command, write: man <command>\n')


if __name__ == '__main__':
    main()
