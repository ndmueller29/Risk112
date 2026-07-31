# Risk112
 
A multi-player, offline implementation of the classic board game **Risk**, built in Python with a full graphical interface.

 <img width="800" height="479" alt="ScreenRecording2026-07-30at7 56 12PM-ezgif com-video-to-gif-converter" src="https://github.com/user-attachments/assets/8388e0d8-91b1-413a-b7c9-f18c18a99335" />
 
## About
 
Built as a term project for CMU's 15-112 (Fundamentals of Programming), this project recreates the strategy board game Risk from scratch, including:
 
- **Object-oriented programming** to model territories, players, and armies
- **Top-down design** to structure the game logic into clean, manageable components
- **Recursive backtracking** to determine whether a player could safely move armies between two territories without passing through enemy-controlled land
- **Pixel manipulation** to dynamically recolor the map — each territory was stored as a black-and-white image, and black pixels were recolored in real time to match the controlling player's color (my favorite part of the project)

## Demo

https://www.youtube.com/watch?v=Gdut6j3RYKI&t=2s

## How to run
 
This project uses [CMU Graphics](https://academy.cs.cmu.edu/desktop).
 
```bash
# Create a Python 3.10 environment (recommended)
conda create -n risk112 python=3.10
conda activate risk112
 
# Install dependencies
pip install cmu-graphics
 
# Run the game
python Risk112.py
```
 
## Built with
- Python
- [CMU Graphics](https://academy.cs.cmu.edu/desktop)

