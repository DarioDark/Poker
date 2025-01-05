from card import Card, CardSuits
from collections import defaultdict
from enum import Enum


class CardCombinations(Enum):
    HIGH_CARD = 1
    PAIR = 2
    TWO_PAIR = 3
    THREE_OF_A_KIND = 4
    STRAIGHT = 5
    FLUSH = 6
    FULL_HOUSE = 7
    FOUR_OF_A_KIND = 8
    STRAIGHT_FLUSH = 9
    ROYAL_FLUSH = 10


class CombinationHandler:
    def __init__(self, cards) -> None:
        self.cards: list[Card] = cards

    @property
    def combination(self) -> tuple[CardCombinations, list[Card]]:
        return self.get_final_combination()
    
    @property
    def power(self) -> int:
        return self.combination[0].value

    def get_card_num_occurences(self) -> dict[int: list[Card]]:
        """Create a dictionary with the occurences of each card depending on their value"""
        d = defaultdict(list)
        for card in self.cards:
            d[card.value].append(card)
        return dict(d)
    
    def get_card_suit_occurences(self) -> dict[str: list[Card]]:
        """Create a dictionary with the occurences of each card depending on their suit"""
        d = defaultdict(list)
        for card in self.cards:
            d[card.suit].append(card)
        return dict(d)
    
    def get_card_num_pairs(self) -> dict[int: list[Card]]:
        """Remove values that occur only once"""
        d = self.get_card_num_occurences()
        keys_to_remove = [key for key, value in d.items() if len(value) <= 1]
        for key in keys_to_remove:
            del d[key]
        return d
    
    def get_card_suit_pairs(self) -> dict[str: list[Card]]:
        """Remove suits that occur only once"""
        d = self.get_card_suit_occurences()
        keys_to_remove = [key for key, value in d.items() if len(value) <= 1]
        for key in keys_to_remove:
            del d[key]   
        return d

    def get_card_straight(self) -> list[Card] | bool:
        """Return the best straight (5 cards) in the cards"""
        if len(self.cards) < 5:
            return False

        straight_cards: list[Card] = [self.cards[-1]]
        # We start from the end of the list to get the highest straight
        for i in range(len(self.cards) - 1, -1, -1):
            card: Card = self.cards[i]
            last_card: Card = straight_cards[-1]
            if card.value == last_card.value - 1:
                straight_cards.append(card)
                if len(straight_cards) == 5:
                    # We sort the cards in ascending order
                    return sorted(straight_cards, key=lambda x: x.value, reverse=True) # MODIFIED
            elif card.value == last_card.value:
                continue
            else:
                straight_cards = [card]
        return False
        
    def is_flush(self, cards: list[Card]) -> bool:
        """Check if the cards in a list form a flush (all from the same suit)"""
        base_suit: CardSuits = cards[0].suit
        return all(card.suit == base_suit for card in cards)

    def get_best_pairs(self) -> list[list[Card]] | bool:
        """Return all group of cards that form a pair in the cards"""
        pairs: list[list[Card]] = [pair for pair in self.get_card_num_pairs().values() if len(pair) == 2]
        if pairs:
            return sorted(pairs, key=lambda pair: pair[0].value, reverse=True) # MODIFIED
        return False
    
    def get_best_pair(self) -> list[Card] | bool:
        """Return the best pair in the cards"""
        pairs: list[list[Card]] = self.get_best_pairs()
        if not pairs:
            return False
        return pairs[0]

    def get_best_two_pair(self) -> list[Card] | bool:
        """Return the two best pairs in the cards"""
        pairs: list[list[Card]] = self.get_best_pairs()
        if not pairs or len(pairs) < 2:
            return False
        
        # Sort pairs by the value of the cards in descending order
        pairs.sort(key=lambda pair: pair[0].value, reverse=True) # MODIFIED
        return pairs[:2]

    def get_best_three_of_a_kind(self) -> list[list[Card]] | bool:
        """Return the best three of a kind in the cards"""
        pairs: list[list[Card]] = [pair for pair in self.get_card_num_pairs().values() if len(pair) == 3]
        if not pairs:
            return False
        
        # Find the pair with the highest value
        best_pair = max(pairs, key=lambda pair: pair[0].value)
        return best_pair
        
    def get_best_four_of_a_kind(self) -> list[list[Card]] | bool:
        """Return the best four of a kind in the cards"""
        pairs: list[list[Card]] = [pair for pair in self.get_card_num_pairs().values() if len(pair) == 4]
        if not pairs:
            return False
        
        # Find the pair with the highest value
        best_pair = max(pairs, key=lambda pair: pair[0].value)
        return best_pair

    def get_best_straight(self) -> list[Card]:
        """Return the best straight (5 cards in a row) in the cards"""
        straight_cards: list[Card] = self.get_card_straight()
        if not straight_cards:
            return False
        return straight_cards[:5] # MODIFIED (-5:)

    def get_best_flush(self) -> dict[str: list[Card]] | bool:
        """Return the best flush (5 cards of the same suit) in the cards"""
        colors: dict[str: list[Card]] = self.get_card_suit_pairs()
        if not colors:
            return False
        for color, cards in colors.items():
            if len(cards) >= 5:
                return sorted(colors[color], key=lambda x: x.value, reverse=True)[:5] # MODIFIED
        return False

    def get_best_full_house(self) -> list[list[Card]] | bool:
        """Return the best full house in the cards"""
        best_pair: list[Card] = self.get_best_pair()
        best_three_of_a_kind: list[Card] = self.get_best_three_of_a_kind()
        if not (best_pair and best_three_of_a_kind):
            return False
        return best_three_of_a_kind + best_pair # MODIFIED

    def get_best_straight_flush(self) -> list[Card] | bool:
        """Return the best straight flush in the cards"""
        straight_cards: list[Card] = self.get_card_straight()
        if not straight_cards:
            return False
        straight_cards = sorted(straight_cards, key=lambda x: x.value, reverse=True)
        for i in range(len(straight_cards) - 4):
            cards_to_check: list[Card] = straight_cards[i:i+5]
            if self.is_flush(cards_to_check):
                return sorted(cards_to_check, key=lambda x: x.value, reverse=True) # MODIFIED
        return False

    def get_best_royal_flush(self) -> list[Card] | bool:
        """Return the best royal flush in the cards"""
        straight_flush_cards: list[Card] = self.get_best_straight_flush()
        if not straight_flush_cards:
            return False
        if list(map(lambda x: x.value, straight_flush_cards)) == [10, 11, 12, 13 ,14]:
            return sorted(straight_flush_cards, key=lambda x: x.value, reverse=True) # MODIFIED
        return False
    
    def get_final_combination(self) -> tuple[CardCombinations, list[Card]]:
        """Return the best combination of cards in the cards"""
        result = self.get_best_royal_flush()
        if result: return (CardCombinations.ROYAL_FLUSH, result)

        result = self.get_best_straight_flush()
        if result: return (CardCombinations.STRAIGHT_FLUSH, result)

        result = self.get_best_four_of_a_kind()
        if result: return (CardCombinations.FOUR_OF_A_KIND, result)

        result = self.get_best_full_house()
        if result: return (CardCombinations.FULL_HOUSE, result)

        result = self.get_best_flush()
        if result: return (CardCombinations.FLUSH, result)

        result = self.get_best_straight()
        if result: return (CardCombinations.STRAIGHT, result)

        result = self.get_best_three_of_a_kind()
        if result: return (CardCombinations.THREE_OF_A_KIND, result)

        result = self.get_best_two_pair()
        if result: return (CardCombinations.TWO_PAIR, result)

        result = self.get_best_pair()
        if result: return (CardCombinations.PAIR, result)

        result = sorted(self.cards, key=lambda x: x.value, reverse=True)
        return (CardCombinations.HIGH_CARD, result)
