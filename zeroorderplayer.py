#Can receive hand strength from: strength = sum(ToepController.RANK_STRENGTH[c[0]] for c in cards)
#           # choose medium card if possible
            #sorted_cards = sorted(
            #    cards,
            #    key=lambda c: ToepController.RANK_STRENGTH[c[0]]
            #)

            #mid = len(sorted_cards) // 2
            #return sorted_cards[mid]

#For following suit: 
#            same_suit = sorted(
            #same_suit,
            #key=lambda c: ToepController.RANK_STRENGTH[c[0]])
            #


from toepen import *

class BaselinePlayer(ToepPlayer):

    def start_game(self, identifier: int, cards):
        self.identifier = identifier

    def take_turn(self, cards, player_count, lead_suit, trick): #type: ignore
        #first turn
        if lead_suit is None:
            #call toep if hand is strong
            strength = sum(
                ToepController.RANK_STRENGTH[c[0]] for c in cards
            )
            if strength >= 20:
                return "TOEP"
            # choose medium card if possible
            sorted_cards = sorted(
                cards,
                key=lambda c: ToepController.RANK_STRENGTH[c[0]]
            )
            mid = len(sorted_cards) // 2
            return sorted_cards[mid]

        #follow suit
        same_suit = [c for c in cards if c[1] == lead_suit]

        if same_suit:

            same_suit = sorted(
                same_suit,
                key=lambda c: ToepController.RANK_STRENGTH[c[0]]
            )

            if trick:
                highest = max(
                    [c for _, c in trick if c[1] == lead_suit],
                    key=lambda c: ToepController.RANK_STRENGTH[c[0]]
                )

                # play smallest card that beats current highest
                for c in same_suit:
                    if (
                        ToepController.RANK_STRENGTH[c[0]]
                        > ToepController.RANK_STRENGTH[highest[0]]
                    ):
                        return c
            # otherwise play lowest of suit
            return same_suit[0]

        #cant follow suit and discard lowest. 
        return min(
            cards,
            key=lambda c: ToepController.RANK_STRENGTH[c[0]]
        )

    def observe_play(self, *args):  #type: ignore
        pass

    def observe_toep(self, *args): #type: ignore
        pass

    def respond_to_toep(self, cards, ante):
        # accept if hand has reasonable strength
        strength = sum(
            ToepController.RANK_STRENGTH[c[0]] for c in cards
        )
        if strength >= 16:
            return "MEEGAAN"
        return "PASS"
    
    
#MAKE THIS BETTER LATER WITH THIS STRUCTURE: 
#funcs: tom0 would toep, take turn. 