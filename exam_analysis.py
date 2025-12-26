import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

os.makedirs("data", exist_ok=True)
os.makedirs("plots", exist_ok=True)

# Generate synthetic exam data
np.random.seed(42)
students = range(1, 101)
questions = range(1, 21)
records = []

for student in students:
    for question in questions:
        difficulty = np.random.choice(['Easy', 'Medium', 'Hard'], p=[0.4,0.35,0.25])
        attempts = np.random.randint(1,4)
        correct = np.random.choice([0,1], p=[0.4,0.6])
        time_taken = np.random.randint(30,300)
        records.append([student, question, difficulty, attempts, correct, time_taken])

df = pd.DataFrame(records, columns=['student_id','question_id','difficulty','attempts','correct','time_taken'])
df.to_csv("data/exam_data.csv", index=False)

print("Dataset created:")
print(df.head())

# Overall success rate
overall_success = df['correct'].mean() * 100
print(f"Overall Success Rate: {overall_success:.2f}%")

# Success rate by difficulty
difficulty_success = df.groupby('difficulty')['correct'].mean() * 100
print("Success Rate by Difficulty:")
print(difficulty_success)

# Plot: Difficulty vs Success Rate
plt.figure(figsize=(8,5))
sns.barplot(x=difficulty_success.index, y=difficulty_success.values, palette='viridis')
plt.title("Success Rate by Question Difficulty")
plt.xlabel("Difficulty")
plt.ylabel("Success Rate (%)")
plt.savefig("plots/difficulty_success_rate.png")
plt.show()

# Attempts vs Correct
plt.figure(figsize=(8,5))
sns.countplot(x="attempts", hue="correct", data=df)
plt.title("Attempts vs Correct Answers")
plt.savefig("plots/attempts_vs_correct.png")
plt.show()

# Time Taken vs Difficulty
plt.figure(figsize=(8,5))
sns.boxplot(x="difficulty", y="time_taken", data=df)
plt.title("Time Taken vs Difficulty Level")
plt.savefig("plots/time_vs_difficulty.png")
plt.show()

# Summary stats
summary = df.groupby('difficulty').agg({'correct':['mean','sum'], 'attempts':'mean', 'time_taken':'mean'})
print("Difficulty-wise Statistical Summary:")
print(summary)
