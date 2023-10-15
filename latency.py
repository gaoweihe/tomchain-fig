# import enum
from pandas import DataFrame
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg', force=True)
sns.set_theme(style="whitegrid")
sns.set_style({'font.family': 'Times New Roman'})

# # latency
f, ax = plt.subplots(figsize=(9, 5))
sns.despine(fig=None, ax=None, top=True, right=True, left=False, bottom=False, offset=None, trim=False)
console_out = open("server-9.out") 
all_lines = console_out.readlines() 
x = []
y = []
sample_count = 0
for index, line in enumerate(all_lines): 
	if (line.find("SPBcastCommit blockid=") != -1 or line.find("LocalCommit blockid=") != -1): 
		str_list = line.split("latency=") 
		print(sample_count, " ", str_list[1].strip('\n'), flush=True)
		x.append(sample_count)
		y.append(int(str_list[1]))
		sample_count = sample_count + 1
console_out.close() 

latency_original_df = DataFrame({'index': x, 'latency': y})
latency_original_df = latency_original_df.iloc[15:]

# get average throughput from throughput_df
tomchain_avg_latency = latency_original_df['latency'].mean() 
# get max value of throughput from throughput_df
tomchain_max_latency = latency_original_df['latency'].max()
# get min value of throughput from throughput_df
tomchain_min_latency = latency_original_df['latency'].min()

# bar plot 
latency_data = {
    'Category': ['TomChain', 'Blockene', 'Algorand', 'SBFT', 'PBFT', 'Ethereum'],
    'Latency': [tomchain_avg_latency, 90000, 18000, 254, 538, 12000],
    'MaxValues': [tomchain_max_latency, 90000, 20000, 254, 538, 12000],
    'MinValues': [tomchain_min_latency, 90000, 16000, 254, 538, 12000]
}
throughput_df = DataFrame(latency_data, columns=['Category', 'Latency', 'MaxValues', 'MinValues'])
throughput_df['PositiveError'] = throughput_df['MaxValues'] - throughput_df['Latency']
throughput_df['NegativeError'] = throughput_df['Latency'] - throughput_df['MinValues']
throughput_yerr = [throughput_df['NegativeError'].values, throughput_df['PositiveError'].values]

throughput_plot = sns.barplot(x='Category', y='Latency', data=throughput_df, yerr=throughput_yerr, capsize=0.2)
throughput_plot.set(xlabel='Category',
         ylabel='Latency (ms)',
         title='Latency')
plt.show()
plt.cla() 

# scatter plot
# latency_plot = sns.scatterplot(x="index", y="latency",
#                 data=latency_df, linewidth=0)
# latency_plot.set(xlabel='#block',
#        ylabel='latency (ms)',
#        title='Latency')
# plt.show()
# plt.cla() 


# throughput
# f, ax = plt.subplots(figsize=(9, 5))
# sns.despine(fig=None, ax=None, top=True, right=True, left=False, bottom=False, offset=None, trim=False)

# console_out = open("server-9.out") 
# all_lines = console_out.readlines() 
# x = []
# y = []
# sample_count = 0
# for index, line in enumerate(all_lines): 
# 	if (line.find("cb:") != -1): 
# 		str_list = line.split("cb:") 
# 		print(sample_count, " ", str_list[1].strip('\n'), flush=True)
# 		# csv_writer.writerow([str_list[1]])
# 		x.append(sample_count * 4)
# 		y.append(int(str_list[1]) * 2000 / 4)
# 		sample_count = sample_count + 1
# console_out.close() 

# throughput_original_df = DataFrame({'index': x, 'cb': y})
# throughput_original_df['cb'] = throughput_original_df['cb'].diff()

# # get average throughput from throughput_df
# tomchain_avg_throughput = throughput_original_df['cb'].mean() 
# # get max value of throughput from throughput_df
# tomchain_max_throughput = throughput_original_df['cb'].max()
# # get min value of throughput from throughput_df
# tomchain_min_throughput = throughput_original_df['cb'].min()

# throughput_data = {
#     'Category': ['TomChain', 'Blockene', 'Algorand', 'SBFT', 'Ethereum', 'Bitcoin'],
#     'TPS': [tomchain_avg_throughput, 23, 45, 67, 0, 0],
#     'MaxValues': [tomchain_max_throughput, 26, 49, 72, 0, 0],
#     'MinValues': [tomchain_min_throughput, 20, 42, 60, 0, 0]
# }
# throughput_df = DataFrame(throughput_data, columns=['Category', 'TPS', 'MaxValues', 'MinValues'])
# throughput_df['PositiveError'] = throughput_df['MaxValues'] - throughput_df['TPS']
# throughput_df['NegativeError'] = throughput_df['TPS'] - throughput_df['MinValues']
# throughput_yerr = [throughput_df['NegativeError'].values, throughput_df['PositiveError'].values]

# throughput_plot = sns.barplot(x='Category', y='TPS', data=throughput_df, yerr=throughput_yerr, capsize=0.2)
# throughput_plot.set(xlabel='Category',
#          ylabel='TPS',
#          title='Throughput')
# plt.show()
# plt.cla() 