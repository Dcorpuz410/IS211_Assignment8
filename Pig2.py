import random
import time
import argparse

class Die:
    """Represents a six-sided die."""
    def __init__(self, seed=0):
        random.seed(seed)

    def roll(self):
        return random.randint(1, 6)

class Player:
    """Base class for a player in Pig."""
    def __init__(self, name):
        self.name = name
        self.score = 0

    def add_score(self, points):
        self.score += points

    def reset_turn(self):
        pass

    def decide(self, turn_total):
        """This should be overridden by subclasses."""
        raise NotImplementedError()

class HumanPlayer(Player):
    """Represents a human player."""
    def decide(self, turn_total):
        while True:
            choice = input("Enter 'r' to roll or 'h' to hold: ").strip().lower()
            if choice in ['r', 'h']:
                return choice
            print("Invalid input. Please enter 'r' to roll or 'h' to hold.")

class ComputerPlayer(Player):
    """Represents a computer-controlled player."""
    def decide(self, turn_total):
        """Computer strategy: hold at min(25, 100 - current score)."""
        if turn_total >= min(25, 100 - self.score):
            return 'h'
        return 'r'

class PlayerFactory:
    """Factory to create either a HumanPlayer or ComputerPlayer."""
    @staticmethod
    def create_player(player_type, name):
        if player_type.lower() == "human":
            return HumanPlayer(name)
        elif player_type.lower() == "computer":
            return ComputerPlayer(name)
        else:
            raise ValueError("Invalid player type. Choose 'human' or 'computer'.")

class PigGame:
    """Handles the core game logic."""
    def __init__(self, player1_type, player2_type):
        self.die = Die()
        self.players = [
            PlayerFactory.create_player(player1_type, "Player 1"),
            PlayerFactory.create_player(player2_type, "Player 2")
        ]
        self.current_player = 0  # 0 or 1 (alternates)

    def switch_turn(self):
        """Switches to the other player."""
        self.current_player = 1 - self.current_player  

    def play(self):
        """Plays a full game of Pig."""
        print("Welcome to the Pig game!")

        while True:
            player = self.players[self.current_player]
            turn_total = 0

            print(f"\n{player.name}'s turn. Current score: {player.score}")

            while True:
                choice = player.decide(turn_total)

                if choice == 'r':
                    roll = self.die.roll()
                    print(f"{player.name} rolled a {roll}.")

                    if roll == 1:
                        print("Rolled a 1! No points added. Turn over.")
                        turn_total = 0
                        break
                    else:
                        turn_total += roll
                        print(f"Turn total: {turn_total}, Game score if held: {player.score + turn_total}")

                elif choice == 'h':
                    player.add_score(turn_total)
                    print(f"{player.name} holds. Added {turn_total} points. New score: {player.score}")
                    break

            if player.score >= 100:
                print(f"\n{player.name} wins with a score of {player.score}!")
                break

            self.switch_turn()

class TimedGameProxy:
    """Proxy class that enforces a 1-minute time limit on the game."""
    def __init__(self, player1_type, player2_type):
        self.game = PigGame(player1_type, player2_type)
        self.start_time = time.time()

    def play(self):
        """Plays the game with a time limit."""
        print("Starting a timed game (1-minute limit)...")

        while True:
            elapsed_time = time.time() - self.start_time
            if elapsed_time >= 60:
                print("\nTime is up! Determining the winner...")
                self.determine_winner()
                break

            player = self.game.players[self.game.current_player]
            turn_total = 0

            print(f"\n{player.name}'s turn. Current score: {player.score}")

            while True:
                if time.time() - self.start_time >= 60:
                    print("\nTime is up during the turn! Stopping the game.")
                    self.determine_winner()
                    return

                choice = player.decide(turn_total)

                if choice == 'r':
                    roll = self.game.die.roll()
                    print(f"{player.name} rolled a {roll}.")

                    if roll == 1:
                        print("Rolled a 1! No points added. Turn over.")
                        turn_total = 0
                        break
                    else:
                        turn_total += roll
                        print(f"Turn total: {turn_total}, Game score if held: {player.score + turn_total}")

                elif choice == 'h':
                    player.add_score(turn_total)
                    print(f"{player.name} holds. Added {turn_total} points. New score: {player.score}")
                    break

            if player.score >= 100:
                print(f"\n{player.name} wins with a score of {player.score}!")
                break

            self.game.switch_turn()

    def determine_winner(self):
        """Determines the winner based on who has the most points."""
        p1, p2 = self.game.players
        if p1.score > p2.score:
            print(f"{p1.name} wins with {p1.score} points!")
        elif p2.score > p1.score:
            print(f"{p2.name} wins with {p2.score} points!")
        else:
            print("It's a tie!")

def main():
    # Ask for player types
    player1_type = input("Enter Player 1 type (human/computer): ").strip().lower()
    player2_type = input("Enter Player 2 type (human/computer): ").strip().lower()

    timed_mode = input("Do you want to play in timed mode? (yes/no): ").strip().lower()

    if timed_mode == "yes":
        game = TimedGameProxy(player1_type, player2_type)
    else:
        game = PigGame(player1_type, player2_type)

    game.play()

if __name__ == "__main__":
    main()