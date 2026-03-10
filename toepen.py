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


class ToepController:
    SUITS: list[str] = ["♠", "♣", "♥", "♦"]
    RANKS: list[str] = ["J", "Q", "K", "A", "7", "8", "9", "10"]
    RANK_STRENGTH = {
        rank: i for i, rank in enumerate(RANKS)
    }  # Not sure how to use this in code.

    ante = 1 #This is the score awarded to the loser, it is += 1 every time Toep is called
    
    def __init__(self) -> None:
        self._players = []

    def join(self, player: ToepPlayer):
        if player not in self._players:
            self._players.append(player)

    def _shuffle_and_divide(self) -> list[list[tuple[str, str]]]:
        deck = [(rank, suit) for suit in self.SUITS for rank in self.RANKS]
        random.shuffle(deck)
        hands = [[] for _ in self._players]
        for i in range(len(self._players)):
            hands[i] = deck[i * 4 : (i + 1) * 4]
        return hands

    def play(self, *, debug=False) -> int:  #type: ignore
        hands = self._shuffle_and_divide()
        for i, player in enumerate(self._players):
            player.start_game(i, tuple(hands[i]))   #start game signal
        current_suit = 0
        current_rank = 0
        current_player = 0
        lead_suit = 0
        winner = None
        last_action: list[str] = []
        last_play: ToepPlay | None = None   #Either the agent responds to a play or makes the first play. 
        while (
            winner is None
        ):
            if debug:
                for player in range(len(self._players)):
                    print(f"Player {player} has hand {sorted(hands[player])}")
                    print("Current suit is", self.SUITS[current_suit])
                    print("Current rank is", self.RANKS[current_rank])
                    #NEED TO ADD MORE DEBUG INFO HERE 
            if len(hands[current_player]) == 0 and last_action is not None: 
        
        
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


#Current problems: 
# Implementing Toepen logic (but this is should be done in the ToMk player logic, anyway), maybe for simplicity leave this for later 
# Implementing meegaan / pass logic (but this is should be done in the ToMk player logic, anyway) 
# Implementing 4 plays in a round logic 
# Implementing kleur bekennen logic (but this is should be done in the ToMk player logic, anyway)  
# Implementing turn-taking logic, where the winner gets to play the first card. 