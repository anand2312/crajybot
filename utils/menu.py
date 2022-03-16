from __future__ import annotations

from typing import Callable


class Menu:
    """Tiny CLI helper"""

    def __init__(
        self,
        *methods: Callable[[], None],
        heading: str = "MENU!",
        format_symbol: str = "#",
        continue_prompt: bool = True,
        variables: dict | None = None,
    ) -> None:
        self.variables = variables
        self.methods = methods
        self.heading = heading
        self.continue_prompt = continue_prompt
        self.format_symbol = format_symbol

    def br(self) -> None:
        print(self.format_symbol * 20)

    def show_options(self) -> None:
        self.br()
        print("Pick your option")
        self.br()
        for i, j in enumerate(self.methods):
            print(f"{i+1}. {j.__name__}")
        self.br()

    def execute(self, choice: int) -> None:
        self.methods[choice - 1]()

    def get_choice(self) -> int:
        choice = int(input("Enter your choice:"))
        return choice

    def run(self) -> None:
        self.br()
        print(self.heading.upper())
        self.br()

        go_on = "y"

        while go_on.lower() == "y":
            self.show_options()
            choice = self.get_choice()
            try:
                self.execute(choice)
            except IndexError:
                print("Invalid choice.")
            self.br()
            if self.continue_prompt:
                go_on = input("Do you want to continue? (y/n)")
            else:
                go_on = "n"
        else:
            self.br()
