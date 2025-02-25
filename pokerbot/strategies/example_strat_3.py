from pokerbot.evaluator import eval_hand


def strat_action(game_state):
    """
    Improved Poker Strategy based on the current game state.
    """
    evaluated_hand = eval_hand(game_state['hole_cards'], game_state['community_cards'])
    stack_size = game_state['stack_size']
    current_bet = game_state['current_bet']
    available_actions = game_state.get('available_actions', [])

    # All-in condition for strong hands if stack is smaller than the current bet
    def go_all_in():
        return {"action": "raise", "amount": stack_size}

    # Strategy based on hand evaluation
    if evaluated_hand in ["Royal Flush", "Straight Flush", "Four of a Kind"]:
        if stack_size <= current_bet:
            return go_all_in()
        max_raise = min(current_bet * 3, stack_size)
        if "raise" in available_actions:
            return {"action": "raise", "amount": max_raise}
        elif "call" in available_actions:
            return {"action": "call", "amount": min(current_bet, stack_size)}
        else:
            return {"action": "check", "amount": 0}

    elif evaluated_hand in ["Full House", "Flush", "Straight"]:
        raise_amount = min(current_bet * 2, stack_size)
        if "raise" in available_actions:
            return {"action": "raise", "amount": raise_amount}
        elif "call" in available_actions:
            return {"action": "call", "amount": min(current_bet, stack_size)}
        else:
            return {"action": "check", "amount": 0}

    elif evaluated_hand in ["Three of a Kind", "Two Pair", "One Pair"]:
        if "call" in available_actions:
            return {"action": "call", "amount": min(current_bet, stack_size)}
        elif "check" in available_actions:
            return {"action": "check", "amount": 0}
        else:
            return {"action": "fold", "amount": 0}

    else:
        # Weaker hands strategy
        if "check" in available_actions:
            return {"action": "check", "amount": 0}
        elif "call" in available_actions and stack_size >= current_bet:
            return {"action": "call", "amount": min(current_bet, stack_size)}
        else:
            return {"action": "fold", "amount": 0}
