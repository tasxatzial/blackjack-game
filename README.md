# Blackjack

## Description

The game of [Blackjack](https://en.wikipedia.org/wiki/Blackjack).

## Language

Python.

## Rules

### Setup

The player and the dealer are each dealt two cards initially with one
of the dealer's cards facing down.

### Playing

Initially the player may use "hit" to get new cards. If, at any point,
the sum of his cards exceeds 21, his hand is "busted" and he loses.
The player may also use "stand" to end his turn. In that case the dealer will
receive cards until the sum of his cards is 17 or more. For the dealer aces
always count as 11 unless the sum of his cards exceeds 21.

### Winning

If player's hand busts, dealer wins.
If dealer's hand busts, player wins.
Otherwise, player and dealer compare their hands and the hand
with the higher sum wins. Dealer wins ties.

## Run

The game runs in [Codesculptor](http://www.codeskulptor.org/) (python 2) or in [Codesculptor](https://py3.codeskulptor.org/) (python 3)
