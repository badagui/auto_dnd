import random

def roll_dices(count, sides):
    """
    Roll [count] dices, each with [sides] sides. 
    Use this tool for determining outcomes in gameplay, such as combat events, ability checks, saving throws, random events, etc. 
    The result is an array containing each individual dice roll, which can then be interpreted and applied to the game mechanic or decision. 
    You can call this function multiple times to roll different sided dices.
    """
    results = [random.randint(1, sides) for _ in range(count)]
    return f"Rolling {count} dices with {sides} sides: {results}"