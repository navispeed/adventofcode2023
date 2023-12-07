import abc
from collections import defaultdict
from typing import Iterator, Iterable

POWER_RANK = "AKQT98765432J"


class Pattern(abc.ABC):
    def __init__(self, row: str, bonus: int):
        self._bonus = bonus
        self._row = row
        self._char_count = defaultdict(int)
        for c in self._row:
            self._char_count[c] += 1

    @abc.abstractmethod
    def __bool__(self):
        pass

    def get_power(self, bonus: bool = True) -> int:
        power = 0
        for c in self._row:
            power *= 100
            power += len(POWER_RANK) - POWER_RANK.find(c)
        if bonus:
            return power + self._bonus
        return power

    def __str__(self):
        return f"{self.__class__.__name__} : {self._row} (valid: {bool(self)}) -> {self.get_power()}"

    def __lt__(self, other: "Pattern"):
        if self._bonus < other._bonus:
            return True
        if self._bonus > other._bonus:
            return False
        return self.get_power(False) < other.get_power(False)


class FiveOfAKind(Pattern):
    """
    Five of a kind, where all five cards have the same label: AAAAA
    """

    def __init__(self, row: str):
        super().__init__(row, 6000)

    def __bool__(self):
        return len(self._char_count) == 1


class FourOfAKind(Pattern):
    """
    Four of a kind, where four cards have the same label and one card has a different label: AA8AA
    """

    def __init__(self, row: str):
        super().__init__(row, 5000)

    def __bool__(self):
        return len(self._char_count) == 2 and (
                1 in self._char_count.values() and 4 in self._char_count.values()
        )


class FullHouse(Pattern):
    """
    Full house, where three cards have the same label, and the remaining two cards share a different label: 23332
    """

    def __init__(self, row: str):
        super().__init__(row, 4000)

    def __bool__(self):
        return len(self._char_count) == 2 and (
                2 in self._char_count.values() and 3 in self._char_count.values()
        )


class ThreeOfAKind(Pattern):
    """
    Three of a kind, where three cards have the same label, and the remaining two cards are each different from any other card in the hand: TTT98
    """

    def __init__(self, row: str):
        super().__init__(row, 3000)

    def __bool__(self):
        return (
                3 in self._char_count.values() and 1 in self._char_count.values()
        )


class TwoPair(Pattern):
    """
    Two pair, where two cards share one label, two other cards share a second label,
     and the remaining card has a third label: 23432
    """

    def __init__(self, row: str):
        super().__init__(row, 2000)

    def __bool__(self):
        return [1, 2, 2] == list(sorted(self._char_count.values()))


class OnePair(Pattern):
    """
    One pair, where two cards share one label, and the other three cards have a different label from the pair and each other: A23A4
    """

    def __init__(self, row: str):
        super().__init__(row, 1000)

    def __bool__(self):
        return [1, 1, 1, 2] == list(sorted(self._char_count.values()))


class HighCard(Pattern):
    """
    High card
    """

    def __init__(self, row: str):
        super().__init__(row, 0)

    def __bool__(self):
        return [1, 1, 1, 1, 1] == list(self._char_count.values())


def build(hand: str) -> Pattern:
    return next(
        filter(None, [FiveOfAKind(hand), FourOfAKind(hand), FullHouse(hand), ThreeOfAKind(hand),
                      TwoPair(hand), OnePair(hand), HighCard(hand)]))


def handle_joker(hand: str, level: int = 0):
    if "J" not in hand:
        return build(hand)

    if ("J" * len(hand)) == hand:
        return build(hand)

    def best(iterator: Iterable[Pattern]):
        for it in iterator:
            return it

    def generate_all():
        for idx, c in enumerate(hand):
            if c == "J":
                for possible in POWER_RANK[0:len(POWER_RANK) - 1]:
                    new_hand = f"{hand[0:idx]}{possible}{hand[min(idx + 1, len(hand)):]}"
                    yield handle_joker(new_hand, level + 1)

    return best(sorted(generate_all(), reverse=True)).__class__(hand)  # type :ignore


assert (all([FiveOfAKind("AAAAA"), FourOfAKind("AA8AA"), ThreeOfAKind("TTT98"), TwoPair("23432"),
             OnePair("A23A4"), HighCard("23456")]))

assert (FiveOfAKind("AAAAA").get_power()) > FiveOfAKind("KKKKK").get_power()

assert isinstance(build("AAAAA"), FiveOfAKind)
assert isinstance(build("23456"), HighCard)
