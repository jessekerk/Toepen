#For simplicity, this version of toepen ends the game when the final card is played, 
# not when the final card is played after 15 rounds as is customary. 

import random


class ToepPlay:
    def __init__(self, count: int, suit: str, player_id: int) -> None:
        self.count = count
        self.suit = suit
        self.player_id = player_id

    def __str__(self) -> str:
        return f"{self.count} x {self.suit} played by {self.player_id}"


class ToepPlayer:
    def start_game(self, identifier: int, cards: tuple[str]):
        self.identifier = identifier

    def take_turn(
        self,
        cards: tuple[str],
        player_count: int,
        current_suit: str,
        previous_play: ToepPlay,
    ) -> ToepPlay:  # type: ignore
        # Here, current_rank will be the suit played by the previous opponent, or the rank the ToMx agent wants to play if he starts.
        pass

    def observe_play(
        self,
        cards: tuple[str],
        player_count: int,
        current_suit: str,
        player_id: int,
        previous_play: ToepPlay,
    ) -> None:
        pass

    def observe_toep(
        self,
        cards: tuple[str],
        player_count: int,
        current_suit: str,
        player_id: int,
        previous_play: ToepPlay,
    ) -> None:
        pass
            
      
import random


class ToepController:
    SUITS = ["♠", "♣", "♥", "♦"]
    RANKS = ["J", "Q", "K", "A", "7", "8", "9", "10"]
    RANK_STRENGTH = {rank: i for i, rank in enumerate(RANKS)}

    def __init__(self):
        self._players = []
        
    def join(self, player):
        if player not in self._players:
            self._players.append(player)
            
    def _shuffle_and_divide(self):
        deck = [(rank, suit) for suit in self.SUITS for rank in self.RANKS]
        random.shuffle(deck)
        hands = []
        for i in range(len(self._players)):
            hands.append(deck[i * 4:(i + 1) * 4])
        return hands

    def _trick_winner(self, trick):
        lead_suit = trick[0][1][1]
        valid_cards = [
            (p, card)
            for (p, card) in trick
            if card[1] == lead_suit
        ]
        winner = max(
            valid_cards,
            key=lambda x: self.RANK_STRENGTH[x[1][0]]
        )
        return winner[0]

    def play(self, *, debug=False):
        hands = self._shuffle_and_divide()
        for i, player in enumerate(self._players):
            player.start_game(i, tuple(hands[i]))
        starting_player = 0
        winner = None
        for trick_number in range(4):
            trick = []
            lead_suit = None
            if debug:
                print("\n--- TRICK", trick_number + 1, "---")
            for i in range(len(self._players)):
                player_id = (starting_player + i) % len(self._players)
                if debug:
                    print("\n--- TURN ---")
                    for pid, hand in enumerate(hands):
                        print(f"Player {pid} hand:", sorted(hand))
                    print("Current trick:", trick)
                    print("Lead suit:", lead_suit)
                    print("Current player:", player_id)
                card = self._players[player_id].take_turn(
                    tuple(hands[player_id]),
                    len(self._players),
                    lead_suit,
                    trick
                )
                if card not in hands[player_id]:
                    raise ValueError("Illegal card played")
                # FOLLOW SUIT RULE
                if lead_suit is not None:
                    player_suits = [c[1] for c in hands[player_id]]
                    if lead_suit in player_suits and card[1] != lead_suit:
                        raise ValueError(
                            f"Player {player_id} failed to follow suit"
                        )
                hands[player_id].remove(card)
                if lead_suit is None:
                    lead_suit = card[1]
                trick.append((player_id, card))
                if debug:
                    print("Player", player_id, "plays", card)
                for p in range(len(self._players)):
                    self._players[p].observe_play(
                        tuple(hands[p]),
                        len(self._players),
                        lead_suit,
                        player_id,
                        card
                    )
            winner = self._trick_winner(trick)
            starting_player = winner
            if debug:
                print("Trick winner:", winner)
        if debug:
            print("\nGame winner:", winner)
        return winner
      
    def repeated_games(
        self,
        number_of_games: int,
        *,
        win_score: int = 1,
    ) -> list[int]:
        total_score = [0 for _ in range(len(self._players))]
        for _ in range(number_of_games):
            winner = self.play()  # your play() returns an int
            total_score[winner] += win_score # type: ignore
        return total_score
      
        
if __name__ == "__main__":
    controller = ToepController()
    players = [ToepPlayer() for _ in range(2)]
    for p in players:
        controller.join(p)
    hands = controller._shuffle_and_divide()
    print("Hands dealt:\n")
    for i, hand in enumerate(hands):
        print(f"Player {i}: {hand}")
    # simple correctness checks
    all_cards = [card for hand in hands for card in hand]
    print("\nTotal cards dealt:", len(all_cards))
