# Minesweeper

A Python implementation of the classic **Minesweeper** game.  
This project focuses on implementing the **core game logic**, including board generation, mine placement, and cell-revealing mechanics.

---

## 🎮 Features

- Grid-based Minesweeper board
- Random mine placement
- Adjacent mine counting
- Recursive revealing of empty cells
- Game win and loss detection
- Console-based gameplay

---

## 🛠️ Technologies Used

- **Python 3**
- Standard Python libraries only

---

## 📂 Project Structure

Minesweeper/
```├── pycache/          # Python bytecode cache (auto-generated)
├── .venv/                # Virtual environment (not required to run)
├── assets/
│   ├── flag.png          # Flag image
│   └── mine.png          # Mine image
├── cell.py               # Cell logic and state
├── ms_board.py           # Board generation and mine logic
├── game.py               # Game controller and rules
├── minesweeper.py        # Main entry point
└── README.md
```
---

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher installed on your machine

### Running the Game

Clone the repository and run the game:

```bash
git clone https://github.com/newwereper/Minesweeper.git
cd Minesweeper
python minesweeper.py
