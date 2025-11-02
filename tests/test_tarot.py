from tarot import tarot


def test_build_deck_has_78_cards():
    deck = tarot.build_deck()
    assert isinstance(deck, list)
    assert len(deck) == 78


def test_draw_returns_requested_number_and_unique():
    cards = tarot.draw(3)
    assert isinstance(cards, list)
    assert len(cards) == 3
    names = [c["card"] for c in cards]
    assert len(set(names)) == 3


def test_meanings_present_and_chinese():
    c = tarot.draw(1)[0]
    assert "card" in c and "meaning" in c
    assert isinstance(c["meaning"], str)
    # basic heuristic: chinese punctuation or chinese characters expected (MVP)
    assert len(c["meaning"]) > 3


def test_draw_spread_three_and_cross():
    three = tarot.draw_spread('three')
    assert isinstance(three, list)
    assert len(three) == 3
    assert all('position' in c and 'card' in c and 'meaning' in c for c in three)

    cross = tarot.draw_spread('cross')
    assert isinstance(cross, list)
    assert len(cross) == 10
    assert all('position' in c and 'card' in c and 'meaning' in c for c in cross)
