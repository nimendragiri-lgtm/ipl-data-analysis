# IPL Data Analysis & Visualization
# Dataset: IPL Matches (Kaggle) - matches.csv
# Author: Nimendra Giri

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = 150
plt.rcParams['font.family'] = 'DejaVu Sans'

# using matplotlib's default color cycle here
COLORS = ['#1f77b4','#ff7f0e','#2ca02c','#d62728','#9467bd',
          '#8c564b','#e377c2','#7f7f7f','#bcbd22','#17becf']

# load the data
df = pd.read_csv('matches.csv')

print(f"Loaded {df.shape[0]} matches across {df['season'].nunique()} seasons")
print(f"Seasons: {df['season'].min()} to {df['season'].max()}")
print(f"\nColumns: {list(df.columns)}")
print("\nFirst few rows:")
print(df.head())

# check for missing values
missing = df.isnull().sum()
print("\nMissing values:")
print(missing[missing > 0])

# some teams changed names over the years, standardising them
team_name_map = {
    'Delhi Daredevils': 'Delhi Capitals',
    'Deccan Chargers': 'Sunrisers Hyderabad',
    'Rising Pune Supergiant': 'Rising Pune Supergiants',
}
for col in ['team1', 'team2', 'winner', 'toss_winner']:
    df[col] = df[col].replace(team_name_map)

# drop the 4 no-result matches, they're not useful here
df = df[df['result'] != 'no result'].copy()
print(f"\nAfter cleaning: {df.shape[0]} matches")


# --- Plot 1: which teams have won the most? ---

win_counts = df['winner'].value_counts().head(10)

plt.figure(figsize=(12, 6))
bars = plt.barh(win_counts.index[::-1], win_counts.values[::-1], color=COLORS[:10][::-1])
for bar, val in zip(bars, win_counts.values[::-1]):
    plt.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2,
             str(val), va='center', fontsize=10, fontweight='bold')
plt.title('Top 10 Most Successful IPL Teams (Total Wins)', fontsize=14, fontweight='bold', pad=15)
plt.xlabel('Number of Wins', fontsize=11)
plt.ylabel('Team', fontsize=11)
plt.tight_layout()
plt.savefig('plot1_most_successful_teams.png', bbox_inches='tight')
plt.show()
print("saved plot1")


# --- Plot 2: how many matches per season? ---

season_matches = df.groupby('season').size().reset_index(name='matches')

plt.figure(figsize=(12, 5))
plt.plot(season_matches['season'], season_matches['matches'],
         marker='o', color='#1f77b4', linewidth=2.5, markersize=8)
plt.fill_between(season_matches['season'], season_matches['matches'], alpha=0.15, color='#1f77b4')
for x, y in zip(season_matches['season'], season_matches['matches']):
    plt.annotate(str(y), (x, y), textcoords="offset points", xytext=(0, 8), ha='center', fontsize=9)
plt.title('Number of IPL Matches Played Per Season', fontsize=14, fontweight='bold', pad=15)
plt.xlabel('Season', fontsize=11)
plt.ylabel('Total Matches', fontsize=11)
plt.xticks(season_matches['season'], rotation=45)
plt.tight_layout()
plt.savefig('plot2_matches_per_season.png', bbox_inches='tight')
plt.show()
print("saved plot2")


# --- Plot 3: toss analysis ---

toss_decision = df['toss_decision'].value_counts()

fig, axes = plt.subplots(1, 2, figsize=(13, 5))
fig.suptitle('Toss Analysis', fontsize=14, fontweight='bold')

axes[0].pie(toss_decision.values, labels=toss_decision.index,
            autopct='%1.1f%%', colors=['#2ecc71', '#e74c3c'],
            startangle=90, textprops={'fontsize': 12})
axes[0].set_title('Toss Decision: Bat vs Field', fontsize=12)

# check if toss winner actually goes on to win the match
df['toss_match_winner'] = df['toss_winner'] == df['winner']
toss_win_result = df['toss_match_winner'].value_counts()

axes[1].pie(toss_win_result.values, labels=['Won Match', 'Lost Match'],
            autopct='%1.1f%%', colors=['#3498db', '#e67e22'],
            startangle=90, textprops={'fontsize': 12})
axes[1].set_title('Did Toss Winner Win the Match?', fontsize=12)

plt.tight_layout()
plt.savefig('plot3_toss_analysis.png', bbox_inches='tight')
plt.show()
print("saved plot3")


# --- Plot 4: which venues host the most games? ---

top_venues = df['venue'].value_counts().head(8)

plt.figure(figsize=(12, 5))
sns.barplot(x=top_venues.values, y=top_venues.index, palette='Blues_r')
plt.title('Top 8 IPL Venues by Matches Hosted', fontsize=14, fontweight='bold', pad=15)
plt.xlabel('Number of Matches', fontsize=11)
plt.ylabel('Venue', fontsize=11)
for i, v in enumerate(top_venues.values):
    plt.text(v + 0.5, i, str(v), va='center', fontsize=10)
