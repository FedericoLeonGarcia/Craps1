#!/usr/bin/env python

from die import * 
import sys
import crapsResources_rc
from time import sleep
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtGui, uic
from PyQt5.QtWidgets import  QMainWindow, QApplication

class Craps(QMainWindow) :
    """A game of Craps."""
    die1 = die2 = None

    def __init__( self, parent=None ):
        """Build a game with two dice."""

        super().__init__(parent)
        uic.loadUi("Craps.ui", self)

        self.bidSpinBox.setRange ( 10, 500 )
        self.bidSpinBox.setSingleStep ( 5 )
        self.resultText = "You have not rolled yet."
        self.wins = 0
        self.losses = 0
        self.bank = 1000
        self.die1 = Die()
        self.die2 = Die()
        self.total = 0
        self.firstRoll = True

        self.buttonText = "Roll"
             #          0  1  2  3  4    5    6    7    8    9    10   11   12
        self.payouts = [0, 0, 0, 0, 2.0, 1.5, 1.2, 1.0, 1.2, 1.5, 2.0, 1.0, 0]

        self.rollButton.clicked.connect(self.rollButtonClickedHandler)

    def __str__( self ):
        """String representation for Dice.
        """

        return "Die1: %s\nDie2: %s" % ( str(self.die1),  str(self.die2) )

    def updateUI ( self ):
        self.die1View.setPixmap(QtGui.QPixmap( ":/" + str( self.die1.getValue() ) ) )
        self.die2View.setPixmap(QtGui.QPixmap( ":/" + str( self.die2.getValue() ) ) )
        self.rollingForLabel.setText("Your roll is " + str(self.total))
        self.winsLabel.setText(str(self.wins))
        self.lossesLabel.setText(str(self.losses))
        self.resultsLabel.setText(str(self.resultText))
        self.bankValue.setText("$" + str(self.bank))
        # Add your code here to update the GUI view so it matches the game state.

		# Player asked for another roll of the dice.
    def rollButtonClickedHandler ( self ):
        self.currentBet = self.bidSpinBox.value()



        if self.currentBet > self.bank:
            self.resultText = "You cannot bet.\n You don't have the moeny."
            self.updateUI()
            return
        self.die1.roll()
        self.die2.roll()
        self.total = self.die1.getValue() + self.die2.getValue()

        if self.firstRoll == True:
            if self.total == 7 or self.total == 11:
                self.resultText = "You win."
                self.wins += 1
                self.bank += self.currentBet
            elif self.total == 2 or self.total == 3 or self.total == 1:
                self.resultText = "You lose."
                self.losses += 1
                self.bank -= self.currentBet
            else:
                self.firstRoll = False
                self.resultText = "Roll again."
                self.previousRolled = self.total
        else:
            if self.total == self.previousRolled:
                self.resultText = "You win."
                self.wins += 1
                self.bank += self.payouts[self.total] * self.currentBet
            else:
                self.resultText = "You lose."
                self.losses += 1
                self.bank -= self.currentBet
            self.firstRoll = True

        if self.bank <= 0:
            self.resultText = "Game Over"
            self.rollButton.setEnabled(False)
        self.updateUI()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    diceApp = Craps()
    diceApp.updateUI()
    diceApp.show()
    sys.exit(app.exec_())


