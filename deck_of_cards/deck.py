#!/usr/bin/python
"""This module provides the :class:`Deck` object
"""

import deck_of_cards.card as card
import random
import logging

#: a logger object
LOGGER = logging.getLogger(__name__)

class Deck(object):
    """A Deck object

    A new deck starts out ordered.

    If jokers are included, contains (2 + 4 * 13) :class:`deck_of_cards.card.Card` objects

    If no jokers are included, contains (4 * 13) :class:`deck_of_cards.card.Card` objects
    """

    #: a boolean to represent if jokers exist in deck
    _with_jokers = True

    #: an array of unused :class:`deck_of_cards.card.Card` objects that are
    #: waiting to be dealt
    _cards = []

    #: an array of discarded :class:`deck_of_cards.card.Card` objects
    _discarded_cards = []

    #: an array of :class:`deck_of_cards.card.Card` objects that have been dealt
    _in_play_cards = []

    def __init__(self, with_jokers=True):
        """
        :param bool with_jokers: include jokers if True
        """
        LOGGER.debug("Creating a new deck (with_jokers:%s)", with_jokers)

        self._with_jokers = with_jokers
        self._cards = []
        self._discarded_cards = []
        self._in_play_cards = []

        # add jokers if necessary
        if with_jokers:
            for _ in xrange(2):
                self._cards.append(card.Card(card.JOKER_RANK, card.JOKER_SUIT))

        for suit in card.POSSIBLE_SUIT:
            for rank in card.POSSIBLE_RANK:
                self._cards.append(card.Card(rank, suit))

    def __repr__(self):
        """
        :returns: unambigious string represenation of deck object
        :rtype: str
        """
        card_arrays_dict = {
            '_cards' : self._cards,
            '_discarded_cards' : self._discarded_cards,
            '_in_play_cards' : self._in_play_cards,
        }

        repr_str = 'Deck('

        for card_array_str, card_array in card_arrays_dict.iteritems():
            repr_str += "%s=[" % card_array_str
            if card_array:
                for c_card in card_array:
                    repr_str += repr(c_card) + ', '
                repr_str = repr_str[:-2]
            repr_str += '], '

        repr_str = repr_str[:-2] + ')'

        return repr_str

    def __str__(self):
        """
        :returns: human readable string represenation of deck object
        :rtype: str
        """
        card_arrays_dict = {
            '_cards' : self._cards,
            '_discarded_cards' : self._discarded_cards,
            '_in_play_cards' : self._in_play_cards,
        }

        str_str = "Deck(\n\t"

        for card_array_str, card_array in card_arrays_dict.iteritems():
            str_str += "%s : [" % card_array_str
            if card_array:
                for c_card in card_array:
                    str_str += str(c_card) + ', '
                str_str = str_str[:-2]
            str_str += '],\n\t'

        str_str = str_str[:-3] + "\n)"

        return str_str

    def shuffle(self):
        """Shuffle the unused set of cards in :attr:`_cards`
        """
        LOGGER.debug("Shuffling deck")
        random.shuffle(self._cards)

    def deal(self):
        """Deals a single :class:`deck_of_cards.card.Card` from :attr:`_cards`

        Raises an IndexError when :attr:`_cards` is empty

        :returns: a single :class:`deck_of_cards.card.Card`
        :rtype: :class:`deck_of_cards.card.Card`
        :raises: IndexError
        """
        LOGGER.debug("Number of cards left : %d", len(self._cards))

        try:
            # deal the last card from the unused _cards array
            deal_card = self._cards.pop()
        except IndexError:
            raise IndexError('Trying to deal from an empty deck.')

        # add the newly dealt card to the _in_play_cards array
        self._in_play_cards.append(deal_card)

        LOGGER.info("Dealing : %s", deal_card)
        return deal_card

    def discard(self, cards):
        """Remove `cards` from the :attr:`_in_play_cards` array and add them to
        :attr:`_discarded_cards` array

        Raises a ValueError when trying to discard a card that does not exist in
        :attr:`_in_play_cards`.

        :param array cards: an array of :class:`deck_of_cards.card.Card` objects
                            or a single :class:`deck_of_cards.card.Card`
        :raises: ValueError
        """
        if not isinstance(cards, list):
            cards = [cards]

        for discard_card in cards:
            try:
                self._in_play_cards.remove(discard_card)
                LOGGER.info("Discarding %s", discard_card)
            except ValueError:
                raise ValueError("%s not found in self._in_play_cards" % discard_card)
            self._discarded_cards.append(discard_card)

    def is_empty(self):
        """This method returns true if the deck(:attr:`_cards`) is empty

        :returns: True if deck is empty
        :rtype: bool
        """
        return not self._cards

    def check_deck(self):
        """Check to make sure all the cards are accounted

        :returns: True if all cards are accounted
        :rtype: bool
        """

        # start with a simple card count check
        total_possible_cards = (13*4) + (2 if self._with_jokers else 0)
        if total_possible_cards != (len(self._cards)
                                    + len(self._in_play_cards)
                                    + len(self._discarded_cards)):
            return False

        return_value = True

        # go through all piles of cards and create a dictionary with
        # [suit][rank] = number of occurrences of card
        card_dict = {}
        for pile in [self._cards, self._in_play_cards, self._discarded_cards]:
            for c_card in pile:
                suit = c_card.get_suit()
                rank = c_card.get_rank()

                if not suit in card_dict:
                    card_dict[suit] = {}

                if not rank in card_dict[suit]:
                    card_dict[suit][rank] = 1
                else:
                    card_dict[suit][rank] += 1

        # go through generated card_dictionary to make sure that there are the
        # appropriate rank of occurrences for each card
        for suit in card_dict.keys():
            for rank in card_dict[suit].keys():
                if 2 == card_dict[suit][rank]:
                    # check for 2 jokers
                    if not (card.JOKER_SUIT == suit and card.JOKER_RANK == rank):
                        return_value = False
                elif 1 != card_dict[suit][rank]:
                    LOGGER.info("Something is wrong with the %s", card.Card(rank, suit))
                    return_value = False

        return return_value
