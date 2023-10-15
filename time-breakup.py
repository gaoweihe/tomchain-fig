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
f, ax = plt.subplots(figsize=(9, 5))
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

sns.barplot(x='Category', y='Overall', data=breakup_df, color='red', label='Overall')
sns.barplot(x='Category', y='DistributeTime', data=breakup_df, color='blue', label='DistributeTime')
sns.barplot(x='Category', y='VoteTime', data=breakup_df, bottom=breakup_df['DistributeTime'], color='green', label='VoteTime')
sns.barplot(x='Category', y='CommitTime', data=breakup_df, bottom=breakup_df['DistributeTime'] + breakup_df['VoteTime'], color='yellow', label='CommitTime')

# Add labels, title, and legend
plt.xlabel('Category') 
plt.ylabel('Time (ms)')
plt.title('Time Break-up')
plt.legend()

plt.show()
plt.cla()

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

