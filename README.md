# Sound Reaction Trainer for Track

A Python application to train and measure your reaction times to audio cues, simulating a track starter experience.

## Goal

This application aims to help track athletes improve their reaction times to starting signals. By practicing with this tool, athletes can:
- Develop faster response times to starting guns
- Train to avoid false starts
- Track their progress over time with data visualization
- Compare their reaction times with other users

## Quick Start

1. **Prerequisites**
   - Python 3.7 or higher
   - Required Python packages: pygame, keyboard, matplotlib, python-dotenv

2. **Installation**
   ```bash
   # Clone or download the repository
   # Install required packages
   pip install -r requirements.txt
   ```

3. **Setup**
   - Update `.env.example` file in the project root with:
     ```
     ROOT_DIR=/path/to/your/project
     ```
   - Create the following directory structure:
     ```
     /path/to/your/project/
     ├── sounds/
     │   ├── set/    # Place "set" audio files (.wav) here
     │   └── gun/    # Place "gun" audio files (.wav) here
     └── results/    # Results will be stored here
     ```

4. **Run the program**
   ```bash
   python reaction_timer.py
   ```

## How It Works

1. **Training Flow**
   - Enter your username to track your progress
   - Press ENTER to start each round
   - Wait for the "Set..." prompt and audio cue
   - After a random delay (1.5-2.5 seconds), the "GO!" prompt appears with a gunshot sound
   - Press SPACE as quickly as possible after hearing the gunshot
   - The program measures your reaction time in seconds
   - Press ENTER to continue to the next round, or 'q' to quit

2. **Features**
   - Reaction time measurement with millisecond precision
   - False start detection (pressing SPACE before the "GO!" signal)
   - Invalid reaction filtering (reactions under 0.099s or above 0.350s)
   - Session statistics with best, worst, and average times
   - Leaderboard showing top 5 reaction times across all users
   - Visual graph of reaction times throughout your session
   - Persistent storage of results for tracking progress over time

## Tips for Improving Your Reaction Time

- Focus on the sound, not the visual prompt
- Keep your finger ready but relaxed above the SPACE key
- Practice regularly to develop muscle memory
- Review your graphs to track progress over time
