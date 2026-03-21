import math
import random

from toepen import ToepPlay, ToepPlayer


class ZeroOrderPlayer(ToepPlayer):
    def observe_play(self, cards: tuple[str, str], player_count: int, current_suit: str, player_id: int, previous_play: ToepPlay, lead_suit: str) -> None:
        if lead_suit is not None and previous_play.suit != lead_suit:
            self.void_suits[player_id].add(lead_suit)
        
        
    def call_witte_was(self, cards: tuple[str, str]) -> str | None:
        face_cards = {"J", "Q", "K", "A"}
        if all(rank in face_cards for rank, suit in cards):
            return "WITTE_WAS"
        if sum(1 for rank, suit in cards if rank in face_cards) == 3:
            return "WITTE_WAS"
        if (
            self.hand_strength <= 13
        ):  # This is the highest combination of cards that have 3 faces and 1 number (AAA7)
            return "WITTE_WAS"
        return None

    def call_toep(self, cards: tuple[str, str], ante: int, lead_suit) -> str | None:
        if (
            self.hand_strength >= 24
        ):  # High hand strength, this corresponds (exactly) to at leats 3 tens or: four 9's, two 10's and two 8's, etc.
            return "TOEP"
        if (
            len({suit for _, suit in cards}) == 1
            and any(rank == "10" for rank, _ in cards)
        ):  # if the agent has 4 cards of the same suit and a high card (for now, a 10), they can exhaust the opponent's hand by starting strong and ending with cards of a suit the opponent does not have.
            return "TOEP"
        if lead_suit is None and len({suit for _, suit in cards}) == 1:
            # If the agent is leading and only has cards of the same suit, and this is the leading suit that the opponents do not have, return TOEP
            return "TOEP"   #Also need to have this work if the agent is leading and has only cards of the same suit, but later in the game. 
        if lead_suit is None and self.hand_strength >= 18: #If agent starts and has good cards
            return "TOEP"
        return None

    def respond_to_witte_was(self, cards: tuple[str, str]) -> str:
        p_4_face_cards = math.comb(16, 4) / math.comb(32, 4)
        if random.random() >= p_4_face_cards:
            return "DOUBT"
        return "BELIEVE"

    def respond_to_toep(self, cards: tuple[str, str], ante: int) -> str:
        remaining_cards = len(cards)
        if (
            # If opponent toeps after winning a trick with a card of a suit that the agent does not have, pass (Is this more suited for ToM1 agent?)
            # Might be too complicated for a tom0 agent. 
        ):
            pass
        if remaining_cards == 1 and self.hand_strength >= 6:
            return "MEEGAAN"
        if remaining_cards == 2 and self.hand_strength >= 12:
            return "MEEGAAN"
        if remaining_cards == 3 and self.hand_strength >= 18:
            return "MEEGAAN"
        if (
            self.hand_strength >= 20
        ):  # I think I need to make this more flexible, as the opponent can toep at the final trick, and the agent could have already discarded all his good cards at that point.
            return "MEEGAAN"
        return "PASS"


class PessimisticZeroOrderPlayer(ZeroOrderPlayer):
    """Always plays the lowest card in hand, in order to end with the strongest card."""

    def take_turn(
        self,
        cards: tuple[str, str],
        player_count: int,
        current_suit: str,
        trick
    ) -> str:
        if current_suit is None:  # ToM1 plays initial card
            return min(
                cards, key=lambda c: self.rank_strength[c[0]]
            )  # throw away lowest ranked card to finish with highest
        same_suit = [c for c in cards if c[1] == current_suit]

        if same_suit:
            return min(same_suit, key=lambda c: self.rank_strength[c[0]])
        return min(cards, key=lambda c: self.rank_strength[c[0]])


class OptimisticZeroOrderPlayer(ZeroOrderPlayer):
    """Always play the highest card in hand, but not if following suit is not possible."""
    def take_turn(
        self,
        cards: tuple[str, str],
        player_count: int,
        current_suit: str,
        trick
    ) -> str:
        if current_suit is None:  # ToM1 plays initial card
            return max(
                cards, key=lambda c: self.rank_strength[c[0]]
            )  # throw away lowest ranked card to finish with highest
        same_suit = [c for c in cards if c[1] == current_suit]

        if same_suit:
            return max(same_suit, key=lambda c: self.rank_strength[c[0]])
        return min(cards, key=lambda c: self.rank_strength[c[0]])


class RationalZeroOrderPlayer(ZeroOrderPlayer):
    """Tries to win the trick with the lowest possible card if possible. If not, discard lowest card in hand. """
    def take_turn(
        self,
        cards: tuple[str, str],
        player_count: int,
        current_suit: str,
        trick,
    ) -> str:
        # update strength dynamically
        self.hand_strength = sum(self.rank_strength[r] for r, _ in cards)
        # leading, play lowest
        if current_suit is None:
            return min(cards, key=lambda c: self.rank_strength[c[0]])
        same_suit = [c for c in cards if c[1] == current_suit]
        if same_suit:
            # get highest card in current trick (same suit only)
            same_suit_plays = [p for p in trick if p.suit == current_suit]
            if same_suit_plays:
                highest = max(
                    same_suit_plays,
                    key=lambda x: self.rank_strength[x.rank],
                )
                winning_cards = [
                    c
                    for c in same_suit
                    if self.rank_strength[c[0]] > self.rank_strength[highest.rank]
                ]
                if winning_cards:
                    return min(winning_cards, key=lambda c: self.rank_strength[c[0]])
            return min(same_suit, key=lambda c: self.rank_strength[c[0]])
        # cannot follow suit
        return min(cards, key=lambda c: self.rank_strength[c[0]])


# ReasonableZeroOrderPlayer assumes previous_play, but that variable never gets updated inside Toepen.
