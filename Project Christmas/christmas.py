import pandas as pd
import matplotlib.pyplot as plt  # for creating the chart

# Adjust these as needed
base_points = 10
extra_points_per_rank = 3
extra_points_per_apparition = 1  # 1 point per apparition
max_rank = 10  # maximum rank in any list (adjust if needed)

# Read data from Excel file
df = pd.read_excel('/Users/imeralvarenga/IT_HUB/Develop/Python/Programs/Project Christmas/songs.xlsx')

# Calculate average rank for each song
df['AvgRank'] = df.groupby('Song')['ListCount'].transform('mean')

# Calculate points for each song
def calculate_points(row):
    list_count = row['ListCount']
    song_rank = row['ListCount']
    rank_bonus = max_rank - song_rank + extra_points_per_rank
    repeat_bonus = list_count * extra_points_per_apparition
    return base_points + rank_bonus + repeat_bonus

# Update the calculate_points function with repeat_bonus calculation
df['Points'] = df.apply(calculate_points, axis=1)

# Normalize points by total participants
total_participants = len(df['ListCount'].unique())  # replace with actual participant count
df['Points'] /= total_participants

# Handle duplicate songs
df = df.groupby('Song').agg(Points=('Points', 'sum'), AvgRank=('AvgRank', 'mean')).reset_index()

# Sort DataFrame by Points and then AvgRank (for tie-breaking)
df_sorted = df.sort_values(by=['Points', 'AvgRank'], ascending=[False, True])

# Print the songs ordered by points and break ties with avg rank
for index, row in df_sorted.iterrows():
    song = row['Song']
    points = row['Points']
    avg_rank = row['AvgRank']
    print(f"{song} (#{int(avg_rank)}) - Points: {points:.2f}")

# Create a bar chart for visualization
plt.figure(figsize=(10, 6))  # adjust figure size if needed
#plt.bar(df_sorted['Song'], df_sorted['Points'], color='skyblue')
plt.bar(df_sorted['Song'], df_sorted['Points'], color='skyblue', label=f"{df_sorted['Song']} (#{df_sorted.index + 1})")
for i, v in enumerate(df_sorted['Points']):
    plt.text(i, v + 0.1, f"#{i + 1}", ha='center', va='bottom', fontsize=12)
plt.xlabel('Song')
plt.ylabel('Points')
plt.title('Christmas Song Countdown by Popularity')
plt.xticks(rotation=45, ha='right')  # rotate x-axis labels for better readability
plt.tight_layout()
plt.show()


# Optional: Visualization with libraries like matplotlib or Plotly

