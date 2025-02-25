# PokerBot

A framework for building and testing custom poker-playing algorithms. This project is 
designed for students participating in a mini-hackathon to create their own poker strategies 
and compete against other bots.

## 📁 Project Structure
```
├── pokerbot
│   ├── __init__.py
│   │   ├── core.cpython-312.pyc
│   │   └── evaluator.cpython-312.pyc
│   ├── core.py
│   ├── evaluator.py
│   └── strategies
│       ├── __init__.py
│       └── example_strat_1.py
└── main.py
```


## 🚀 Getting Started


### Installation

```bash
pip install -r requirements.txt
cd pokerbot
```


## 🤖 How to Build Your Own Strategy
Create a new Python file inside the strategies folder. Here’s a basic template:

```python
from pokerbot.evaluator import eval_hand


def strat_action(game_state):
    """
    Write your strategy here. The function receives a dictionary `game_state`
    with the following keys:
      - 'hole_cards': List of two cards dealt to your bot
      - 'community_cards': List of shared cards on the table
      - 'stack_size': Your current stack size
      - 'current_bet': The current bet to call
      - 'pot': The total amount in the pot

    Return a dictionary with:
      - 'action': One of 'fold', 'check', 'call', 'raise'
      - 'amount': The amount to bet/raise (if applicable)
    """
    evaluated_hand = eval_hand(game_state['hole_cards'], game_state['community_cards'])
    stack_size = game_state['stack_size']
    current_bet = game_state['current_bet']

    # All-in condition for strong hands if stack is smaller than the current bet
    def go_all_in():
        return {"action": "raise", "amount": stack_size}

    # Example logic (replace with your custom strategy)
    if evaluated_hand in ["Royal Flush", "Straight Flush", "Four of a Kind"]:
        if stack_size <= current_bet:
            return go_all_in()  # Go all-in if stack size is smaller than the current bet
        max_raise = min(current_bet * 3, stack_size)
        return {"action": "raise", "amount": max_raise}

    elif evaluated_hand in ["Full House", "Flush", "Straight"]:
        raise_amount = min(current_bet * 2, stack_size)
        return {"action": "raise", "amount": raise_amount}

    elif evaluated_hand in ["Three of a Kind", "Two Pair", "One Pair"]:
        call_amount = min(current_bet, stack_size)
        return {"action": "call", "amount": call_amount}

    else:
        # Fold if calling is not possible (stack too small)
        if stack_size < current_bet:
            return go_all_in()  # Consider going all-in as a last-ditch effort
        return {"action": "fold", "amount": 0}
```

## 📊 Understanding game_state
The game_state dictionary provides:

```
hole_cards: Your two private cards.
community_cards: Shared cards on the table (flop, turn, river).
stack_size: Total chips your bot has.
current_bet: Chips required to stay in the game.
pot: Total amount of chips collected for the current hand.
Use this information to evaluate the situation and implement your strategy.
```

## 🏆 Competing Against Other Bots
1. Write your custom strategy.
2. Add your strategy to the strategies directory.
3. Run the main game loop (to be provided or implemented by the competition organizers).
4. The bot with the highest stack at the end of a set number of games wins!

## 💡 Example Strategy: Command Line Input
An example strategy given `example_strat_1.py` lets users decide actions manually:

1. Evaluates your hand strength.
2. Displays the current game state.
3. Accepts user input for actions (fold, check, call, raise).
4. 📝 Contribution Guidelines
5. Stick to the existing folder structure.
6. Add proper comments and documentation.
7. Test your strategy thoroughly before submitting.