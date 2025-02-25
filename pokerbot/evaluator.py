from collections import Counter

'''

["Royal Flush", "Straight Flush", "Four of a Kind", "Full House"]:
["Flush", "Straight"]:
["Three of a Kind", "Two Pair", "One Pair"]

Evaluates a hand from the hole and community cards.
'''

def eval_hand(hole_cards, community_cards):
    all_cards = hole_cards + community_cards
    values = [card[:-1] for card in all_cards]  # Card values (e.g., 'A', 'K', '10')
    suits = [card[-1] for card in all_cards]  # Card suits (e.g., 'H', 'D', 'S', 'C')

    value_map = {
        "2": 2, "3": 3, "4": 4, "5": 5, "6": 6,
        "7": 7, "8": 8, "9": 9, "10": 10,
        "J": 11, "Q": 12, "K": 13, "A": 14
    }
    numeric_values = sorted([value_map[v] for v in values])
    value_counter = Counter(numeric_values)
    suit_counter = Counter(suits)

    is_flush = any(count >= 5 for count in suit_counter.values())

    # Check for Straight
    def is_straight(values):
        values = sorted(set(values))
        for i in range(len(values) - 4):
            if values[i + 4] - values[i] == 4:
                return True
        # Special case: A-2-3-4-5 straight
        if set([14, 2, 3, 4, 5]).issubset(values):
            return True
        return False

    is_straight_hand = is_straight(numeric_values)

    # Check for Straight Flush
    if is_flush:
        flush_suit = suit_counter.most_common(1)[0][0]
        flush_cards = [value_map[card[:-1]] for card in all_cards if card[-1] == flush_suit]
        if is_straight(flush_cards):
            if max(flush_cards) == 14:
                return "Royal Flush"
            return "Straight Flush"

    # Check for Four of a Kind, Full House, Three of a Kind, Two Pair, One Pair
    counts = value_counter.values()
    if 4 in counts:
        return "Four of a Kind"
    if 3 in counts and 2 in counts:
        return "Full House"
    if is_flush:
        return "Flush"
    if is_straight_hand:
        return "Straight"
    if 3 in counts:
        return "Three of a Kind"
    if list(counts).count(2) == 2:
        return "Two Pair"
    if 2 in counts:
        return "One Pair"

    return "High Card"