from utils.menu import Menu

def setup() -> None:
    guild_id = int(input("Enter your Guild ID:"))
    announce_channel = int(input("Enter channel ID where the bot is allowed to announce things:"))
    general = int(input("Enter general chat ID:"))
    bot_commander_roles = []
    check = "y"
    print()
    while check == "y":
        i = int(input("Enter the ID of role that can control the bot: "))
        bot_commander_roles.append(i)
        check = input("Enter more roles? (y/n): ")
    chat_money_channels = []
    check = "y"
    print()
    while check == "y":
        i = int(input("Enter the ID of a channel where users will be allowed to earn currency for chatting: "))
        chat_money_channels.append(i)
        check = input("Enter more channels? (y/n): ")

    with open(".\secret\constants_test.py", "w+") as f:
        data = f"GUILD_ID = {guild_id}\nBOT_ANNOUNCE_CHANNEL = {announce_channel}\nGENERAL_CHAT = {general}\nBOT_COMMANDER_ROLES = {bot_commander_roles}\nCHAT_MONEY_CHANNELS = {chat_money_channels}"
        f.write(data)

    print("Constants set up.")



if __name__ == "__main__":
    functions = [setup, ]
    menu = Menu(*functions, heading="Bot Control", format_symbol="=", continue_prompt=False)
    menu.run()