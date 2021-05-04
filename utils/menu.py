# TO DO: Switch manage.py to argparse and delete this.


class Menu:
    """Pass in all the functions that has to be run in the menu
    For eg, if you had defined three functions
    def push():
        ...
    def pull():
        ...
    def pop():
        ...
    While making the Menu object, pass them all in as arguments, like
    menu_object = Menu(push, pull, pop)
    The other arguments the Menu takes are:
        1. Heading - heading for the menu
        2. Format Symbol - for making it look PrEtTy, Menu class will spam print this symbol all the time.
        3. Continue Prompt: Whether the menu should keep asking the user if they want to continue, or end execution after one loop.

    For eg, (using the above defined function) the way you would use this Menu class is;
    menu_object = Menu(push, pull, pop, heading="EXAMPLE!", format_symbol="=", continue_prompt=True)
    menu_object.run()
    """

    def __init__(
        self,
        *methods: tuple,
        heading: str = "MENU!",
        format_symbol: str = "#",
        continue_prompt: bool = True,
        variables: dict = None,
    ) -> "Menu":
        self.variables = variables
        self.methods = methods
        self.heading = heading
        self.continue_prompt = continue_prompt
        self.format_symbol = format_symbol

    def bullshit(self) -> None:
        print(self.format_symbol * 20)

    def show_options(self) -> None:
        number = len(self.methods)
        self.bullshit()
        print("Pick your option")
        self.bullshit()
        for i, j in enumerate(self.methods):
            print(f"{i+1}. {j.__name__}")
        self.bullshit()

    def execute(self, choice: int) -> None:
        self.methods[choice - 1]()

    def get_choice(self) -> int:
        choice = int(input("Enter your choice:"))
        return choice

    def run(self) -> None:
        self.bullshit()
        print(self.heading.upper())
        self.bullshit()

        go_on = "y"

        while go_on.lower() == "y":
            self.show_options()
            choice = self.get_choice()
            try:
                self.execute(choice)
            except IndexError:
                print("Invalid choice.")
            self.bullshit()
            if self.continue_prompt:
                go_on = input("Do you want to continue? (y/n)")
            else:
                go_on = "n"
        else:
            self.bullshit()
