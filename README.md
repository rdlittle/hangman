# Cheat the Hangman

Its a game in which you guess letters in order to reveal the secret word. (I need to explain this?).  

I got the solution on how to animate a gif with tkinter from this video: https://www.youtube.com/watch?v=lYIy4nJd7P8

## Features
* Tracks which letters you guessed
* Bars you from guessing the same letter twice
* Awards one credit toward buying a vowel when a correct letter is guessed
* Disables all the vowel buttons unless buying a vowel
* When buying a vowel, temporarily enables the vowel buttons and disables the consonant buttons

## Requires
* python 3
* pillow

## Installation
------------
You may need to install pillow

Try
    pip install --user -r requirements.txt

Or
    pip install --user pillow

## Known issues
* On Windows, the letter buttons do not extend the full width of the game board.

## To Play
### From the command line:

Linux:

python hangman.py 

Windows:

py hangman.py
