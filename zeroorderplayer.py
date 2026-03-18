import math
import random

from toepen import ToepPlayer


class ZeroOrderPlayer(ToepPlayer):
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

    def call_toep(self, cards: tuple[str, str], ante: int) -> str | None:
        if (
            self.hand_strength >= 24
        ):  # High hand strength, this corresponds (exactly) to at leats 3 tens or: four 9's, two 10's and two 8's, etc.
            return "TOEP"
        if (
            len({suit for _, suit in cards}) == 1
            and any(rank == "10" for rank, _ in cards)
        ):  # if the agent has 4 cards of the same suit and a high card (for now, a 10), they can exhaust the opponent's hand by starting strong and ending with cards of a suit the opponent does not have.
            return "TOEP"
        if (
            # If the agent is leading and only has cards of the same suit, and this is the leading suit that the opponents do not have, return TOEP
        ):
            pass
        return None

    def respond_to_witte_was(self, cards: tuple[str, str]) -> str:
        p_4_face_cards = math.comb(16, 4) / math.comb(32, 4)
        if random.random() >= p_4_face_cards:
            return "DOUBT"
        return "BELIEVE"

    def respond_to_toep(self, cards: tuple[str, str], ante: int) -> str:
        if (
            # If opponent toeps after winning a trick with a card of a suit that the agent does not have, pass (Is this more suited for ToM1 agent?)
        ):
            pass
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
        previous_play: tuple[str, str],
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
        previous_play: tuple[str, str],
    ) -> str:
        if current_suit is None:  # ToM1 plays initial card
            return max(
                cards, key=lambda c: self.rank_strength[c[0]]
            )  # throw away lowest ranked card to finish with highest
        same_suit = [c for c in cards if c[1] == current_suit]

        if same_suit:
            return max(same_suit, key=lambda c: self.rank_strength[c[0]])
        return min(cards, key=lambda c: self.rank_strength[c[0]])


class ReasonableZeroOrderPlayer(ZeroOrderPlayer):
    """Play lowest card unless you can win the trick (then play lowest winning card)."""

    def take_turn(
        self,
        cards: tuple[str, str],
        player_count: int,
        current_suit: str,
        previous_play: tuple[str, str],
    ):
        # If starting, just play lowest
        if current_suit is None:
            return min(cards, key=lambda c: self.rank_strength[c[0]])
        same_suit = [c for c in cards if c[1] == current_suit]

        if same_suit:
            # If no previous play (first in trick), just lowest
            if not previous_play:
                return min(same_suit, key=lambda c: self.rank_strength[c[0]])
            # Find current highest card in trick
            highest = max(previous_play, key=lambda p: self.rank_strength[p.rank]) # type: ignore
            # Cards that can beat it
            winning_cards = [
                c
                for c in same_suit
                if self.rank_strength[c[0]] > self.rank_strength[highest.rank] # type: ignore
            ]
            if winning_cards:
                # play smallest card that still wins
                return min(winning_cards, key=lambda c: self.rank_strength[c[0]])
            # cannot win,  dump lowest
            return min(same_suit, key=lambda c: self.rank_strength[c[0]])
        # Cannot follow suit, dump lowest card
        return min(cards, key=lambda c: self.rank_strength[c[0]])

# ReasonableZeroOrderPlayer assumes previous_play, but that variable never gets updated inside Toepen. 