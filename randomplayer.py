from toepen import *
from toepen import ToepPlay 


class RandomPlayer(ToepPlayer):
    def take_turn(self, cards, player_count, lead_suit, trick): #type: ignore
        if lead_suit is None:
            return random.choice(cards)
        
        same_suit = [c for c in cards if c[1] == lead_suit]

        if same_suit:
            return random.choice(same_suit)
        return random.choice(cards)
