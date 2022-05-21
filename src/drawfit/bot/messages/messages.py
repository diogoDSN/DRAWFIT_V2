def NoPermission(needed: str):
    return f'You do not have permission to do this.\nTo execute this command you need `{needed}` permissions.'

def TimedOut():
    return "The request has timed out."

def Yes():
    return "👍"

def No():
    return "👎"

def DateFormating():
    return '%Y-%B-%d, %A\n%H:%M:%S'