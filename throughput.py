# import enum
from pandas import DataFrame
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg', force=True)
sns.set_theme(style="whitegrid")
sns.set_style({'font.family': 'Times New Roman'})

# throughput
f, ax = plt.subplots(figsize=(9, 5))
sns.despine(fig=None, ax=None, top=True, right=True, left=False, bottom=False, offset=None, trim=False)

console_out = open("server-9.out") 
all_lines = console_out.readlines() 
x = []
y = []
sample_count = 0
for index, line in enumerate(all_lines): 
	if (line.find("cb:") != -1): 
		str_list = line.split("cb:") 
		print(sample_count, " ", str_list[1].strip('\n'), flush=True)
		# csv_writer.writerow([str_list[1]])
		x.append(sample_count * 4)
		y.append(int(str_list[1]) * 2000 / 4)
		sample_count = sample_count + 1
console_out.close() 

throughput_original_df = DataFrame({'index': x, 'cb': y})
throughput_original_df['cb'] = throughput_original_df['cb'].diff()

# get average throughput from throughput_df
tomchain_avg_throughput = throughput_original_df['cb'].mean() 
# get max value of throughput from throughput_df
tomchain_max_throughput = throughput_original_df['cb'].max()
# get min value of throughput from throughput_df
tomchain_min_throughput = throughput_original_df['cb'].min()

throughput_data = {
    'Category':     ['TomChain', 'Blockene', 'Algorand', 'SBFT', 'PBFT', 'Ethereum', 'Bitcoin'],
    'TPS':          [tomchain_avg_throughput, 2000, 1000, 378, 204, 10, 7],
    'MaxValues':    [tomchain_max_throughput, 2000, 1000, 378, 204, 10, 7],
    'MinValues':    [tomchain_min_throughput, 2000, 1000, 378, 204, 10, 7]
}
throughput_df = DataFrame(throughput_data, columns=['Category', 'TPS', 'MaxValues', 'MinValues'])
throughput_df['PositiveError'] = throughput_df['MaxValues'] - throughput_df['TPS']
throughput_df['NegativeError'] = throughput_df['TPS'] - throughput_df['MinValues']
throughput_yerr = [throughput_df['NegativeError'].values, throughput_df['PositiveError'].values]

throughput_plot = sns.barplot(x='Category', y='TPS', data=throughput_df, yerr=throughput_yerr, capsize=0.2)
throughput_plot.set(xlabel='Category',
         ylabel='TPS',
         title='Throughput')
plt.yscale('log')
plt.show()
plt.cla() 

# # scatter plot 
# throughput_plot = sns.scatterplot(x="index", y="cb",
#                 data=throughput_df, linewidth=0)
# throughput_plot.set(xlabel='time (s)',
#        ylabel='TPS',
#        title='Throughput')

# plt.xlabel('time (s)')
# plt.ylabel('TPS')
# plt.show()
# plt.cla() 

# # latency
# f, ax = plt.subplots(figsize=(9, 5))
# sns.despine(fig=None, ax=None, top=True, right=True, left=False, bottom=False, offset=None, trim=False)
# console_out = open("server-9.out") 
# all_lines = console_out.readlines() 
# x = []
# y = []
# sample_count = 0
# for index, line in enumerate(all_lines): 
# 	if (line.find("SPBcastCommit blockid=") != -1 or line.find("LocalCommit blockid=") != -1): 
# 		str_list = line.split("latency=") 
# 		print(sample_count, " ", str_list[1].strip('\n'), flush=True)
# 		x.append(sample_count)
# 		y.append(int(str_list[1]))
# 		sample_count = sample_count + 1
# console_out.close() 

# latency_df = DataFrame({'index': x, 'latency': y})
# print(latency_df)

# latency_plot = sns.scatterplot(x="index", y="latency",
#                 data=latency_df, linewidth=0)
# latency_plot.set(xlabel='#block',
#        ylabel='latency (ms)',
#        title='Latency')
# plt.show()
# plt.cla() 

# # performance break-up 
# f, ax = plt.subplots(figsize=(9, 5))
# sns.despine(fig=None, ax=None, top=True, right=True, left=False, bottom=False, offset=None, trim=False)
# console_out = open("server-9.out")
# all_lines = console_out.readlines()
# x = []
# proposal = []
# dist = []
# commit = []
# recv = []
# base_timestamp = 0
# sample_count = 0
# for index, line in enumerate(all_lines):
#     if (line.find("SPBcastCommit block=") != -1):
#         str_list = line.split("proposal_ts=")
#         str_list = str_list[1].split(", ")
#         proposal_ts = int(str_list[0].strip('\n'))
#         if (sample_count == 0): 
#             base_timestamp = proposal_ts - 10000
#         proposal_ts = proposal_ts - base_timestamp
		
#         str_list = line.split("dist_ts=")
#         str_list = str_list[1].split(", ")
#         dist_ts = int(str_list[0].strip('\n')) - base_timestamp
		
#         str_list = line.split("commit_ts=")
#         str_list = str_list[1].split(", ")
#         commit_ts = int(str_list[0].strip('\n')) - base_timestamp
		
#         str_list = line.split("recv_ts=")
#         str_list = str_list[1].split(", ")
#         recv_ts = int(str_list[0].strip('\n')) - base_timestamp

#         print(sample_count, " ", "proposal:", proposal_ts, "dist:", dist_ts, "commit:", commit_ts, "recv:", recv_ts, flush=True)
#         x.append(sample_count)
#         proposal.append(proposal_ts) 
#         dist.append(dist_ts)
#         commit.append(commit_ts)
#         recv.append(recv_ts)
#         sample_count = sample_count + 1

# console_out.close()

# performance_df = DataFrame({'index': x, 'proposal': proposal, 'dist': dist, 'commit': commit, 'recv': recv})
# for col in performance_df.columns:
#     performance_df[col] = performance_df[col].sort_values().values
# print(performance_df)

# performance_plot = sns.lineplot(data=performance_df[['proposal', 'dist', 'commit', 'recv']], linewidth=1)
# performance_plot.set(xlabel='#block',
#        ylabel='time (ms)',title='Performance Break-up')
# plt.show()
# plt.cla() 
