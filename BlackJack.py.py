# Simple app to test image labels.  

# CIS 211
# Spring 2014

# Note: see flip_one_frame.py for a better organization....

from tkinter import *
from tkinter.messagebox import showinfo
from random import randint
from CardLabel import *
import Card
import Deck
import time

class BlackJack(Frame):
    ''' Creates Widgets: labels for players and buttons for the user to interact with and play the game '''
    players = ['Dealer:', 'Player1:']
    def __init__(self, master=None):
        Frame.__init__(self, master)
        CardLabel.load_images()
        # Create Labels
        dealerLabel = Label(root, text = self.players[0])
        dealerLabel.grid(row = 0, column = 0)
        player1Label = Label(root, text = self.players[1])
        player1Label.grid(row = 2, column = 0)
        # Set dimensions of the game space
        for i in range(6):
            root.columnconfigure(i, minsize=80)
        for i in [1,3]:
            root.rowconfigure(i, minsize=106)
        # Buttons 
        self._dealButton = Button(root, text='Deal', command=self.deal, padx=10)
        self._dealButton.grid(row=4, column=0, pady = 0)
        self._hitButton = Button(root, text='Hit', command=self.hit, padx=14)
        self._hitButton.grid(row=4, column=1, pady = 0)
        self._passButton = Button(root, text='Pass', command=self.stand, padx=10)
        self._passButton.grid(row=4, column=2, pady = 0)
        
    def deal(self):
        ''' Adds cards to the game: Creates a deck, shuffles the deck, deals cards to the dealer and then the player '''
        BlackJack.__init__(self) # Reinstantiates the class to reset the game space
        self._deck = Deck.Deck() # 1) Create Deck
        self._deck.shuffle()     # 2) shuffle deck
                                    
        self._dealer = self._deck.deal(2) # 3) Create Dealers Hand 
        self._dealercard1 = CardLabel(root)
        self._dealercard1.grid(row=1, column=0)
        self._dealercard1.display('back', self._dealer[0].num())
        
        self._dealercard2 = CardLabel(root)
        self._dealercard2.grid(row=1, column=1)
        self._dealercard2.display('front', self._dealer[1].num())
        self._player = self._deck.deal(2) # 4) Create Players hand

        for i in range (len(self._player)):
            self._playercards = CardLabel(root)
            self._playercards.grid(row=3, column=i)
            self._playercards.display('front', self._player[i].num())
         
    def hit(self):
        ''' Appends a card to the players hand and then displays that card. If the player busts gameover() is called'''
        self._player.append(self._deck.deal(1)[0])
        self.hits = CardLabel(root)
        self.hits.grid(row=3, column=len(self._player)-1)
        self.hits.display('front', self._player[-1].num())
        #print(self._player)
        if (BlackJack.total(self._player)) > 21:
            BlackJack.gameover(self, 0, 'You Busted!')
            
    def stand(self):
        ''' this function is called when the player clicks the pass button. To stand in blackjack means you pass priority and allow the dealer to play out their hand '''
        self._dealercard1.display('front', self._dealer[0].num())
        while (BlackJack.total(self._dealer) < 22):
            if (BlackJack.total(self._dealer)) < 17:
                self._dealer.append(self._deck.deal(1)[0])
                self.dealerhits = CardLabel(root)
                #self.dealerhits.after(2000)
                self.dealerhits.grid(row=1, column=len(self._dealer)-1)
                self.dealerhits.display('front', self._dealer[-1].num())
            else:
                return self.compare(self._dealer, self._player)

        return BlackJack.gameover(self, 1, 'Dealer Busted!')
            
    def compare(self, dealer, player):
        ''' Compares Dealer hand to Players hand and makes the call to gameover() with appropriate results '''
        dealertotal, playertotal = BlackJack.total(dealer), BlackJack.total(player)
        
        if dealertotal > playertotal:
            BlackJack.gameover(self, 0)
        elif dealertotal < playertotal:
            BlackJack.gameover(self, 1)
        elif dealertotal == 21 and 2 == len(dealer) < len(player):
            BlackJack.gameover(self, 0, "Dealer BlackJack!")
        elif playertotal == 21 and 2 == len(player) < len(dealer):
            BlackJack.gameover(self, 0, "Player BlackJack!")
        else:
            BlackJack.gameover(self, 2, "Push")
       
    def gameover(self, win = 1, result="Highscore wins"):
        ''' called from many other methods; reports if the player wins or loses the game via message box and signals player to start new a game '''
        global Score
        script = [" YOU LOSE... ", "YOU WIN!", "No winners"]
        msg = showinfo(message = (script[win]," Click the 'Deal' button to play again"),
                        title = ("GAME OVER:", result)) # This should be a message box
        self._hitButton['state'] = 'disabled'
        self._passButton['state'] = 'disabled'
        self._dealButton['bg'] = 'green'

    def total(hand):
        ''' calculates the total point value of a hand, allowing for smart handing of Aces dual, but mutually exclusive value state '''
        values = { "2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9, "10":10, "J":10, "Q":10, "K":10, "A":11 } 
        
        result = 0
        numAces = 0
        
        for i in range (len(hand)):
            result += values[hand[i].symb()]
            if hand[i].symb() == 'A':
                numAces += 1
        while result > 21 and numAces > 0:
            result -= 10
            numAces -= 1
        
        return result
        
## Make It Run
if __name__ == '__main__':
    root = Tk(className="'BlackJack' -- Multilingual")
    app = BlackJack(master=root)
    app.mainloop()