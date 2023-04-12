import random

# Define the deck of cards
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

    def deal_seven_cards_for_testing(self):
        return [self.cards.pop() for i in range(7)]

    def deal_five_cards_for_testing(self):
        return [self.cards.pop() for i in range(5)]

    def deal_two_cards_for_testing(self):
        return [self.cards.pop() for i in range(2)]


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
    def __init__(self, ante, blind, trip, play):
        self.ante = ante
        self.blind = blind
        self.trip = trip

    def add_play(self, amount):
        self.play += amount

    def get_bets(self):
        # return all bets as a list
        return [self.ante, self.blind, self.trip, self.play]


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



