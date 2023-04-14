import os
import random

# Define the deck of cards
import time

suits = ['♠️', '♥️', '♦️', '♣️']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

# List of all possible straights
straights = [['A', 'K', 'Q', 'J', '10'], ['K', 'Q', 'J', '10', '9'], ['Q', 'J', '10', '9', '8'],
             ['J', '10', '9', '8', '7'], ['10', '9', '8', '7', '6'], ['9', '8', '7', '6', '5'],
             ['8', '7', '6', '5', '4'], ['7', '6', '5', '4', '3'], ['6', '5', '4', '3', '2'],
             ['5', '4', '3', '2', 'A']]

# Define the possible hands in Texas Hold'em
hands = ['High Card', 'Pair', 'Two Pair', 'Three of a Kind', 'Straight', 'Flush', 'Full House', 'Four of a Kind',
         'Straight Flush', 'Royal Flush']
# enumerate the hands
hand_values = {hand: value for value, hand in enumerate(hands)}


class Deck:
    def __init__(self):
        self.cards = []
        for rank in ranks:
            for suit in suits:
                self.cards.append((rank, suit))
        random.shuffle(self.cards)

    def deal(self):
        return self.cards.pop()

    def shuffle(self):
        self.__init__()

    def deal_two_cards(self):
        return [self.cards.pop() for i in range(2)]

    def deal_seven_cards_for_testing(self):
        return [self.cards.pop() for i in range(7)]

    def deal_three_cards(self):
        return [self.cards.pop() for i in range(3)]

    def deal_five_cards(self):
        return [self.cards.pop() for i in range(5)]


class PlayerBalance:
    def __init__(self, balance):
        self.balance = balance

    def add_funds(self, amount):
        self.balance += amount

    def remove_funds(self, amount):
        self.balance -= amount

    def get_balance(self):
        return self.balance


class Bets:
    def __init__(self):
        self.ante = 0
        self.blind = 0
        self.trips = 0
        self.play = 0

    def bet(self, ante, trips):
        self.ante = ante
        self.blind = ante
        self.trips = trips

    def add_play(self, amount):
        self.play += amount

    def get_bets(self):
        # return all bets as a list
        return [self.ante, self.blind, self.trips, self.play]


class PlayerCards:
    def __init__(self, deck):
        self.hand = [deck.deal(), deck.deal()]

    def get_hand(self):
        return self.hand


class DealerCards:
    def __init__(self, deck):
        self.hand = [deck.deal(), deck.deal()]

    def get_hand(self):
        return self.hand


class BoardCards:
    def __init__(self):
        self.board = []

    def deal_flop(self, deck):
        self.board.append(deck.deal())
        self.board.append(deck.deal())
        self.board.append(deck.deal())

    def deal_turn_and_river(self, deck):
        self.board.append(deck.deal())
        self.board.append(deck.deal())

    def get_board(self):
        return self.board


# Get 2 Hole cards and 5 board cards and return the best 5 card hand made from all 7 cards.

def return_hand(hole_cards, board):
    # get all 7 cards
    all_cards = hole_cards + board

    # Check for Flush
    flush = is_flush(all_cards)

    # Check for Straight Flush only from the suited cards
    if flush[0]:
        straight_flush = is_straight([card for card in all_cards if card[1] == flush[1]])
        if straight_flush[0]:
            # Check for Royal Flush
            if 'A' in [card[0] for card in straight_flush[1]] and 'K' in [card[0] for card in straight_flush[1]]:
                # Return Royal Flush and the 5 cards that make it
                return hands[9], straight_flush[1]
            # Return Straight Flush and the 5 cards that make it
            return hands[8], straight_flush[1]
    # Check for Four of a Kind
    four_of_a_kind = is_four_of_a_kind(all_cards)
    if four_of_a_kind[0]:
        # Return Four of a Kind and the 5 cards that make it
        return hands[7], four_of_a_kind[1]
    # Check for Full House
    full_house = is_full_house(all_cards)
    if full_house[0]:
        # Return Full House and the 5 cards that make it
        return hands[6], full_house[1]
    # Check for Flush
    if flush[0]:
        # Return Flush and the 5 cards that make it
        return hands[5], flush[1]
    # Check for Straight
    straight = is_straight(all_cards)
    if straight[0]:
        # Return Straight and the 5 cards that make it
        return hands[4], straight[1]
    # Check for Three of a Kind
    three_of_a_kind = is_three_of_a_kind(all_cards)
    if three_of_a_kind[0]:
        # Return Three of a Kind and the 5 cards that make it
        return hands[3], three_of_a_kind[1]
    # Check for Two Pair
    two_pair = is_two_pair(all_cards)
    if two_pair[0]:
        # Return Two Pair and the 5 cards that make it
        return hands[2], two_pair[1]
    # Check for Pair
    pair = is_pair(all_cards)
    if pair[0]:
        # Return Pair and the 5 cards that make it
        return hands[1], pair[1]
    # Return High Card and the 5 highest cards
    return hands[0], sort_by_rank(all_cards)[:5]


