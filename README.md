# PokerBot

## 🚀 Getting Started

## 🏆 How the Tournament Will Proceed (IMPORTANT)

1. For the first hour, we will be building bots in teams of 2 or 3. (Find instructions below.)
2. In the second hour, you will run your bot and compete with other bots. By this point, make sure your team is registered
    and has a unique ID for your seat at the table. 

## The tournament will proceed in a knockout format

### 1️⃣ 1st Round
In Blocks of 4 minutes (3 tables total)

1st Block: 9/9/9 bots

2nd Block: 8/8/8 bots

...

6th Block 3/3/3 bots

First 24 minutes: bots will be evenly divided into 3 tables. The bot with the lowest stack will be kicked out every 4 minutes.
  In total, 6 bots will be kicked in this round. The top 3 will then proceed to the next round.

### 2️⃣ 2nd Round
In Blocks of 4 minutes (1 table total)

1st Block: 9 bots

2nd Block: 8 bots

9th Block: 1 bot remaining 

Next 25 minutes: the top 3 bots from all 3 tables will compete on a single table against each other.
    The bot with the lowest stack will be kicked out every 4 minutes. The top bot remaining will win!

### ❗️ At any point if a bot takes more than 10 seconds to make a move, they will be kicked out.

Prizes TBA!

## 🤖 How to Build Your Own Strategy

1. Clone the Poker Table system here and set it up (instructions provided on that repo).
2. Clone this repository.

### Installation

```bash
pip install -r requirements.txt
cd pokerbot
```

3. Run an example bot using the strategy provided (`example_strat_1.py`). All you have to do for this have 
   two or more team members run `main.py` and connect to server provided (edit server and port details in a ``.env`` file).
   (Or you can run multiple bots in different terminals.)
4. Once you understand how the game proceeds, look at `example_strat_2.py` for a very bare bones approach of how you can
    think about making a Poker bot that thinks algorithmically. Change line 21 in ``main.py`` to use ``example_strat_2`` instead.
5. Once you understand this, you can proceed to ``example_strat_3.py`` which is a little more complicated but nothing too crazy.
6. If you have any questions, reach out to any organizing members walking around. Good luck!

Some data definitions are provided below, but it is not necessary to use them.

## 📊 Understanding private_state
The private_state dictionary provides:

```
hole_cards: Your two private cards.
community_cards: Shared cards on the table (flop, turn, river).
pot: Total amount of chips collected for the current hand.
available_actions: The actions you can take (combination of "check, call, raise, fold, bet")
current_bet: Chips required to stay in the game.
min_raise: Minimum total amount to put in if you want to raise.
max_bet: The maximum you can bet in this turn.
stack_size: Total chips your bot has.
```
Use this information to evaluate the situation and implement your strategy.