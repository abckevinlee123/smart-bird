import pickle
import utility

# --- Load the saved thought processes ---
with open("../saved_tp/best.pkl", "rb") as f:  # Replace with your actual filename
    thought_processes = pickle.load(f)

# --- Sort by fitness_score descending ---
sorted_processes = sorted(thought_processes, key=lambda tp: tp['fitness_score'], reverse=True)

# --- Print top 10 scores ---
print("Top 10 Fitness Scores:")
for rank, tp in enumerate(sorted_processes[:10], start=1):
    print(f"{rank}: {tp['fitness_score']}")

utility.visualize_thought_process(sorted_processes[0])  # Visualize the best thought process