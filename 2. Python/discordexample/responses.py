from random import choice, randint
def get_response(user_input: str) -> str:
    lowered: str = user_input.lower()

    if lowered == '':
        return 'Well, you are quiet'
    elif 'hello' in lowered:
        return 'Hello there! You need to code your AI Bot here'
    elif 'roll dice' in lowered:
        return f'You rolled a {randint(1, 6)}'
    elif 'help' in lowered:
        return f'you can say !data, !temp, or !pressure'
    else:
        return choice(['I don\'t have any brains',
                       'What?',
                       'Code me something good'])
