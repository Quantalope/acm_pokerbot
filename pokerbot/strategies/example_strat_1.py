def strat_action(game_state):
    """
    A strategy function that prompts the user via command-line
    to choose an action based on the current game state.
    Returns a dictionary with keys 'action' and 'amount'.
    """

    hole_cards = game_state.get("holeCards", [])
    community_cards = game_state.get("communityCards", [])
    pot = game_state.get("pot", 0)
    current_bet = game_state.get("currentBet", 0)
    available_actions = game_state.get("availableActions", [])
    min_raise = game_state.get("minRaise", 0)
    max_bet = game_state.get("maxBet", 0)
    stack_size = game_state.get("stackSize", 0)

    # Print relevant information for user reference
    # Format hole cards as rank + suit
    formatted_hole = [f"{card['_rank']}{card['_suit']}" for card in hole_cards]
    formatted_community = [f"{card['_rank']}{card['_suit']}" for card in community_cards]

    print("\n=== Your Private Info ===")
    if formatted_hole:
        print(f"Your hole cards: {' '.join(formatted_hole)}")

    print(f"Available actions: {', '.join(available_actions) if available_actions else 'None'}")
    print(f"Min raise: {min_raise}")
    print(f"Max bet: {max_bet}")
    print("\n=== Table Info ===")
    print(f"Community cards: {' '.join(formatted_community) if formatted_community else 'No community cards yet'}")
    print(f"Pot: ${pot}")
    print(f"Current bet: ${current_bet}")
    print(f"Stack Size: ${stack_size}")

    # If no actions are available, just return a no-op (fold) or wait
    if not available_actions:
        print("No actions available; returning fold...")
        return {"action": "fold", "amount": 0}

    # Prompt user for which action to take
    while True:
        action = input(f"\nChoose an action {available_actions}): ").strip().lower()

        # Validate action
        if action not in available_actions:
            print(f"Invalid action. Must be one of: {available_actions}")
            continue

        # If action requires an amount, prompt for it
        if action in ["bet", "raise"]:
            try:
                amount = int(input("Enter amount: ").strip())
            except ValueError:
                print("Invalid amount. Please enter a numeric value.")
                continue
            return {"action": action, "amount": amount}
        else:
            # For fold, check, or call (no additional input needed)
            return {"action": action, "amount": 0}