# Get 7 cards and return True if there is a flush
def is_flush(cards):
    # Sort cards
    cards = sort_by_rank(cards)
    suit_hist = {}
    for card in cards:
        if card[1] in suit_hist:
            suit_hist[card[1]] += 1
        else:
            suit_hist[card[1]] = 1
    for suit in suit_hist:
        if suit_hist[suit] >= 5:
            # Get the 5 cards that make the flush
            flush = [card for card in cards if card[1] == suit]
            # Get the 5 highest cards in the flush
            flush = flush[:5]
            return True, flush
    return False, cards


# Check for straight
def is_straight(cards):
    # Sort cards
    cards = sort_by_rank(cards)
    # Get all ranks
    ranks = [card[0] for card in cards]
    # Check for straight
    for straight in straights:
        if all(rank in ranks for rank in straight):
            #  Get the 5 cards that make the straight
            straight = [card for card in cards if card[0] in straight]
            # Remove card if it has the same rank as another in the straight
            for card in straight:
                if ranks.count(card[0]) > 1:
                    straight.remove(card)
                    ranks.remove(card[0])
            if straight[4][0] == '2' and straight[0][0] == 'A':
                # Move ace to the end of the list
                straight = straight[1:] + [straight[0]]
            return True, straight
    return False, straight


# Check for four of a kind
def is_four_of_a_kind(cards):
    # Get all ranks
    ranks = [card[0] for card in cards]
    # Check for four of a kind
    for rank in ranks:
        if ranks.count(rank) == 4:
            # Get the 4 cards that make the four of a kind
            four_of_a_kind = [card for card in cards if card[0] == rank]
            # Get the remaining cards
            kicker = [card for card in cards if card[0] != rank]
            kicker = sort_by_rank(kicker)
            # get the last card in the list
            kicker = kicker[0]

            # Return four of a kind and the 5 cards that make it
            return True, four_of_a_kind + [kicker]
    return False, cards


# Create sort function for sorting cards by rank descending order
def sort_by_rank(cards):
    # sort list of cards by rank
    return sorted(cards, key=lambda x: ranks.index(x[0]), reverse=True)


def is_full_house(cards):
    # Sort cards by rank
    cards = sort_by_rank(cards)
    # Get all ranks
    ranks = [card[0] for card in cards]
    # Check for three of a kind
    for rank in ranks:
        if ranks.count(rank) == 3:
            # Get the 3 cards that make the three of a kind
            three_of_a_kind = [card for card in cards if card[0] == rank]
            # Get the remaining cards
            remaining_cards = [card for card in cards if card[0] != rank]
            # Get all ranks
            ranks = [card[0] for card in remaining_cards]
            # Check for pair
            for rank in ranks:
                if ranks.count(rank) >= 2:
                    if ranks.count(rank) == 3:
                        # Get only 2 cards from the 3 that make the three of a kind
                        pair = [card for card in remaining_cards if card[0] == rank][0:2]
                    else:
                        # Get the 2 cards that make the pair
                        pair = [card for card in remaining_cards if card[0] == rank]
                    # Return full house and the 5 cards that make it
                    return True, three_of_a_kind + pair
    return False, cards


