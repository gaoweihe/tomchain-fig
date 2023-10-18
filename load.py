# import enum
from pandas import DataFrame
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg', force=True)
sns.set_theme(style="whitegrid")
sns.set_style({'font.family': 'Times New Roman'})

f, ax1 = plt.subplots(figsize=(9, 5))
sns.despine(fig=None, ax=None, top=True, right=True, left=False, bottom=False, offset=None, trim=False)

console_out = open("log/load.log") 
all_lines = console_out.readlines() 
df_index = []
cpu = []
ram = []
io = []
network_tx = []
network_rx = []
sample_count = 0
for index, line in enumerate(all_lines): 
	# CPU
	if (line.find("PM     all") != -1): 
		str_list = line.split("PM     all") 
		str_list = str_list[1].split()
		df_index.append(sample_count)
		cpu.append(float(str_list[0]))
		sample_count = sample_count + 1
	
    # network
	if (line.find("PM      eno4") != -1): 
		str_list = line.split("PM      eno4") 
		str_list = str_list[1].split()
		network_rx.append(float(str_list[2]))
		network_tx.append(float(str_list[3]))
        
console_out.close() 

print(df_index.__len__())
print(cpu.__len__())
print(network_rx.__len__())
print(network_tx.__len__())

cpu_df = DataFrame({'index': df_index, 'cpu': cpu})
network_rx_df = DataFrame({'index': df_index, 'network_rx': network_rx})
network_tx_df = DataFrame({'index': df_index, 'network_tx': network_tx})

line_color = 'gray'
bar_width = 0.4
ticks_fontsize = 13
labels_fontsize = 16
legend_fontsize = 13
title_fontsize = 17

# Drawing lines
# plt.plot(df.index, df['cpu'], marker='o', label='CPU')
# plt.plot(df.index, df['network_rx'], marker='o', label='network_rx')
# plt.plot(df.index, df['network_tx'], marker='o', label='network_tx')
ax1 = sns.lineplot(x='index', y='cpu', data=cpu_df, ax=ax1, label='CPU', marker='x', color=line_color)
ax1.set_xlabel('Time (s)', fontsize=labels_fontsize)
ax1.set_ylabel(r'Load (%)', fontsize=labels_fontsize)
ax1.set_xticks([0, 20, 40, 60, 80, 100])
ax1.set_ylim(0, 100)
# sns.lineplot(x='index', y='network_rx', data=network_rx_df, label='network_rx', marker='o')
# sns.lineplot(x='index', y='network_tx', data=network_tx_df, label='network_tx', marker='o')

ax2 = ax1.twinx() 
sns.lineplot(x='index', y='network_rx', data=network_rx_df, ax=ax2, label='network_rx', marker='o', color=line_color)
sns.lineplot(x='index', y='network_tx', data=network_tx_df, ax=ax2, label='network_tx', linestyle=':', marker='o', color=line_color)
ax2.set_ylabel(r'Network (kB/s)', fontsize=labels_fontsize)

ax1.legend(loc='upper left', fontsize=legend_fontsize)
ax2.legend(loc='upper right', fontsize=legend_fontsize)

# Adding title and labels
plt.title('System Loads', fontsize=title_fontsize)

# Adding legend, which helps differentiate lines A and B
plt.legend(fontsize=legend_fontsize)

# Show plot
plt.show()

print(cpu)
print(network_rx)
print(network_tx)