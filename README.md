# Sudoku Solver

## Introduction

In the creation of artificial intelligence, it’s important not only to enable an AI agent to process inputs and generate outputs, but to teach them to act within a system of rules. Making a program that plays games is a very valuable way of setting down the building blocks for a more complex, truly intelligent agent - and it’s fun! Games have many different systems of rules, and playing a game by its unique rule system is great way to work on problem-solving techniques. Game-playing programs also keep both programmers and users interested, because games can capture the imagination and inspire the drive to win even in observers.

In recent years, sudoku has exploded in popularity as a simple game that is deceptively challenging - and enjoyable - to play. The rules of sudoku are these:

1. You have a grid of 81 boxes.
2. These boxes are divided into 9 blocks, each containing 9 boxes. 
3. Each of the 9 blocks in the grid _must_ contain every possible number, from 1 to 9.
4. Every number from 1 to 9 _must_ appear only once in each row, column, or block on the grid.

Sudoku can be made even more difficult by the addition of of an optional, fifth rule:

5. Each _diagonal_ line of nine squares across the grid must also contain all of the numbers 1-9.

The addition of the diagonal rule can make a sudoku much more tricky. Fortunately, there are also strategies that can be applied to make a sudoku puzzle easier to solve, and one of these tricks is called the ’naked twins’ strategy. It works like this:

1. Look for individual boxes in which only two numbers are possible solutions.
2. If there is any other box in the same row, column or block - or diagonal line - which also has only those two numbers as possible solutions, eliminate those numbers from the possible solutions for every other box in the same unit.

A useful technique indeed. Unfortunately, humans in general are pretty bad at math, and we're worse at memorizing running lists of numbers. Luckily, doing math and keeping lists are two things computers are excellent at doing! And writing a program is very successful way to put the ’naked twins’ sudoku strategy to work.

## Description

The collection of programs in this repository form the basis of an agent which plays sudoku using several strategies: a) the ‘elimination’ strategy, b) the ‘only-choice’ strategy, and c) the ’naked twins’ strategy. 

- `utils.py` contains a set of functions that set the shape of the sudoku board, record the states of the boxes, and enable the game to be displayed.
- `solution.py` sets the rules of the game, and dictates the strategies the agent uses to play.
- `PySudoku.py`, `GameResources.py` and `SudokuSquare.py` use Pygame to generate a visual simulation of the resulting game of sudoku.

The initial code this is built on is part of Udacity’s Artificial Intelligence specialization, and can be found [here](https://github.com/udacity/artificial-intelligence/tree/master/Projects/1_Sudoku).

## Installation

Open an [Anaconda](https://www.continuum.io/downloads) environment in a terminal, and clone the GitHub repository:

`$ git clone https://github.com/elinorwahl/sudoku-solver.git`

Change the directory to the appropriate folder:

`$ cd sudoku-solver`

To allow this program to display a sudoku game in progress on a simulated board, an installation of Pygame is necessary. This can be challenging, especially for Mac users, and in-depth instructions for installing Pygame can be found [on the Pygame wiki](https://www.pygame.org/wiki/GettingStarted).

## Usage

To run the basic sudoku solver with visualization, execute the following command:

`$ python solution.py`

To test the solution code using additional sudoku puzzle examples:

`$ python test_solution.py`