def is_three_of_a_kind(cards):
    # Sort cards by rank
    cards = sort_by_rank(cards)
    # Get all ranks
    ranks = [card[0] for card in cards]
    # Check for three of a kind
    for rank in ranks:
        if ranks.count(rank) == 3:
            # Get the 3 cards that make the three of a kind
            three_of_a_kind = [card for card in cards if card[0] == rank]
            # Get the remaining cards
            remaining_cards = [card for card in cards if card[0] != rank]
            # Get other 2 highest cards
            remaining_cards = sort_by_rank(remaining_cards)
            remaining_cards = remaining_cards[0:2]
            # Return three of a kind and the 5 cards that make it
            return True, three_of_a_kind + remaining_cards
    return False, cards


def is_two_pair(cards):
    # sort cards by rank
    cards = sort_by_rank(cards)
    # Get all ranks
    ranks = [card[0] for card in cards]
    # Check for two pairs
    for rank in ranks:
        if ranks.count(rank) == 2:
            # Get the 2 cards that make the pair
            pair = [card for card in cards if card[0] == rank]
            # Get the remaining cards
            remaining_cards = [card for card in cards if card[0] != rank]
            # Get all ranks
            ranks = [card[0] for card in remaining_cards]
            # Check for second pair
            for rank in ranks:
                if ranks.count(rank) == 2:
                    # Get the 2 cards that make the second pair
                    second_pair = [card for card in remaining_cards if card[0] == rank]
                    # Get the remaining card
                    remaining_cards = [card for card in remaining_cards if card[0] != rank]
                    remaining_cards = sort_by_rank(remaining_cards)
                    remaining_cards = remaining_cards[0]
                    # Return two pair and the 5 cards that make it
                    return True, pair + second_pair + [remaining_cards]
    return False, cards


def is_pair(cards):
    # Sort cards by rank
    cards = sort_by_rank(cards)
    # Get all ranks
    ranks = [card[0] for card in cards]
    # Check for pair
    for rank in ranks:
        if ranks.count(rank) == 2:
            # Get the 2 cards that make the pair
            pair = [card for card in cards if card[0] == rank]
            # Get the remaining cards
            remaining_cards = [card for card in cards if card[0] != rank]
            # Get other 3 highest cards
            remaining_cards = sort_by_rank(remaining_cards)
            remaining_cards = remaining_cards[0:3]
            # Return pair and the 5 cards that make it
            return True, pair + remaining_cards
    return False, cards


def check_winner(player_hand, dealer_hand, board):
    # Get 5 cards hands for dealer and player
    player_hand = return_hand(player_hand, board)
    dealer_hand = return_hand(dealer_hand, board)
    if hand_values[player_hand[0]] > hand_values[dealer_hand[0]]:
        return 'Player'
    elif hand_values[player_hand[0]] < hand_values[dealer_hand[0]]:
        return 'Dealer'
    else:
        return get_winner_if_same_hand_rank(player_hand, dealer_hand, player_hand[0])


States = {'IDLE': 0, 'BETTING': 1, 'DEALING': 2, 'PLAYER_TURN_PRE_FLOP': 3, 'PLAYER_BET_3X_OR_4X': 4, 'OPEN_FLOP': 5,
          'PLAYER_TURN_FLOP': 6, 'PLAYER_BET_2X': 7, 'OPEN_TURN_AND_RIVER': 8, 'PLAYER_TURN_FULL_BOARD': 9,
          'SHOWDOWN': 10, 'UPDATE_BALANCE': 11}