plt.tight_layout()
plt.savefig('plot4_top_venues.png', bbox_inches='tight')
plt.show()
print("saved plot4")


# --- Plot 5: player of the match leaders ---

top_players = df['player_of_match'].value_counts().head(10)

plt.figure(figsize=(11, 5))
sns.barplot(x=top_players.index, y=top_players.values, palette='rocket_r')
plt.title("Top 10 'Player of the Match' Award Winners", fontsize=14, fontweight='bold', pad=15)
plt.xlabel('Player', fontsize=11)
plt.ylabel('Awards Won', fontsize=11)
plt.xticks(rotation=30, ha='right')
for i, v in enumerate(top_players.values):
    plt.text(i, v + 0.2, str(v), ha='center', fontsize=10, fontweight='bold')
plt.tight_layout()
plt.savefig('plot5_top_players.png', bbox_inches='tight')
plt.show()
print("saved plot5")


# --- Plot 6: win margins (runs vs wickets) ---

bat_first_wins = df[df['win_by_runs'] > 0]['win_by_runs']
chase_wins = df[df['win_by_wickets'] > 0]['win_by_wickets']

fig, axes = plt.subplots(1, 2, figsize=(13, 5))
fig.suptitle('How Teams Win — Margin Analysis', fontsize=14, fontweight='bold')

axes[0].hist(bat_first_wins, bins=20, color='#e74c3c', edgecolor='white', alpha=0.85)
axes[0].axvline(bat_first_wins.mean(), color='black', linestyle='--',
                label=f'Mean: {bat_first_wins.mean():.1f} runs')
axes[0].set_title('Win by Runs (Batting First)', fontsize=12)
axes[0].set_xlabel('Runs Margin', fontsize=10)
axes[0].set_ylabel('Frequency', fontsize=10)
axes[0].legend()

axes[1].hist(chase_wins, bins=10, color='#2ecc71', edgecolor='white', alpha=0.85)
axes[1].axvline(chase_wins.mean(), color='black', linestyle='--',
                label=f'Mean: {chase_wins.mean():.1f} wickets')
axes[1].set_title('Win by Wickets (Chasing)', fontsize=12)
axes[1].set_xlabel('Wickets Margin', fontsize=10)
axes[1].set_ylabel('Frequency', fontsize=10)
axes[1].legend()

plt.tight_layout()
plt.savefig('plot6_win_margins.png', bbox_inches='tight')
plt.show()
print("saved plot6")


# --- Plot 7: win % by team (only teams with 30+ matches) ---

all_teams = pd.concat([df['team1'], df['team2']]).value_counts()
wins = df['winner'].value_counts()
win_pct = (wins / all_teams * 100).dropna().round(1)
win_pct = win_pct[all_teams >= 30].sort_values(ascending=False)

plt.figure(figsize=(12, 5))
sns.barplot(x=win_pct.index, y=win_pct.values, palette='viridis')
plt.axhline(50, color='red', linestyle='--', linewidth=1.5, label='50% Win Rate')
plt.title('Team Win Percentage in IPL (min. 30 matches played)', fontsize=13, fontweight='bold', pad=15)
plt.xlabel('Team', fontsize=11)
plt.ylabel('Win %', fontsize=11)
plt.xticks(rotation=30, ha='right')
plt.legend()
for i, v in enumerate(win_pct.values):
    plt.text(i, v + 0.5, f'{v}%', ha='center', fontsize=9, fontweight='bold')
plt.tight_layout()
plt.savefig('plot7_team_win_percentage.png', bbox_inches='tight')
plt.show()
print("saved plot7")


# quick summary of what we found
print("\n--- Key Insights ---")
print(f"Most wins: {win_counts.index[0]} ({win_counts.iloc[0]} wins)")

best_season = season_matches.loc[season_matches['matches'].idxmax()]
print(f"Busiest season: {int(best_season['season'])} ({int(best_season['matches'])} matches)")

field_pct = toss_decision.get('field', 0) / toss_decision.sum() * 100
print(f"Teams chose to field first {field_pct:.1f}% of the time")

toss_win_pct = toss_win_result.get(True, 0) / toss_win_result.sum() * 100
print(f"Toss winners won the match {toss_win_pct:.1f}% of the time")

print(f"Most used venue: {top_venues.index[0]} ({top_venues.iloc[0]} matches)")
print(f"Most POTM awards: {top_players.index[0]} ({top_players.iloc[0]})")
print(f"Avg win by runs: {bat_first_wins.mean():.1f} | Avg win by wickets: {chase_wins.mean():.1f}")
