# Flappy Bird 

This is a complete Flappy Bird game clone built using Python and Pygame.

It includes smooth gameplay, background animation, pipe generation, sounds, and both start/game over screens. Perfectly tuned for desktop play.

## Features

- Playable Flappy Bird physics (realistic jump & fall)
- Animated bird with flapping wings
- Scrolling background & ground
- Randomly generated pipes with gaps
- Sound effects (flap, point, crash)
- Start screen and game over screen
- Restart and quit options after game over

## Controls

| Key        | Action              |
|------------|---------------------|
| SPACE      | Jump / Start Game   |
| R          | Restart after Game Over |
| Q          | Quit after Game Over |

## Folder Structure

```
mitali2004/
├── FlappyBird.py        # Main game file
├── README.md            # This file
├── images/              # Game assets (background, pipes, bird)
│   ├── bird1.png
│   ├── bird2.png
│   ├── bird3.png
│   ├── pipe.png
│   ├── base.png
│   └── bg.png
└── sounds/              # Sound effects
    ├── wing.wav
    ├── point.wav
    └── hit.wav
```

## Requirements

- Python 3.6+
- Pygame library

### Install Dependencies
```bash
pip install pygame
```

## How to Run

1. Make sure you're in the project folder (mitali2004)
2. Run the game:
```bash
python FlappyBird.py
```

## Notes

- Make sure your images/ and sounds/ folders are present and contain all the required files.
- Sound files must be in .wav format.

## Credits

Built by mitali2004  
Inspired by the original Flappy Bird by Dong Nguyen

Sound sources:
- pixabay.com/sound-effects
- zapsplat.com
- freesound.org
