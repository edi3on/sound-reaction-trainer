import os
import time
import random
import pygame
import keyboard
import matplotlib.pyplot as plt
import statistics
from datetime import datetime
from dotenv import load_dotenv

# Load .env
load_dotenv()
ROOT_DIR = os.getenv("ROOT_DIR")

# Validate root dir
if not ROOT_DIR or not os.path.exists(ROOT_DIR):
    raise ValueError("ROOT_DIR not set correctly in .env or doesn't exist.")

# Paths
SET_SOUND_DIR = os.path.join(ROOT_DIR, 'sounds', 'set')
GUN_SOUND_DIR = os.path.join(ROOT_DIR, 'sounds', 'gun')
RESULTS_FILE = os.path.join(ROOT_DIR, 'results', 'reactions.txt')

# Init pygame
pygame.mixer.init()

# Utility Functions
def get_random_sound(path):
    files = [f for f in os.listdir(path) if f.endswith('.wav')]
    return os.path.join(path, random.choice(files)) if files else None

def play_sound(sound_path):
    if sound_path:
        sound = pygame.mixer.Sound(sound_path)
        sound.play()
        return sound
    return None

def stop_sound(sound_obj):
    if sound_obj:
        sound_obj.stop()

def log_result(username, round_num, reaction_time):
    os.makedirs(os.path.dirname(RESULTS_FILE), exist_ok=True)
    with open(RESULTS_FILE, 'a') as f:
        f.write(f"{username}, Round {round_num}, {reaction_time:.3f} sec, {datetime.now()}\n")

def parse_results():
    if not os.path.exists(RESULTS_FILE):
        return {}
    users = {}
    with open(RESULTS_FILE, 'r') as f:
        for line in f:
            parts = line.strip().split(',')
            if len(parts) >= 3:
                user = parts[0].strip()
                time_sec = float(parts[2].split()[0])
                if user not in users:
                    users[user] = []
                users[user].append(time_sec)
    return users

def show_leaderboard(users):
    print("\n🏆 Leaderboard - Fastest Reactions (unique sessions):")
    all_stats = [(user, min(times), statistics.median(times)) for user, times in users.items() if len(times) > 0]
    top5 = sorted(all_stats, key=lambda x: x[1])[:5]
    for i, (user, best, med) in enumerate(top5, 1):
        print(f"{i}. {user} - Best: {best:.3f} sec | Median: {med:.3f} sec")

def show_graph(username, times):
    plt.figure(figsize=(10, 5))
    plt.plot(times, marker='o', label='Reaction Time (s)')
    plt.title(f"{username}'s Reaction Times")
    plt.xlabel('Round')
    plt.ylabel('Time (seconds)')
    plt.ylim(0, max(times) + 0.2)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

# Main Session
def main():
    print("🎯 Reaction Timer: Track Starter Mode")
    username = input("Enter your username: ").strip()
    print("\nInstructions:")
    print("- Press SPACE *only* after the gun sound.")
    print("- Pressing before the gun = False Start!")
    print("- Press ENTER to start each round. Type 'q' after any round to quit.\n")

    round_num = 1
    reaction_times = []

    while True:
        input(f"Round {round_num}: Press ENTER to get ready...")

        print("Set...")
        set_sound = play_sound(get_random_sound(SET_SOUND_DIR))
        wait_time = random.uniform(1.5, 2.5)

        start = time.time()
        false_start = False

        while time.time() - start < wait_time:
            if keyboard.is_pressed('space'):
                false_start = True
                break
            time.sleep(0.01)

        if false_start:
            print("🚫 False start! You pressed too early.")
            time.sleep(1.5)
            stop_sound(set_sound)
            continue

        stop_sound(set_sound)
        print("GO!")
        gun_sound = play_sound(get_random_sound(GUN_SOUND_DIR))
        start_time = time.time()

        while True:
            if keyboard.is_pressed('space'):
                reaction = time.time() - start_time
                break
            time.sleep(0.001)

        stop_sound(gun_sound)

        if 0.099 <= reaction <= 0.350:
            reaction_times.append(reaction)
            log_result(username, round_num, reaction)
            avg_time = sum(reaction_times) / len(reaction_times)
            med_time = statistics.median(reaction_times)
            print(f"✅ Reaction Time: {reaction:.3f} sec | Avg: {avg_time:.3f} sec | Median: {med_time:.3f} sec")
        else:
            print(f"🚫 Invalid reaction time ({reaction:.3f} sec). Try again.")

        round_num += 1
        next_action = input("Press ENTER to continue or 'q' to quit: ").strip().lower()
        if next_action == 'q':
            break

    print("\n📊 Session Summary:")
    if reaction_times:
        print(f"Rounds played: {len(reaction_times)}")
        print(f"Best: {min(reaction_times):.3f} sec")
        print(f"Worst: {max(reaction_times):.3f} sec")
        print(f"Average: {sum(reaction_times)/len(reaction_times):.3f} sec")
        print(f"Median: {statistics.median(reaction_times):.3f} sec")
    else:
        print("No valid reaction times recorded.")

    all_users = parse_results()
    show_leaderboard(all_users)
    if reaction_times:
        show_graph(username, reaction_times)

if __name__ == "__main__":
    main()
