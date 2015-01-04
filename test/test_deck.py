#!/usr/bin/python

import os
import sys
file_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(file_path, './../'))

import pytest
import deck_of_cards.deck as deck
import deck_of_cards.card as card

import numpy
import itertools

def local_check_deck(d_deck):
    # another and different deck validation function
    # not as easily readable and a lot more concise
    # return True if deck is good

    # create a dictionary with all possible suits and ranks
    card_dict = dict((suit, dict((rank, 0) for rank in card.POSSIBLE_RANK)) for suit in card.POSSIBLE_SUIT)
    card_dict[card.JOKER_SUIT] = {card.JOKER_RANK: 0}

    # iterate through all cards in deck and count
    cards_iter = itertools.chain(d_deck._cards, d_deck._in_play_cards, d_deck._discarded_cards)
    for c_card in cards_iter:
        card_dict[c_card.get_suit()][c_card.get_rank()] += 1

    # check normal cards
    normal_cards_check = True
    for suit in card.POSSIBLE_SUIT:
        for occurences in card_dict[suit].itervalues():
            normal_cards_check = normal_cards_check and (occurences == 1)

    normal_cards_check = not any(any(occurences != 1 for occurences in card_dict[suit].itervalues()) for suit in card.POSSIBLE_SUIT)

    # check count of jokers
    number_of_jokers = 2 if d_deck._with_jokers else 0
    jokers_check = (number_of_jokers == card_dict[card.JOKER_SUIT][card.JOKER_RANK])

    return normal_cards_check and jokers_check

def assert_good_deck(d_deck):
    assert local_check_deck(d_deck)
    assert d_deck.check_deck()

def assert_bad_deck(d_deck):
    assert not local_check_deck(d_deck)
    assert not d_deck.check_deck()

def is_deck_ordered(d_deck):
    # deck cannot be ordered if cards have been dealt or discarded
    if d_deck._in_play_cards or d_deck._discarded_cards:
        return False

    # a new deck starts out ordered
    ordered_deck = deck.Deck(d_deck._with_jokers)

    # check length of _cards
    if len(ordered_deck._cards) != len(d_deck._cards):
        return False

    # check each card one by one using the same index
    for a_card, b_card in zip(ordered_deck._cards, d_deck._cards):
        if a_card != b_card:
            return False

    return True

def test_new_deck_is_good():
    for with_jokers in [True, False]:
        new_deck = deck.Deck(with_jokers)
        assert_good_deck(new_deck)

def test_dealing():
    new_deck = deck.Deck()

    while not new_deck.is_empty():
        dealt_card = new_deck.deal()
        assert_good_deck(new_deck)

    # raise IndexError when trying to deal from empty deck
    with pytest.raises(IndexError):
        new_deck.deal()

def test_discard_single_card():
    new_deck = deck.Deck()
    assert_good_deck(new_deck)

    for _ in xrange(3):
        dealt_card = new_deck.deal()
        assert_good_deck(new_deck)

        new_deck.discard(dealt_card)
        assert_good_deck(new_deck)

def test_discard_multiple_cards():
    new_deck = deck.Deck()
    assert_good_deck(new_deck)

    for _ in xrange(3):
        dealt_cards = []
        dealt_cards.append(new_deck.deal())
        dealt_cards.append(new_deck.deal())
        dealt_cards.append(new_deck.deal())
        assert_good_deck(new_deck)

        new_deck.discard(dealt_cards)
        assert_good_deck(new_deck)

def test_discard_jokers():
    new_deck = deck.Deck()
    new_deck._cards = []

    joker_1 = card.Card(card.JOKER_RANK, card.JOKER_SUIT)
    joker_2 = card.Card(card.JOKER_RANK, card.JOKER_SUIT)
    joker_3 = card.Card(card.JOKER_RANK, card.JOKER_SUIT)
    joker_4 = card.Card(card.JOKER_RANK, card.JOKER_SUIT)
    joker_5 = card.Card(card.JOKER_RANK, card.JOKER_SUIT)

    new_deck._in_play_cards = [joker_1, joker_2]
    assert len(new_deck._in_play_cards) == 2
    assert new_deck._in_play_cards[0] == joker_5
    assert new_deck._in_play_cards[1] == joker_5

    new_deck.discard(joker_3)
    assert len(new_deck._in_play_cards) == 1
    assert new_deck._in_play_cards[0] == joker_5

    new_deck.discard(joker_4)
    assert len(new_deck._in_play_cards) == 0

def test_invalid_discard():
    new_deck = deck.Deck(with_jokers=True)
    assert len(new_deck._in_play_cards) == 0

    joker = card.Card(card.JOKER_RANK, card.JOKER_SUIT)

    with pytest.raises(ValueError):
        new_deck.discard(joker)

def test_new_deck_is_ordered():
    new_deck = deck.Deck()
    assert is_deck_ordered(new_deck)

def test_new_deck_is_not_ordered_after_shuffle():
    new_deck = deck.Deck()
    new_deck.shuffle()
    assert not is_deck_ordered(new_deck)

def test_new_deck_is_not_ordered_after_a_deal():
    new_deck = deck.Deck()
    new_deck.deal()
    assert not is_deck_ordered(new_deck)

def test_bad_deck_when_missing_card():
    new_deck = deck.Deck()
    new_deck._cards.pop()
    assert_bad_deck(new_deck)

