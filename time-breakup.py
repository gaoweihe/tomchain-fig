# import enum
import pandas
from pandas import DataFrame
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg', force=True)
sns.set_theme(style="whitegrid")
sns.set_style({'font.family': 'Times New Roman'})

# performance break-up 
fig, axs = plt.subplots(1, 2, figsize=(9, 5))
sns.despine(fig=None, ax=None, top=True, right=True, left=False, bottom=False, offset=None, trim=False)
console_out = open("server-9.out")
all_lines = console_out.readlines()
x = []
proposal = []
dist = []
commit = []
recv = []
base_timestamp = 0
sample_count = 0
for index, line in enumerate(all_lines):
    if (line.find("SPBcastCommit block=") != -1):
        str_list = line.split("proposal_ts=")
        str_list = str_list[1].split(", ")
        proposal_ts = int(str_list[0].strip('\n'))
        if (sample_count == 0): 
            base_timestamp = proposal_ts - 10000
        proposal_ts = proposal_ts - base_timestamp
		
        str_list = line.split("dist_ts=")
        str_list = str_list[1].split(", ")
        dist_ts = int(str_list[0].strip('\n')) - base_timestamp
		
        str_list = line.split("commit_ts=")
        str_list = str_list[1].split(", ")
        commit_ts = int(str_list[0].strip('\n')) - base_timestamp
		
        str_list = line.split("recv_ts=")
        str_list = str_list[1].split(", ")
        recv_ts = int(str_list[0].strip('\n')) - base_timestamp

        print(sample_count, " ", "proposal:", proposal_ts, "dist:", dist_ts, "commit:", commit_ts, "recv:", recv_ts, flush=True)
        x.append(sample_count)
        proposal.append(proposal_ts) 
        dist.append(dist_ts)
        commit.append(commit_ts)
        recv.append(recv_ts)
        sample_count = sample_count + 1

console_out.close()

tomchain_original_df = DataFrame({'index': x, 'proposal': proposal, 'dist': dist, 'commit': commit, 'recv': recv})
tomchain_avg_proposal = tomchain_original_df['proposal'].mean()
tomchain_avg_dist = tomchain_original_df['dist'].mean()
tomchain_avg_commit = tomchain_original_df['commit'].mean()
tomchain_avg_recv = tomchain_original_df['recv'].mean()

tomchain_dist_time = tomchain_avg_dist - tomchain_avg_proposal
tomchain_commit_time = tomchain_avg_commit - tomchain_avg_dist
tomchain_recv_time = tomchain_avg_recv - tomchain_avg_commit

breakup_data = {
    'Category': ['TomChain', 'Blockene', 'SBFT'],
    'Overall': [0, 0, 254], 
    'DistributeTime': [tomchain_dist_time, 5000, 0],
    'VoteTime': [tomchain_commit_time, 35000, 0], 
    'CommitTime': [tomchain_recv_time, 10000, 0]
}
breakup_df = DataFrame(breakup_data)

# pie chart 
# Setting the overall aesthetics
sns.set_theme(style="whitegrid")

# Sample data
data1 = {'Categories': ['Distribute', 'Vote', 'Commit'], 'Values': [abs(tomchain_dist_time), abs(tomchain_commit_time), abs(tomchain_recv_time)]}
data2 = {'Categories': ['Distribute', 'Vote', 'Commit'], 'Values': [5000, 35000, 10000]}
# data3 = {'Categories': ['G', 'H', 'I'], 'Values': [25, 35, 40]}

df1 = pandas.DataFrame(data1)
df2 = pandas.DataFrame(data2)
# df3 = pandas.DataFrame(data3)

# Create a color palette
# colors = sns.color_palette("viridis", 3)
hatches = ['/', '\\', '|', '-']
pie_color = ['gray']
font_properties = {'family': 'Times New Roman'}
ticks_fontsize = 13
labels_fontsize = 16
legend_fontsize = 13
title_fontsize = 17

# Create the first pie chart using data from df1
axs[0].pie(df1['Values'], labels=df1['Categories'], autopct='%1.1f%%', startangle=90, colors=pie_color)
axs[0].set_title('TMCD', fontsize=title_fontsize)
axs[0].axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

# Create the second pie chart using data from df2
axs[1].pie(df2['Values'], labels=df2['Categories'], autopct='%1.1f%%', startangle=90, colors=pie_color)
axs[1].set_title('Blockene', fontsize=title_fontsize)
axs[1].axis('equal')

# # Create the third pie chart using data from df3
# axs[2].pie(df3['Values'], labels=df3['Categories'], autopct='%1.1f%%', startangle=90, colors=colors)
# axs[2].set_title('SBFT')
# axs[2].axis('equal')

# Improve spacing between subplots
plt.tight_layout()

# Show the plot
plt.show()

# bar chart 
# bar_color = 'gray'
# bar_width = 0.4
# ticks_fontsize = 13
# labels_fontsize = 16
# legend_fontsize = 13
# title_fontsize = 17

# # Define different hatch patterns for each segment within each bar
# hatches = ['///', '+++','xxx', '\\\\\\', '---', '***', '...', 'ooo']

# overall_plot = sns.barplot(x='Category', y='Overall', data=breakup_df, label='Overall', width=bar_width, color=bar_color)
# dist_plot = sns.barplot(x='Category', y='DistributeTime', data=breakup_df, label='DistributeTime', width=bar_width, color=bar_color)
# vote_plot = sns.barplot(x='Category', y='VoteTime', data=breakup_df, bottom=breakup_df['DistributeTime'], label='VoteTime', width=bar_width, color=bar_color)
# commit_plot = sns.barplot(x='Category', y='CommitTime', data=breakup_df, bottom=breakup_df['DistributeTime'] + breakup_df['VoteTime'], label='CommitTime', width=bar_width, color=bar_color)
# plots = [overall_plot, dist_plot, vote_plot, commit_plot]

# for curr_plot in plots:
#     # Applying hatches to each bar segment
#     total_bars = len(curr_plot.patches)
#     for i, bar in enumerate(curr_plot.patches):
#         # Calculate the appropriate hatch pattern for this bar segment
#         pattern = hatches[i % len(hatches)]
#         # Skip the bars from the first set (bottom layer), as they are already drawn
#         if i < total_bars:
#             pass
#             # continue
    
#         # Apply the hatch pattern to the bar segment
#         bar.set_hatch(pattern)

# # Add labels, title, and legend
# plt.xticks(fontsize=ticks_fontsize)  # x tick labels
# plt.yticks(fontsize=ticks_fontsize)  # y tick labels
# plt.xlabel('Category', fontsize=labels_fontsize) 
# plt.ylabel('Time (ms)', fontsize=labels_fontsize)
# # plt.yscale('log')
# plt.title('Time Break-up', fontsize=title_fontsize)
# plt.legend(fontsize=legend_fontsize)

# plt.show()
# plt.cla()

# line plot 
# performance_df = DataFrame({'index': x, 'proposal': proposal, 'dist': dist, 'commit': commit, 'recv': recv})
# for col in performance_df.columns:
#     performance_df[col] = performance_df[col].sort_values().values
# print(performance_df)

# performance_plot = sns.lineplot(data=performance_df[['proposal', 'dist', 'commit', 'recv']], linewidth=1)
# performance_plot.set(xlabel='#block',
#        ylabel='time (ms)',title='Performance Break-up')
# plt.show()
# plt.cla() 

