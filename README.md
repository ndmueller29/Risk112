# Risk112
 
A multi-player, offline implementation of the classic board game **Risk**, built in Python with a full graphical interface.
 
<img width="1298" height="775" alt="Risk112_screenshot" src="https://github.com/user-attachments/assets/e297215d-e65e-4b1c-9bb2-dc5f54e6a27f" />

 
## About
 
Built as a term project for CMU's 15-112 (Fundamentals of Programming), this project recreates the strategy board game Risk from scratch, including:
 
- **Object-oriented programming** to model territories, players, and armies
- **Top-down design** to structure the game logic into clean, manageable components
- **Recursive backtracking** to determine whether a player could safely move armies between two territories without passing through enemy-controlled land
- **Pixel manipulation** to dynamically recolor the map — each territory was stored as a black-and-white image, and black pixels were recolored in real time to match the controlling player's color (my favorite part of the project)
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
 
