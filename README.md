# Conquerors of Catan

&nbsp; 🌾 &nbsp; 🌲&nbsp; 🐑&nbsp; 🧱 &nbsp; 🪨  &nbsp; &nbsp; &nbsp; ❔

[Goals and Achievements](./docs/challenge_week/Goals_and_Achievements.md)

[Project Planning](./docs/challenge_week/Project_Planning.md)

## Getting Started

In order to run the game, you first need to install the dependencies. This can be done by running the following command:

```pip install -r requirements.txt```

After the dependencies are installed, you can run the program by running the following command:

```cd ./src && python __main__.py``` or ```cd ./src && python3 __main__.py```

## Notes

It is currently possible to get stuck in a loop where no players have enough resources to do anything. This is because trading is currently not implemented, and so each player is stuck with the resources they have. This will be fixed in the future.
