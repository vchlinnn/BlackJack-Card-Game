#!/usr/bin/env python
# coding: utf-8

# ## Steps to Build this: 
# 
# 1. Create a deck of 52 cards
# 2. Shuffle the deck
# 3. Ask the Player for their bet
# 4. Make sure that the Player's bet does not exceed their available chips
# 5. Deal two cards to the Dealer and two cards to the Player
# 6. Show only one of the Dealer's cards, the other remains hidden
# 7. Show both of the Player's cards
# 8. Ask the Player if they wish to Hit, and take another card
# 9. If the Player's hand doesn't Bust (go over 21), ask if they'd like to Hit again.
# 10. If a Player Stands, play the Dealer's hand. The dealer will always Hit until the Dealer's value meets or exceeds 17
# 11. Determine the winner and adjust the Player's chips accordingly
# 12. Ask the Player if they'd like to play again

# In[7]:


# Import the random module to shuffle the deck:
import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
         'Queen':10, 'King':10, 'Ace':11}

# Declare a Boolean value to control while loops: 
playing = True


# In[8]:


# Create a Card Class with two attributes: suit and rank. 

class Card:
    
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
    
    def __str__(self):
        return (f"{self.suit} of {self.rank}")


# In[9]:


# Create a Deck Class:

class Deck:
    
    def __init__(self):
        self.deck = []  # start with an empty list
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit,rank))
    
    def __str__(self):
        deck_str = ""
        for card in self.deck:
            deck_str += str(card) + "\n"
        return deck_str.rstrip()

    def shuffle(self):
        random.shuffle(self.deck)
        
    def deal(self):
        return self.deck.pop()


# In[10]:


#Test our Deck:

test_deck = Deck()
print(test_deck)


# In[11]:


# Create a Hand Class to hold Card objects dealt from the Deck and
# calculate the value of those cards:

class Hand:
    def __init__(self):
        self.cards = []  # start with an empty list as we did in the Deck class
        self.value = 0   # start with zero value
        self.aces = 0    # add an attribute to keep track of aces
            
    def add_card(self,card):
        # card passed in 
        # from Deck.deal() --> single Card(suit,rank)
        self.cards.append(card)
        self.value += values[card.rank]
        
        # track for an Ace
        if card.rank == 'Aces':
            self.aces += 1
    
    def adjust_for_ace(self):
        while self.value > 21 and self.aces: #(if i still have an ace)
            self.value -= 10
            self.aces -= 1 


# In[12]:


# Create a Chips Class - keep track of a Player's starting chips, bets, and wins:

class Chips:
    
    def __init__(self,total = 100):
        self.total = total  # This can be set to a default value or supplied by a user input
        self.bet = 0
        
    def win_bet(self):
        self.total += self.bet
    
    def lose_bet(self):
        self.total -= self.bet


# In[13]:


# Taking bets:

def take_bet(chips):
    
    while True:
        
        try:
            chips.bet = int(input("How many chips would you like to bet? "))
        except:
            print("Sorry please provide an integer")
        else:
            if chips.bet > chips.total:
                print("Not enough chips")
            else:
                break
                
# Taking hits:

def hit(deck,hand):
    
    single_card = deck.deal()
    hand.add_card(single_card)
    hand.adjust_for_ace()
    
# Prompting the Player to Hit or Stand

def hit_or_stand(deck,hand):
    global playing  # to control an upcoming while loop
    
    while True: 
        x = input('Hit or Stand? ')
        
        if x[0].lower() == 'h':
            hit(deck,hand)
        
        elif x[0].lower() == 's':
            print("Player Stands! Dealer's Turn")
            playing = False
        else:
            continue
        break 
        
# Display Cards:

def show_some(player,dealer):
    
    #Show only one of the dealer's cards
    print("\n Dealer's Hand: ")
    print(dealer.cards[1])
    
    #Show all (2 cards) of the player's hand/cards
    print("\n Player's hand : ")
    for card in player.cards:
        print(card)
    
def show_all(player,dealer):
    
    #Show all the dealer's cards
    print("\n All dealer's hand : ")
    for card in dealer.cards:
        print(card)
        
    #Calculate and display value (J+K == 20)
    print(f"Value of Dealer's hand is:{dealer.value}")
    
    #Show all the players cards 
    print("\n Player's hand : ")
    for card in player.cards:
        print(card)
    print(f"Value of Player's hand is:{player.value}")
    
# Handle end of game scenarios:

def player_busts(player,dealer,chips):
    print("Player Busts!")
    chips.lose_bet()

def player_wins(player,dealer,chips):
    print('Player Wins!')
    chips.win_bet()

def dealer_busts(player,dealer,chips):
    print('Dealer Busts!')
    chips.win_bet()
    
def dealer_wins(player,dealer,chips):
    print('Dealer Wins!')
    chips.lose_bet()
    
def push(player,dealer):
    print('Dealer and player tie! PUSH')


# In[ ]:


###  THE GAME ###

while True:
    # Print an opening statement
    print("Game starts!")
    
    # Create & shuffle the deck, deal two cards to each player
    deck = Deck()
    deck.shuffle()
    
    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.adjust_for_ace()
    player_hand.add_card(deck.deal())
    player_hand.adjust_for_ace()
    
    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())
        
    # Set up the Player's chips
    player_chips = Chips()
    
    # Prompt the Player for their bet
    take_bet(player_chips)
    
    # Show cards (but keep one dealer card hidden)
    show_some(player_hand,dealer_hand)
    
    while playing:  # recall this variable from our hit_or_stand function
        
        # Prompt for Player to Hit or Stand
        hit_or_stand(deck,player_hand)
        
        # Show cards (but keep one dealer card hidden)
        show_some(player_hand,dealer_hand)
        
        # If player's hand exceeds 21, run player_busts() and break out of loop
        if player_hand.value > 21:
            player_busts(player_hand,dealer_hand,player_chips)
            break

    # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
        else:
        
            while dealer_hand.value < 17:
                hit(deck,dealer_hand)
                if dealer_hand.value >= 17:
                    dealer_turn = False 
                    break
                
        # Show all cards
        show_all(player_hand,dealer_hand)
    
        # Run different winning scenarios
        if dealer_hand.value > 21:
            dealer_busts(player_hand,dealer_hand,player_chips)
        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand,dealer_hand,player_chips)
        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand,dealer_hand,player_chips)
        else:
            push(player_hand,dealer_hand)
    
    # Inform Player of their chips total 
    print(f"Total chips is: {player_chips.total}")
    # Ask to play again
    new_game = input("Wanna play again? ")
    
    if new_game[0].lower == 'y':
        playing = True
        continue
    else:
        print('Thanks for playing!')
        break


# In[ ]:




