"""Blackjack game

Setup:
The player and the dealer are each dealt two cards initially with one
of the dealer's cards being dealt faced down.

Playing:
Initially the player may use "hit" to get new cards. If, at any point,
the sum of his cards exceeds 21, his hand is "busted" and he loses.
The player may also use "stand" to end his turn. In that case the dealer will
receive cards until the sum of his cards 17 or more. For the dealer, aces
always count as 11 unless the sum of his cards exceeds 21.

Winning:
If player's hand busts, the dealer wins.
If dealer's hand busts, the player wins.
Otherwise, player and dealer compare their hands and the hand
with the higher sum wins. Dealer wins ties.
"""

import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
URL = 'http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png'
card_images = simplegui.load_image(URL)

# load back image of cards
CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
URL = 'http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png'
card_back = simplegui.load_image(URL)

# initial score
score = 0

# a round is not in progress
in_play = False

# define globals for the cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9,
          'T':10, 'J':10, 'Q':10, 'K':10}


class Card:
    """Creates a Card type object given a suit and a rank"""

    def __init__(self, suit, rank):
        """Each Card has a suit, a rank, and is drawn face up by default"""
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print('Invalid card: ', suit, rank)
        self.hidden = False

    def __str__(self):
        """Returns the suit and the rank of the Card"""
        return self.suit + self.rank

    def get_suit(self):
        """Returns the suit of the Card"""
        return self.suit

    def get_rank(self):
        """Returns the rank of the Card"""
        return self.rank

    def draw(self, canvas, pos):
        """Draws an image for the Card on the canvas at position pos"""

        # if the Card is not hidden, draw the corresponding image face up
        if not self.hidden:
            card_loc = (CARD_CENTER[0] + CARD_SIZE[0]*RANKS.index(self.rank), 
                        CARD_CENTER[1] + CARD_SIZE[1]*SUITS.index(self.suit))
            dest_loc = [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]]
            canvas.draw_image(card_images, card_loc, CARD_SIZE,
                              dest_loc, CARD_SIZE)

        # else draw the back of the Card
        else:
            dest_loc = [pos[0] + CARD_BACK_CENTER[0],
                        pos[1] + CARD_BACK_CENTER[1]]
            canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE,
                              dest_loc, CARD_BACK_SIZE)
    
    def hide(self):
        """Hides the Card: Card is drawn face down"""
        self.hidden = True

    def show(self):
        """Exposes the Card: Card is drawn face up"""
        self.hidden = False


class Hand:
    """Creates a Hand type object. Card type objects can be added to it"""

    def __init__(self):
        """Initializes an instance as an empty list"""
        self.cards = []

    def __str__(self):
        """Returns all Cards contained in the Hand"""
        cards = ''
        for card in self.cards:
            cards += str(card) + ' '
        return 'Hand contains ' + cards

    def add_card(self, card):
        """Adds a Card to the Hand"""
        self.cards.append(card)

    def get_value(self):
        """Returns the value of the Hand"""
        value = 0
        has_ace = False

        # for each Card in Hand
        for card in self.cards:

            # get its rank
            rank = card.get_rank()

            # check if Card is an Ace
            if rank == 'A':
                has_ace = True

            # and update the Hand value based on the VALUES dictionary
            value += VALUES[rank]

        # if Hand has an Ace, add 10 to Hand value if hand doesn't bust
        if has_ace and value + 10 <= 21:
            value += 10
        return value
   
    def draw(self, canvas, pos):
        """Draws Hand on the canvas starting at position pos >= 0"""
        for card in self.cards:
            loc = [pos[0] + (CARD_SIZE[0] + 8)*self.cards.index(card), pos[1]]
            card.draw(canvas, loc)
    
    def find_card(self, num):
        """Returns the Card of the Hand at position num >= 0"""
        return self.cards[num]

    
class Deck:
    """Creates a Deck type object from all possible Card objects"""

    def __init__(self):
        """Initializes an instance as a list of all possible Card objects"""
        self.deck = [Card(suit, rank) for suit in SUITS for rank in RANKS]

    def shuffle(self):
        """Shuffles the Deck"""
        random.shuffle(self.deck)

    def deal_card(self):
        """Removes and returns the last Card from the Deck"""
        card = self.deck.pop(len(self.deck) - 1)
        return card
    
    def __str__(self):
        """Returns all Cards contained in the Deck"""
        cards = ''
        for card in self.deck:
            cards += str(card) + ' '
        return 'Deck contains ' + cards


def deal():
    """Event handler for the deal button"""
    global in_play, player_hand, dealer_hand, score, deck

    # if a round is in progress, player loses
    if in_play:
        score -= 1

    # start a new round
    in_play = True

    # create and shuffle the Deck
    deck = Deck()
    deck.shuffle()

    # create Hands for player and dealer
    player_hand = Hand()
    dealer_hand = Hand()

    # add 2 Cards to player's Hand
    player_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())

    # add 2 Cards to dealer's Hand, first one hidden
    dealer_card = deck.deal_card()
    dealer_card.hide()
    dealer_hand.add_card(dealer_card)
    dealer_hand.add_card(deck.deal_card())


def hit():
    """Event handler for the hit button"""
    global in_play, score, outcome

    # give player a new Card if a round is in progress
    if in_play:
        player_hand.add_card(deck.deal_card())

        # if player's hand busted, player loses
        if player_hand.get_value() > 21:
            outcome = 'You have busted'
            score -= 1
            in_play = False


def stand():
    """Event handler for the stand button"""
    global in_play, score, outcome
    
    # if a round is in progress, give dealer Cards until his Hand has
    # value >= 17
    if in_play:
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(deck.deal_card())

        # if dealer's Hand not busted && >= player's Hand: dealer wins
        if (dealer_hand.get_value() >= player_hand.get_value() and
                dealer_hand.get_value() <= 21):
            outcome = 'You lost'
            score -= 1

        # else player wins
        else:
            outcome = 'You won'
            score += 1

    # round ends
    in_play = False


def draw(canvas):
    """Handles drawing on the canvas"""
    
    # draw messages
    canvas.draw_text('Blackjack', [20, 100], 50, 'Yellow')
    canvas.draw_text('Dealer', [20, 170], 30, 'Black')
    canvas.draw_text('Player', [20, 370], 30, 'Black')
    canvas.draw_text('Score: ' + str(score), [300, 100], 30, 'Black')
    if in_play:
        canvas.draw_text('Hit or Stand?', [200, 370], 30, 'Black')
    else:
        canvas.draw_text('New deal?', [200, 370], 30, 'Black')
        canvas.draw_text(outcome, [300, 170], 30, 'Black')
        
    # draw player's Hand
    player_hand.draw(canvas, [20, 400])
    
    # if a round is not in progress
    if not in_play:
        
        # get dealer's first Card
        dealer_first_card = dealer_hand.find_card(0)
    
        # and unhide it
        dealer_first_card.show()
    
    # draw dealer's Hand
    dealer_hand.draw(canvas, [20, 200])

# create frame and set canvas background color
frame = simplegui.create_frame('Blackjack', 600, 600)
frame.set_canvas_background('Green')

# register event handlers
frame.add_button('Deal', deal, 200)
frame.add_button('Hit',  hit, 200)
frame.add_button('Stand', stand, 200)
frame.set_draw_handler(draw)

# start game & frame
deal()
frame.start()