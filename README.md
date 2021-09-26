# AI: GO Project
This is the depository of AI project in Python. Welcome !

The project consists on implementing an intelligent GO player to integrate a tournament.

## Team members

- Boullit Mohamed Faycal (Sans Machine 2)
- Elomari Alaoui Ismail  (Sans Machine 2)

## Project Arborescence

*The current folder contains all files needed:*
- localGame.py: to launch a game with AI player against AI player

- namedGame.py: to launch costumized game

- playerInterface.py: interface specification for players

- myPlayer.py: AI player, implemented using MinMax with AlphaBeta pruning

- randomPlayer.py: a random player

- testHeuristic.py: we used this file to determinate some paramaters for our evaluation function

- Goban.py: file containing GO rules

- GnuGo.py: file to communicate with GnuGo player

- starter-go.py: Examples of developpment of random games (using legal_moves and push/pop).

## Requirements

You can start the game with:

        - python3 namedGame.py myPlayer randomPlayer
                - Launch game between (BLACK) myPlayer AI player and (WHITE) randomPlayer

        - python3 namedGame.py myPlayer gnugoPlayer.py
                - Launch game between (BLACK) myPlayer AI player and (WHITE) gnugo

        - python3 localGame.py
                - Launch game between (BLACK) myPlayer AI player and (WHITE) myPlayer AI player