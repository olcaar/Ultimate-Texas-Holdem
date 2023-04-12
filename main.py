from cards import *

deck = Deck()
for i in range(1000):
    deck.shuffle()
    hole_cards = deck.deal_two_cards_for_testing()
    board_cards = deck.deal_five_cards_for_testing()
    check = return_hand(hole_cards, board_cards)
    if check:
        print(check)

# test sort_by_rank function
cards = [('3', '♠'), ('4', '♠'), ('5', '♠'), ('2', '♠'), ('6', '♠'), ('7', '♠'), ('A', '♠')]
print(sort_by_rank(cards))

cards = deck.deal_seven_cards_for_testing()
cards = [('3', '♠'), ('4', '♠'), ('5', '♠'), ('2', '♠'), ('6', '♠'), ('7', '♠'), ('A', '♠')]
print(is_straight(cards))
# test is_flush
print('done')