class Game:
    def __init__(self):
        self.player_balance = PlayerBalance(1000)
        self.deck = Deck()
        self.board = []
        self.player_hand = []
        self.dealer_hand = []
        self.bets = Bets()
        self.money_won_in_round = 0

    def print_game(self):
        # Delete terminal
        print('\n' * 80)  # prints 80 line breaks
        # Print game state
        print('Player balance: {}'.format(self.player_balance.balance))
        print('Board: {}'.format(self.board))
        print('Player hand: {}'.format(self.player_hand))
        print('Dealer hand: {}'.format(self.dealer_hand))
        print('Bets: {}'.format(self.bets.get_bets()))

    def start_game(self):
        self.state_zero()

    def state_zero(self):
        input("Press Enter to continue...")
        self.deck.shuffle()
        self.board = []
        self.player_hand = []
        self.dealer_hand = []
        self.bets = Bets()
        self.print_game()
        self.money_won_in_round = 0
        self.state_one()

    def state_one(self):
        self.print_game()
        # Ask player for ante and trips bet
        ante_bet = input('Enter ante bet: ')
        if ante_bet.isnumeric() and int(ante_bet) > 0:
            ante_bet = int(ante_bet)
        else:
            print('Invalid input, press enter to try again')
            # wait for 1.5 seconds
            time.sleep(1.5)
            self.state_one()
        # check if input is valid
        trips_bet = input('Enter trips bet: ')
        if trips_bet.isnumeric() and int(trips_bet) > 0:
            trips_bet = int(trips_bet)
        else:
            print('Invalid input, press enter to try again')
            # wait for 1.5 seconds
            time.sleep(1.5)
            self.state_one()
        # Check if player has enough money
        if self.player_balance.balance < ante_bet * 2 + trips_bet:
            print('Not enough money, press enter to try lower bets')
            # wait for 1.5 seconds
            time.sleep(1.5)
            self.state_one()
            return
        # Place bets
        self.bets.bet(ante_bet, trips_bet)
        # Update player balance
        self.player_balance.remove_funds(ante_bet * 2 + trips_bet)
        self.state_two()

    def state_two(self):
        self.player_hand = self.deck.deal_two_cards()
        self.print_game()
        self.state_three()

    def state_three(self):
        self.print_game()
        # Ask player for check/ Bet 3x/ Bet 4x
        player_action = input('Enter action (check, bet 3x, bet 4x): ')
        if player_action == 'check':
            self.state_five()
        elif player_action == 'bet 3x':
            # Check if player has enough money
            if self.player_balance.balance < self.bets.ante * 3:
                print('Not enough money')
                # wait for 1.5 seconds
                time.sleep(1.5)
                self.state_three()
                return
            # Place bet
            self.bets.add_play(self.bets.ante * 3)
            # Update player balance
            self.player_balance.remove_funds(self.bets.ante * 3)
            self.state_four()
        elif player_action == 'bet 4x':
            # Check if player has enough money
            if self.player_balance.balance < self.bets.ante * 4:
                print('Not enough money')
                # wait for 1.5 seconds
                time.sleep(1.5)
                self.state_three()
            # Place bet
            self.bets.add_play(self.bets.ante * 4)
            # Update player balance
            self.player_balance.remove_funds(self.bets.ante * 4)
            self.state_four()
        else:
            print('Invalid action')
            # wait for 1.5 seconds
            time.sleep(1.5)
            self.state_three()

    def state_four(self):
        self.print_game()
        # Open 5 cards on the board
        self.board = self.deck.deal_five_cards()
        self.state_ten()

    def state_five(self):
        self.print_game()
        # Open 3 cards on the board
        self.board = self.deck.deal_three_cards()
        self.state_six()

    def state_six(self):
        self.print_game()
        print('Player hand: {}'.format(return_hand(self.player_hand, self.board)))
        # Ask player for check/ Bet 2x
        player_action = input('Enter action (check, bet 2x): ')
        if player_action == 'check':
            self.state_eight()
        elif player_action == 'bet 2x':
            # Check if player has enough money
            if self.player_balance.balance < self.bets.ante * 2:
                print('Not enough money')
                # wait for 1.5 seconds
                time.sleep(1.5)
                self.state_six()
            # Place bet
            self.bets.add_play(self.bets.ante * 2)
            # Update player balance
            self.player_balance.remove_funds(self.bets.ante * 2)
            self.state_seven()
        else:
            print('Invalid action')
            # wait for 1.5 seconds
            time.sleep(1.5)
            self.state_six()

    def state_seven(self):
        self.print_game()
        # Add 2 cards on the board
        self.board += self.deck.deal_two_cards()
        self.state_ten()

    def state_eight(self):
        self.print_game()
        # Add 2 cards on the board
        self.board += self.deck.deal_two_cards()
        self.state_nine()

    def state_nine(self):
        self.print_game()
        print('Player hand: {}'.format(return_hand(self.player_hand, self.board)))
        # Ask player for Fold/ Bet 1x
        player_action = input('Enter action (fold, bet 1x): ')
        if player_action == 'fold':
            # wait for 1.5 seconds
            time.sleep(1.5)
            self.state_eleven()
        elif player_action == 'bet 1x':
            # Check if player has enough money
            if self.player_balance.balance < self.bets.ante:
                print('Not enough money, Lost hand')
                # wait for 1.5 seconds
                time.sleep(1.5)
                self.state_zero()
            # Place bet
            self.bets.add_play(self.bets.ante)
            # Update player balance
            self.player_balance.remove_funds(self.bets.ante)
            self.state_ten()
        else:
            print('Invalid action')
            # wait for 1.5 seconds
            time.sleep(1.5)
            self.state_nine()

    def state_ten(self):
        # Deal dealer hand
        self.dealer_hand = self.deck.deal_two_cards()
        self.print_game()
        # Compare hands
        winner = check_winner(self.player_hand, self.dealer_hand, self.board)
        player_final_hand = return_hand(self.player_hand, self.board)
        dealer_final_hand = return_hand(self.dealer_hand, self.board)
        trips_payout = get_trips_payout(player_final_hand[1], self.bets.trips)
        self.money_won_in_round += trips_payout
        # Add Trips bet and winnings to player balance
        self.player_balance.add_funds(trips_payout)
        if winner == 'Player':
            blind_payout = get_blind_payout(player_final_hand[1], self.bets.blind)
            # Add Blind and play bets and winnings to player balance
            self.player_balance.add_funds(blind_payout + self.bets.play * 2)
            self.money_won_in_round += blind_payout + self.bets.play * 2
            if dealer_final_hand != 'High Card':
                # Add Ante win to player balance
                self.player_balance.add_funds(self.bets.ante)
                self.money_won_in_round += self.bets.ante
            # Add Ante bet to player balance
            self.player_balance.add_funds(self.bets.ante)
            self.money_won_in_round += self.bets.ante
        elif winner == 'Tie':
            # Add Ante, play and Blind bets to player balance
            self.player_balance.add_funds(self.bets.ante + self.bets.play + self.bets.blind)
            self.money_won_in_round += self.bets.ante + self.bets.play + self.bets.blind
        print(f'{winner} wins')
        print('Player hand: {}'.format(player_final_hand))
        print('Dealer hand: {}'.format(dealer_final_hand))
        print('Money won in round: {}'.format(self.money_won_in_round - sum(self.bets.get_bets())))
        # wait for 1.5 seconds
        time.sleep(1.5)
        self.state_zero()

    def state_eleven(self):
        self.dealer_hand = self.deck.deal_two_cards()
        player_final_hand = return_hand(self.player_hand, self.board)
        dealer_final_hand = return_hand(self.dealer_hand, self.board)
        # pay for trips
        trips_payout = get_trips_payout(player_final_hand[0], self.bets.trips)
        self.money_won_in_round += trips_payout
        # Update player balance
        self.player_balance.add_funds(trips_payout)
        print('Player folds')
        print('Player hand: {}'.format(player_final_hand))
        print('Dealer hand: {}'.format(dealer_final_hand))
        self.print_game()
        if (trips_payout > 0):
            print('trips payout: {}'.format(trips_payout - self.bets.get_bets()[2]))
        # wait for 1.5 seconds
        time.sleep(1.5)
        self.state_zero()


