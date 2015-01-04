#!/usr/bin/python

import os
import sys
file_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(file_path, './../'))

import pytest
import deck_of_cards.card as card

import numpy
import string

def _assert_card(rank, suit):
    # all assertions to prove the card is good
    new_card = card.Card(rank, suit)

    # create human readable rank string
    if 0 == rank:
        rank_string = 'Joker'
    elif 1 == rank:
        rank_string = 'Ace'
    elif 11 == rank:
        rank_string = 'Jack'
    elif 12 == rank:
        rank_string = 'Queen'
    elif 13 == rank:
        rank_string = 'King'
    else:
        rank_string = rank

    # assert rank and suit
    assert rank == new_card.get_rank()
    assert suit.lower() == new_card.get_suit()

    # create card str
    # assert to check for joker
    new_card_str = "%s of %s" % (rank_string, suit.title())
    if 'joker' == suit.lower():
        new_card_str = suit.title()
        assert new_card.is_joker()
    else:
        assert False == new_card.is_joker()

    # assert card str and repr
    assert new_card_str == str(new_card)

    new_card_repr = "Card(_rank=%s, _suit=%s)" % (rank, suit.lower())
    assert new_card_repr == repr(new_card)

def test_normal_cards():
    for suit in ('hearts', 'diamonds', 'spades', 'clubs'):
        for rank in xrange(1, 14):
            _assert_card(rank, suit)

def test_normal_cards_case_insensitive():
    for suit in ('hearts', 'diamonds', 'spades', 'clubs'):
        suit = suit.upper()
        rank = 1
        _assert_card(rank, suit)

def test_normal_cards_invalid_rank():
    # get random rank in [-50, 50] and ignore [1, 13]
    # do this a random number of times in range [0, 50]
    for rank in numpy.random.randint(-50, 50, numpy.random.randint(50)):
        if (rank >= 1) and (rank <= 13):
            continue
        with pytest.raises(ValueError):
            new_card = card.Card(rank, 'hearts')

def test_normal_cards_invalid_suit():
    def _random_suit(length=5):
        # create a random string/suit
        return ''.join(numpy.random.choice(string.letters) for i in range(length))

    # test random suit
    # do this a random number of times in range [0, 50]
    for i in xrange(numpy.random.randint(50)):
        with pytest.raises(ValueError):
            new_card = card.Card(numpy.random.randint(14), _random_suit())

    # closely matching but still invalid suits
    for suit in ('HEARTSS', 'DIAMOONNDSA', 'SSPADDES', 'CCLLUUBBSS'):
        with pytest.raises(ValueError):
            new_card = card.Card(numpy.random.randint(14), suit)

def test_joker():
    rank = 0
    suit = 'joker'
    _assert_card(rank, suit)

def test_joker_case_insensitive():
    rank = 0
    suit = 'joker'.upper()
    _assert_card(rank, suit)

def test_joker_invalid_rank():
    # joker is only valid with appropriate rank
    for rank in xrange(1, 14, 1):
        with pytest.raises(ValueError):
            new_card = card.Card(rank, 'joker')

def test_equality():
    joker_1 = card.Card(card.JOKER_RANK, card.JOKER_SUIT)
    joker_2 = card.Card(card.JOKER_RANK, card.JOKER_SUIT)
    assert joker_1 == joker_2

    ace_of_spades_1 = card.Card(1, 'spades')
    ace_of_spades_2 = card.Card(1, 'spades')
    assert ace_of_spades_1 == ace_of_spades_2

def test_ineqality():
    ace_of_spades = card.Card(1, 'spades')
    ace_of_clubs = card.Card(1, 'clubs')
    assert ace_of_spades != ace_of_clubs
