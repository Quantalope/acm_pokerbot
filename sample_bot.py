from inspect import stack

import websocket
import json
import uuid
import os
from dotenv import load_dotenv

class PokerBot:
    def __init__(self):
        load_dotenv()
        self.server_ip = os.getenv('SERVER_IP')
        self.port = os.getenv('PORT')
        # self.port = 3002
        self.ws = None
        self.player_id = str(uuid.uuid4())
        self.name = input("Enter your name: ")
        self.buy_in = 1000
        self.community_cards = []
        self.pot = 0
        self.currentBet = 0

    def on_message(self, ws, message):
        data = json.loads(message)

        if data["type"] == "privateState":
            print("\n=== Your Private Info ===")
            state = data["state"]

            # Show hole cards
            if "holeCards" in state:
                hole_cards = [f"{card['_rank']}{card['_suit']}" for card in state["holeCards"]]
                print(f"Your hole cards: {' '.join(hole_cards)}")

            # Show available actions
            availableActions = state["availableActions"]
            if availableActions:
                print(f"Available actions: {', '.join(availableActions)}")
                if "minRaise" in state:
                    print(f"Min raise: {state['minRaise']}")
                if "maxBet" in state:
                    print(f"Max bet: {state['maxBet']}")

            if availableActions == []:
                print("No actions available - waiting for other players")
                return

            action = input("Choose action: ").lower()

            if action in availableActions:
                if action in ["bet", "raise"]:
                    amount = int(input("Enter amount: "))
                    self.send_action(action, amount)
                else:
                    self.send_action(action)
            else:
                print(f"Invalid action. Must be one of: {availableActions}")

            # try:
            #     if "bet" in availableActions:
            #         bet_amount = int(input("How much bet?\n"))
            #         self.send_action("bet", bet_amount)
            #     elif "raise" in availableActions:
            #         raise_amount = int(input("How much raise?\n"))
            #         self.send_action("raise", raise_amount)
            #     elif "call" in availableActions:
            #         self.send_action("call")
            #     elif "check" in availableActions:
            #         self.send_action("check")
            #     else:
            #         self.send_action("fold")
            # except Exception as e:
            #     print(e)

            # self.send_action("call")

        elif data["type"] == "gameState":
            print("\n=== Table Info ===")
            state = data["state"]

            # Show community cards
            if state["communityCards"]:
                community = [f"{card['_rank']}{card['_suit']}" for card in state["communityCards"]]
                print(f"Community cards: {' '.join(community)}")

            # Show pot and round
            print(f"Pot: ${state['pot']}")
            print(f"Current round: {state['currentRound']}")

            # Show active players
            print("\nPlayers:")
            for player in state["players"]:
                if player is not None:
                    status = "FOLDED" if player["folded"] else "Active"
                    current = "(Current Actor)" if player["isCurrentActor"] else ""
                    print(f"  {player['name']}: ${player['stackSize']} {status} {current}")
            print()

        elif data["type"] == "handComplete":
            if any(winner['playerId'] == self.player_id for winner in data['winners']):
                print("\n🎉 YOU WON! ��")
            else:
                print("\n😢 YOU LOST 😢")

        elif data["type"] == "players":
            print("\n=== Players at Table ===")
            for player in data["players"]:
                if player is not None:
                    print(f"  {player['name']}")
            print()

    def on_error(self, ws, error):
        print(error)

    def on_open(self, ws):
        self.send_join()

    def send_action(self, action, amount=0):
        print("Sent action {action} for {amount}".format(action=action, amount=amount))
        self.ws.send(json.dumps({
            "playerId": self.player_id,
            "type": "action",
            "action": action,
            "amount": amount
        }))

    def send_join(self):
        self.ws.send(json.dumps({
            "type": "join",
            "playerId": self.player_id,
            "name": self.name,
            "buyIn": self.buy_in
        }))

    def run(self):
        self.ws = websocket.WebSocketApp(
            f"ws://{self.server_ip}:{self.port}",
            # f"ws://localhost:3002",
            on_message=self.on_message,
            on_error=self.on_error,
            on_open=self.on_open
        )
        self.ws.run_forever()

if __name__ == "__main__":
    bot = PokerBot()
    bot.run()