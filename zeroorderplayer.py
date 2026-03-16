from toepen import ToepPlayer

class FirstOrderPlayer(ToepPlayer):
    
    def call_witte_was(self, cards: tuple[str]) -> str | None:
        face_cards = {"J","Q","K","A"}
        if all(rank in face_cards for rank, suit in cards):
            return "WITTE_WAS"

        
    