def get_trips_payout(hand, trips):
    if hand == 'Royal Flush':
        return trips * 50 + trips
    elif hand == 'Straight Flush':
        return trips * 40 + trips
    elif hand == 'Four of a Kind':
        return trips * 30 + trips
    elif hand == 'Full House':
        return trips * 8 + trips
    elif hand == 'Flush':
        return trips * 6 + trips
    elif hand == 'Straight':
        return trips * 5 + trips
    elif hand == 'Three of a Kind':
        return trips * 3 + trips
    else:
        return 0


def get_blind_payout(hand, blind):
    if hand == 'Royal Flush':
        return blind * 500 + blind
    elif hand == 'Straight Flush':
        return blind * 50 + blind
    elif hand == 'Four of a Kind':
        return blind * 10 + blind
    elif hand == 'Full House':
        return blind * 3 + blind
    elif hand == 'Flush':
        return blind * 1.5 + blind
    elif hand == 'Straight':
        return blind * 1 + blind
    else:
        return blind


def get_winner_if_same_hand_rank(player_hand, dealer_hand, hand_rank):
    # FIXME: hand[1][x][0] error if x is broadway ('A', 'K', 'Q', 'J'). need to compare broadway cards somehow
    if hand_rank == 'High Card':
        # Compare high cards
        for i in range(5):
            if player_hand[1][i][0] > dealer_hand[1][i][0]:
                return 'Player'
            elif player_hand[1][i][0] < dealer_hand[1][i][0]:
                return 'Dealer'
        return 'Tie'

    elif hand_rank == 'Pair':
        # Compare pairs
        if player_hand[1][0][0] > dealer_hand[1][0][0]:
            return 'Player'
        elif player_hand[1][0][0] < dealer_hand[1][0][0]:
            return 'Dealer'
        # Compare high cards (last 3 cards)
        for i in range(3):
            if player_hand[1][i + 2][0] > dealer_hand[1][i + 2][0]:
                return 'Player'
            elif player_hand[1][i + 2][0] < dealer_hand[1][i + 2][0]:
                return 'Dealer'
        return 'Tie'

    elif hand_rank == 'Two Pair':
        # Compare first pair
        if player_hand[1][0][0] > dealer_hand[1][0][0]:
            return 'Player'
        elif player_hand[1][0][0] < dealer_hand[1][0][0]:
            return 'Dealer'
        # Compare second pair
        if player_hand[1][2][0] > dealer_hand[1][2][0]:
            return 'Player'
        elif player_hand[1][2][0] < dealer_hand[1][2][0]:
            return 'Dealer'
        # Compare high card
        if player_hand[1][4][0] > dealer_hand[1][4][0]:
            return 'Player'
        elif player_hand[1][4][0] < dealer_hand[1][4][0]:
            return 'Dealer'
        return 'Tie'

    elif hand_rank == 'Three of a Kind':
        # Compare three of a kind
        if player_hand[1][0][0] > dealer_hand[1][0][0]:
            return 'Player'
        elif player_hand[1][0][0] < dealer_hand[1][0][0]:
            return 'Dealer'
        # Compare high cards
        if player_hand[1][3][0]> dealer_hand[1][3][0]:
            return 'Player'
        elif player_hand[1][3][0] < dealer_hand[1][3][0]:
            return 'Dealer'
        if player_hand[1][4][0] > dealer_hand[1][4][0]:
            return 'Player'
        elif player_hand[1][4][0] < dealer_hand[1][4][0]:
            return 'Dealer'
        return 'Tie'

    elif hand_rank == 'Straight':
        # Compare high card
        if player_hand[1][0][0] > dealer_hand[1][0][0]:
            return 'Player'
        elif player_hand[1][0][0] < dealer_hand[1][0][0]:
            return 'Dealer'
        return 'Tie'

    elif hand_rank == 'Flush':
        # Compare high cards
        for i in range(5):
            if player_hand[1][i][0] > dealer_hand[1][i][0]:
                return 'Player'
            elif player_hand[1][i][0] < dealer_hand[1][i][0]:
                return 'Dealer'
        return 'Tie'

    elif hand_rank == 'Full House':
        # Compare three of a kind
        if player_hand[1][0][0] > dealer_hand[1][0][0]:
            return 'Player'
        elif player_hand[1][0][0] < dealer_hand[1][0][0]:
            return 'Dealer'
        # Compare pair
        if player_hand[1][3][0] > dealer_hand[1][3][0]:
            return 'Player'
        elif player_hand[1][3][0] < dealer_hand[1][3][0]:
            return 'Dealer'
        return 'Tie'

    elif hand_rank == 'Four of a Kind':
        # Compare four of a kind
        if player_hand[1][0][0] > dealer_hand[1][0][0]:
            return 'Player'
        elif player_hand[1][0][0] < dealer_hand[1][0][0]:
            return 'Dealer'
        # Compare high card
        if player_hand[1][4][0] > dealer_hand[1][4][0]:
            return 'Player'
        elif player_hand[1][4][0] < dealer_hand[1][4][0]:
            return 'Dealer'
        return 'Tie'

    elif hand_rank == 'Straight Flush':
        # Compare high card
        if player_hand[1][0][0] > dealer_hand[1][0][0]:
            return 'Player'
        elif player_hand[1][0][0] < dealer_hand[1][0][0]:
            return 'Dealer'
        return 'Tie'

    elif hand_rank == 'Royal Flush':
        return 'Tie'
