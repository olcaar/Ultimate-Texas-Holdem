from cards import *
import time

# count time to run
start = time.time()
statistics = {'High Card': 0, 'Pair': 0, 'Two Pair': 0, 'Three of a Kind': 0, 'Straight': 0, 'Flush': 0,
              'Full House': 0, 'Four of a Kind': 0, 'Straight Flush': 0, 'Royal Flush': 0}
deck = Deck()
num_of_hands = 1
# for i in range(num_of_hands):
#     deck.shuffle()
#     hole_cards = deck.deal_two_cards_for_testing()
#     dealer_hand = deck.deal_two_cards_for_testing()
#     board_cards = deck.deal_five_cards_for_testing()
#     check = return_hand(hole_cards, board_cards)
#     if check[0] == 'High Card':
#         statistics['High Card'] += 1
#     elif check[0] == 'Pair':
#         statistics['Pair'] += 1
#     elif check[0] == 'Two Pair':
#         statistics['Two Pair'] += 1
#     elif check[0] == 'Three of a Kind':
#         statistics['Three of a Kind'] += 1
#     elif check[0] == 'Straight':
#         statistics['Straight'] += 1
#     elif check[0] == 'Flush':
#         statistics['Flush'] += 1
#     elif check[0] == 'Full House':
#         statistics['Full House'] += 1
#     elif check[0] == 'Four of a Kind':
#         statistics['Four of a Kind'] += 1
#     elif check[0] == 'Straight Flush':
#         statistics['Straight Flush'] += 1
#     elif check[0] == 'Royal Flush':
#         statistics['Royal Flush'] += 1
#     print(f'hole cards: {hole_cards}')
#     print(f'dealer hand: {dealer_hand}')
#     print(f'board cards: {board_cards}')
#     print(check_winner(hole_cards, dealer_hand, board_cards))

game = Game()
game.start_game()


# # print the percentage of each hand
# for key, value in statistics.items():
#     print(f'{key}: {value / num_of_hands * 100}%')
print(f'time to run: {time.time() - start}')
print('done')