def test_bad_deck_when_missing_single_joker():
    new_deck = deck.Deck(with_jokers=True)
    joker = card.Card(card.JOKER_RANK, card.JOKER_SUIT)
    new_deck._cards.remove(joker)
    assert_bad_deck(new_deck)

def test_bad_deck_when_missing_both_joker():
    new_deck = deck.Deck(with_jokers=True)
    joker = card.Card(card.JOKER_RANK, card.JOKER_SUIT)
    new_deck._cards.remove(joker)
    new_deck._cards.remove(joker)
    assert_bad_deck(new_deck)

def test_bad_deck_when_missing_cards():
    new_deck = deck.Deck()
    new_deck._cards.pop()
    new_deck._cards.pop()
    new_deck._cards.pop()
    assert_bad_deck(new_deck)

def _get_random_index(high):
    return numpy.random.randint(high)

def _deepcopy(c_card):
    return card.Card(c_card.get_rank(), c_card.get_suit())

def test_bad_deck_single_repeated_card():
    new_deck = deck.Deck()

    # find card to copy
    random_card_index = _get_random_index(len(new_deck._cards))
    chosen_card = new_deck._cards[random_card_index]
    copied_chosen_card = _deepcopy(chosen_card)

    # find another card index different that the first
    new_random_card_index = random_card_index
    while random_card_index == new_random_card_index:
        new_random_card_index = _get_random_index(len(new_deck._cards))

    # good deck before copy
    # bad deck after copy
    assert_good_deck(new_deck)
    new_deck._cards[new_random_card_index] = copied_chosen_card
    assert_bad_deck(new_deck)

def test_bad_deck_double_repeated_card():
    new_deck = deck.Deck()

    # find card to copy
    # create 2 copies
    random_card_index = _get_random_index(len(new_deck._cards))
    chosen_card = new_deck._cards[random_card_index]
    copied_chosen_card = _deepcopy(chosen_card)
    copied_chosen_2_card = _deepcopy(chosen_card)

    # find another card index different that the first
    new_random_card_index = random_card_index
    while random_card_index == new_random_card_index:
        new_random_card_index = _get_random_index(len(new_deck._cards))

    # find another card index different from the first 2 indexes
    new_random_card_2_index = random_card_index
    while (random_card_index == new_random_card_2_index) or (new_random_card_index == new_random_card_2_index):
        new_random_card_2_index = _get_random_index(len(new_deck._cards))

    # good deck before copy
    # bad deck after copy
    assert_good_deck(new_deck)
    new_deck._cards[new_random_card_index] = copied_chosen_card
    new_deck._cards[new_random_card_2_index] = copied_chosen_2_card
    assert_bad_deck(new_deck)

def test_bad_deck_three_jokers():
    new_deck = deck.Deck(with_jokers=True)
    joker = card.Card(card.JOKER_RANK, card.JOKER_SUIT)

    random_card_index = _get_random_index(len(new_deck._cards))
    while new_deck._cards[random_card_index].is_joker():
        random_card_index = _get_random_index(len(new_deck._cards))

    assert_good_deck(new_deck)
    new_deck._cards[random_card_index] = joker
    assert_bad_deck(new_deck)

def test_deck_simple_repr():
    new_deck = deck.Deck(with_jokers=True)
    joker = card.Card(card.JOKER_RANK, card.JOKER_SUIT)
    ace_of_hearts = card.Card(1, 'hearts')
    king_of_spades = card.Card(13, 'spades')
    new_deck._cards = [joker]
    new_deck._discarded_cards = [ace_of_hearts]
    new_deck._in_play_cards = [king_of_spades]

    new_deck_repr = "Deck(_cards=[%s], _discarded_cards=[%s], _in_play_cards=[%s])" % (repr(joker), repr(ace_of_hearts), repr(king_of_spades))
    assert new_deck_repr == repr(new_deck)

def test_deck_simple_empty_repr():
    new_deck = deck.Deck()
    new_deck._cards = []
    new_deck._discarded_cards = []
    new_deck._in_play_cards = []

    new_deck_repr = "Deck(_cards=[], _discarded_cards=[], _in_play_cards=[])"
    assert new_deck_repr == repr(new_deck)

def test_deck_simple_str():
    new_deck = deck.Deck(with_jokers=True)
    joker = card.Card(card.JOKER_RANK, card.JOKER_SUIT)
    ace_of_hearts = card.Card(1, 'hearts')
    king_of_spades = card.Card(13, 'spades')
    new_deck._cards = [joker]
    new_deck._discarded_cards = [ace_of_hearts]
    new_deck._in_play_cards = [king_of_spades]

    new_deck_str = "Deck(\n\t_cards : [%s],\n\t_discarded_cards : [%s],\n\t_in_play_cards : [%s]\n)" % (str(joker), str(ace_of_hearts), str(king_of_spades))
    assert new_deck_str == str(new_deck)

def test_deck_simple_empty_str():
    new_deck = deck.Deck()
    new_deck._cards = []
    new_deck._discarded_cards = []
    new_deck._in_play_cards = []

    new_deck_str = "Deck(\n\t_cards : [],\n\t_discarded_cards : [],\n\t_in_play_cards : []\n)"
    assert new_deck_str == str(new_deck)
