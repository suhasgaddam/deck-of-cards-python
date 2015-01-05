deck-of-cards-python
================

A Python Implementation Of A Deck of Cards

[![Documentation Status](https://readthedocs.org/projects/deck-of-cards-python/badge/?version=latest)](http://deck-of-cards-python.readthedocs.org/en/latest/)

Example Usage
```python
import deck_of_cards.deck as deck
import deck_of_cards.card as card

joker = card.Card(card.JOKER_RANK, card.JOKER_SUIT)
ace_of_spades = card.Card(1, 'spades')
print joker
print ace_of_spades

new_deck = deck.Deck(with_jokers=True)
new_deck.shuffle()
while not new_deck.is_empty():
    c_card = new_deck.deal()
    print c_card
    new_deck.discard(c_card)
```

Tests require pytest and numpy.

Test Usage when in deck-of-cards-python folder

```python
py.test
```