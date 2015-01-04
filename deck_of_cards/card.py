#!/usr/bin/python
"""This module provides the :class:`Card` object.
This module also has 5 constant attributes that help validate or string format
the :class:`Card` object: :attr:`POSSIBLE_SUIT`, :attr:`POSSIBLE_RANK`,
, :attr:`JOKER_SUIT`, :attr:`JOKER_RANK`, and :attr:`RANK_TRANSLATION`
"""

#: an array with all the possible suit strings
POSSIBLE_SUIT = ['hearts', 'diamonds', 'spades', 'clubs']

#: an array with the possible ranks
POSSIBLE_RANK = range(1, 14, 1)

#: a string representing the Joker's suit
JOKER_SUIT = 'joker'

#: a number representing the Joker's rank
JOKER_RANK = 0

#: a dictionary which translates the special face cards to strings
RANK_TRANSLATION = {
    1  : 'ace',
    11 : 'jack',
    12 : 'queen',
    13 : 'king',
}

class Card(object):
    """A Card object
    """

    #: Holds the suit as a lowercase string
    _suit = None

    #: Holds an integer which represents the card rank
    _rank = None

    def __init__(self, rank, suit):
        """
        :param int rank: a rank in :attr:`POSSIBLE_RANK` or :attr:`JOKER_RANK`
        :param str suit: a case-independent string in :attr:`POSSIBLE_SUIT` or
                         :attr:`JOKER_SUIT`
        :raises: ValueError
        """

        # convert to lowercase
        suit = suit.lower()

        base_error_str = 'A new Card cannot be created.'

        if suit == JOKER_SUIT:
            if rank == JOKER_RANK:
                self._suit = suit
                self._rank = rank
            else:
                raise ValueError(base_error_str + " Joker's rank must be %d"
                                 % JOKER_RANK)
        elif suit in POSSIBLE_SUIT:
            self._suit = suit

            if rank in POSSIBLE_RANK:
                self._rank = rank
            else:
                raise ValueError(base_error_str + " A normal card's rank (%s)"
                                 " is not %s." % (rank, POSSIBLE_RANK))
        else:
            raise ValueError(base_error_str + " Suit ('%s') is not in"
                             " %s." % (suit, POSSIBLE_SUIT + [JOKER_SUIT]))

    def _translate_rank(self):
        """This is a hidden method that changes the card rank to a
        human-readable string. It also returns the title case of the string if
        possible.

        'Ace' for 1
        'Joker' for joker

        :returns: human-readable string for face cards or card rank
        :rtype: str
        """
        if self.is_joker():
            return JOKER_SUIT.title()
        elif self.get_rank() in RANK_TRANSLATION:
            return RANK_TRANSLATION[self.get_rank()].title()
        else:
            return self.get_rank()

    def __repr__(self):
        """This method returns an unambigious string representation of the card object

        :returns: unambigious string represenation of card object
        :rtype: str
        """
        return "Card(_rank=%s, _suit=%s)" % (self.get_rank(), self.get_suit())

    def __str__(self):
        """This method returns a nice string representation of the card object

        useful in printing card object as "%s"

        :returns: human readable string represenation of card object
        :rtype: str
        """
        translated_rank = self._translate_rank()
        if self.is_joker():
            return translated_rank
        else:
            return "%s of %s" % (translated_rank, self._suit.title())

    def get_rank(self):
        """
        :returns: :attr:`_rank`
        :rtype: int
        """
        return self._rank

    def get_suit(self):
        """
        :returns: :attr:`_suit`
        :rtype: str
        """
        return self._suit

    def is_joker(self):
        """
        :returns: True if joker
        :rtype: bool
        """
        return (JOKER_RANK == self.get_rank()) and (JOKER_SUIT == self.get_suit())
