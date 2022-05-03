def InvalidCommand() -> str:
    return "The inputed command is invalid."


def NoArguments(commandName: str) -> str:
    return f"The command {commandName} has no arguments."


def InvalidCommandUsage(commandName: str, argumentNames: dict) -> str:
    result = f"Invalid usage. The correct usage is:\n\
                {commandName}"
    for argument in argumentNames:
        if argumentNames[argument]:
            result += f" {argument}"
        else:
            result += f" [{argument}]"
    
    return result

def NoPermissions(levelNeeded: str):
    return f"You do not have the permissions to use this command. Permissions needed \'{levelNeeded}\'"