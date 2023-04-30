"""
Self-made logger for the bot.
"""

import datetime
import colorama

class LogCommand():

    """
    Log commands.
    """

    def __init__(self) -> None:
        super(LogCommand, self).__init__()
        # D/M/Y H:M:S
        self.current_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    def info(self, author: str, msg: str) -> None:
        msg = f"{colorama.Fore.BLUE}{self.current_time} {colorama.Fore.LIGHTBLUE_EX}{author}{colorama.Fore.RESET} > {colorama.Fore.LIGHTGREEN_EX}{msg}{colorama.Fore.RESET}"
        print(msg)
    
    def error(self, author: str, msg: str) -> None:
        msg = f"{colorama.Fore.BLUE}{self.current_time} {colorama.Fore.LIGHTBLUE_EX}{author}{colorama.Fore.RESET} > {colorama.Fore.LIGHTRED_EX}{msg}{colorama.Fore.RESET}"
        print(msg)
    
    def warn(self, author: str, msg: str) -> None:
        msg = f"{colorama.Fore.BLUE}{self.current_time} {colorama.Fore.LIGHTBLUE_EX}{author}{colorama.Fore.RESET} > {colorama.Fore.YELLOW}{msg}{colorama.Fore.RESET}"
        print(msg)

    def log_err_code(self, msg: str) -> None:
        msg = f"{colorama.Fore.BLUE}{self.current_time} {colorama.Fore.LIGHTMAGENTA_EX}{msg}{colorama.Fore.RESET}"
        print(msg)