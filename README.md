# Conquerors of Catan

&nbsp; 🌾 &nbsp; 🌲&nbsp; 🐑&nbsp; 🧱 &nbsp; 🪨  &nbsp; &nbsp; &nbsp; ❔

## Introduction

Conquerors of Catan is a final year bachelors project at the University of Essex, aimed at investigating different AI strategies for the board game Settlers of Catan. The project is being developed solely by [Harrison Phillingham](https://harrison.phillingham.com).

Currently, these include:
- Random AI
- MiniMax Search AI - See [here](https://en.wikipedia.org/wiki/Minimax) for more information
- Monte Carlo Tree Search AI - See [here](https://wikipedia.org/wiki/Monte_Carlo_tree_search) for more information

The game can be played with or without a Human Player. To specify the players, edit the `players` list at the top of `__main__.py`.

Game play happens in turns. On each turn, the player rolls the dice, and then performs one or move of the following actions:
- Trading with the bank
- Purchasing a development card
- Building a settlement, city or road.

These interactions are automated for the AI players, but the human player is prompted to make a choice and told how to do so. All interactions for humans happen in the terminal.

The overall aim is to be the first player to reach 10 victory points. Points are scored as follows:
- 1 point for each settlement
- 2 points for each city
- 1 point for each development card of the type "Victory Point"
- 2 points for having the longest road
- 2 points for having the largest army

## Getting Started

In order to run the game, you first need to install the dependencies. This can be done by running the following command:

```pip install -r requirements.txt```

After the dependencies are installed, you can run the program by running the following command:

```cd ./src && python3 __main__.py``` or ```python3 src```

(You may need to change `python3` to `python` depending on your system)

## Game Information and Workings

### Board State Representation

The board uses letters and grid references to identify the different tiles and vertices on the board. The tiles are lettered in alphabetic order from top to bottom, left to right. The vertices are labeled with each letter that they are adjacent to, and then a number indicating their position. For example, the top most tile is 'a' and has vertices 'a1' and 'a2' for the two vertices in the ocean. Continuing clockwise, it then has 'a,c', 'a,c,e', 'a,b,e' and 'a,b'.

The board data is stored as a series of lists, arrays and dictionaries. These are:
- `tiles` - A list of class `tile` objects, representing the tiles on the board
- `buildings` - A dictionary mapping the grid references to a tuple of the player, the building type, and the tiles that touch it
- `roads` - A dictionary mapping tuples of the start and end of the road to the player that owns it, and the symbol to be drawn on the board

The board also has a number of other variables that are used to keep track of the game state:
- `players` - A list of the players in the game
- `resource_deck` - A list of the resources in the bank
- `development_card_deck` - A list of the development cards in the bank
- `largest_army` - A list of the player with the largest army, and the number of knights they have
- `longest_road` - A list of the player with the longest road, and the number of roads they have


### MiniMax Search Heuristic

The MiniMax Search Heuristic uses the following values and weights to evaluate the board. These are:

| Metric                         | Description                                                                                        |
|--------------------------------|----------------------------------------------------------------------------------------------------|
| Victory Points                 | VP * 10. The number of victory points the player has                                               |
| Current VP > Next Highest VP   | Adds 50 if the current player has more victory points than the next highest player, or 25 if equal |
| Roads Count                    | RC * 2. The number of roads the player has                                                         |
| Total Num. resources available | TR * 1. A sum of how many resources each city and settlement can get.                              |
| Development Cards              | DC * 3. The number of development cards the player has                                             |
| Robber Cards                   | Played Robber Cards * 3.                                                                           |
If the player has won, the metric returns 1000000.

The metric prioritizes getting victory points and expanding over hoarding cards. It is a fairly general heuristic, and is not specific to any particular strategy.

## Known Differences to the main game

- 1


## Contact

If you have any questions, please feel free to contact me at [harrison@phillingham.com](mailto:harrison@phillingham.com)
