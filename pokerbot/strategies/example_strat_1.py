from pokerbot.evaluator import eval_hand


def strat_action(game_state):
    """
    Takes command-line input from the user to decide the next action.
    Evaluates the current hand and displays it for user reference.
    """
    # Evaluate the hand using the hole and community cards
    hole_cards = game_state.get('hole_cards', [])
    community_cards = game_state.get('community_cards', [])
    evaluated_hand = eval_hand(hole_cards, community_cards)

    print("\n--- Current Game State ---")
    print(f"Stack Size: {game_state['stack_size']}")
    print(f"Current Bet: {game_state['current_bet']}")
    print(f"Pot: {game_state['pot']}")
    print(f"Hole Cards: {hole_cards}")
    print(f"Community Cards: {community_cards}")
    print(f"Evaluated Hand: {evaluated_hand}")
    print("--------------------------")

    # Display action options
    print("Choose an action:")
    print("1: Fold")
    print("2: Check")
    print("3: Call")
    print("4: Raise")
    print(f"Available Actions : {game_state['availableActions']}")

    # Get user input
    while True:
        try:
            user_input = input("Enter the number corresponding to your action: ").strip()
            if user_input == '1':
                return {"action": "fold", "amount": 0}
            elif user_input == '2':
                return {"action": "check", "amount": 0}
            elif user_input == '3':
                return {"action": "call", "amount": game_state['current_bet']}
            elif user_input == '4':
                raise_amount = int(input("Enter raise amount: ").strip())
                return {"action": "raise", "amount": raise_amount}
            else:
                print("Invalid input. Please enter a number between 1 and 4.")
        except ValueError:
            print("Invalid input. Please enter valid numbers for your choices.")
