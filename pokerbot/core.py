import json
import uuid
import websocket
import os
from dotenv import load_dotenv


class PokerBot:
    def __init__(self, strategy, name):
        load_dotenv()
        self.strategy = strategy
        self.ws = None
        self.server_ip = os.getenv("SERVER_IP")
        self.port = os.getenv("PORT", 3002)
        self.player_id = str(uuid.uuid4())
        self.name = name
        self.buy_in = 1000
        self.community_cards = []
        self.hole_cards = []
        self.pot = 0
        self.current_bet = 0
        self.stack_size = 0

    def on_message(self, ws, message):
        data = json.loads(message)
        print("Received:", data)

        # Check if state exists in the incoming data
        state = data.get('state', {})
        gs = {
            'stack_size': self.stack_size,
            'current_bet': self.current_bet,
            'pot': self.pot,
            'hole_cards': self.hole_cards,
            'community_cards': self.community_cards
        }

        if data["type"] == "privateState":
            gs.update(state)
            move = self.strategy.strat_action(gs)
            if state.get('isCurrentActor', False):
                self.send_action(move["action"], move.get("amount", 0))

        elif data["type"] == "gameState":
            self.community_cards = state.get("communityCards", [])
            self.hole_cards = state.get("holeCards", [])
            self.pot = state.get("pot", 0)
            self.current_bet = state.get("currentBet", 0)
            self.stack_size = state.get("stackSize", 0)

        elif data["type"] == "handComplete":
            winners = data.get('winners', [])
            if any(winner['playerId'] == self.player_id for winner in winners):
                print("YOU WON!")
            else:
                print("YOU LOST!")

        elif data["type"] == "players":
            print("Players:", data.get("players", []))

    def on_error(self, ws, error):
        print("Error:", error)

    def on_close(self, ws, close_status_code, close_msg):
        print(f"WebSocket closed: {close_status_code} - {close_msg}")

    def on_open(self, ws):
        print("WebSocket opened, joining the game...")
        self.send_join()

    def send_action(self, action, amount=0):
        if self.ws:
            print(f"Sent action: {action} for {amount}")
            self.ws.send(json.dumps({
                "playerId": self.player_id,
                "type": "action",
                "action": action,
                "amount": amount
            }))
        else:
            print("[ERROR] WebSocket connection is not established.")

    def send_join(self):
        self.ws.send(json.dumps({
            "type": "join",
            "playerId": self.player_id,
            "name": self.name,
            "buyIn": self.buy_in
        }))

    def run(self):
        # Construct the WebSocket URL
        if not self.server_ip:
            print("[ERROR] SERVER_IP not set in .env file.")
            return

        ws_url = f"ws://{self.server_ip}:{self.port}"
        print(f"[INFO] Connecting to {ws_url}...")

        # Set up WebSocket with callbacks
        self.ws = websocket.WebSocketApp(
            ws_url,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close,
            on_open=self.on_open
        )

        # Run WebSocket connection
        self.ws.run_forever()
