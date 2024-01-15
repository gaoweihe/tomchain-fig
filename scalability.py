import pandas
import pandas as pd
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg', force=True)
sns.set_theme(style="whitegrid")
sns.set_style({'font.family': 'Times New Roman'})

# Create individual dataframes. In practice, these might come from different sources or computations.
# Here, we're just creating some example data.

f, ax = plt.subplots(figsize=(9, 5))
sns.despine(fig=None, ax=None, top=True, right=True, left=False, bottom=False, offset=None, trim=False)

console_out = open("log/scalability/2servers.out") 
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
throughput_original_df_2 = pandas.DataFrame({'index': x, 'cb': y})
throughput_original_df_2['cb'] = throughput_original_df_2['cb'].diff()
throughput_original_df_2 = throughput_original_df_2[throughput_original_df_2['cb'] >= 7500]
throughput_original_df_2 = throughput_original_df_2.tail(40)
throughput_original_df_2 = throughput_original_df_2.head(20)
throughput_original_df_2['index'] = throughput_original_df_2['index'] - 44

console_out = open("log/scalability/3servers.out") 
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

throughput_original_df_4 = pandas.DataFrame({'index': x, 'cb': y})
throughput_original_df_4['cb'] = throughput_original_df_4['cb'].diff()
# throughput_original_df_4 = throughput_original_df_4[throughput_original_df_4['cb'] >= 6500]
throughput_original_df_4 = throughput_original_df_4.tail(40)
throughput_original_df_4 = throughput_original_df_4.head(20)
throughput_original_df_4['index'] = throughput_original_df_4['index'] - 56

console_out = open("log/scalability/9servers.out") 
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

throughput_original_df_8 = pandas.DataFrame({'index': x, 'cb': y})
throughput_original_df_8['cb'] = throughput_original_df_8['cb'].diff()
# throughput_original_df_8 = throughput_original_df_8[throughput_original_df_8['cb'] >= 6500]
throughput_original_df_8 = throughput_original_df_8.tail(40)
throughput_original_df_8 = throughput_original_df_8.head(20)
throughput_original_df_8['index'] = throughput_original_df_8['index'] - 104


# First dataset
data1 = {
    'x_values': throughput_original_df_2['index'],
    'y_values': throughput_original_df_2['cb']
}
df1 = pd.DataFrame(data1)

# Second dataset
data2 = {
    'x_values': throughput_original_df_4['index'],
    'y_values': throughput_original_df_4['cb']
}
df2 = pd.DataFrame(data2)

# Third dataset
data3 = {
    'x_values': throughput_original_df_8['index'],
    'y_values': throughput_original_df_8['cb']
}
df3 = pd.DataFrame(data3)

line_color = 'gray'
line_width = 0.4
ticks_fontsize = 13
labels_fontsize = 16
legend_fontsize = 13
title_fontsize = 17

# Plotting the first line
sns.lineplot(x='x_values', y='y_values', data=df1, label='9', marker='o', color=line_color)

# Plotting the second line
sns.lineplot(x='x_values', y='y_values', data=df2, label='6', marker='x', color=line_color)

# Plotting the third line
sns.lineplot(x='x_values', y='y_values', data=df3, label='3', marker='*', linestyle=':', color=line_color)

# Customizing the visuals
plt.title('Scalability', fontsize=title_fontsize)
plt.xlabel('Time (s)', fontsize=labels_fontsize)  # Custom x-axis title
plt.ylabel('TPS', fontsize=labels_fontsize)  # Custom y-axis title
plt.xlim(0, 80)
plt.ylim(0, 10000)
plt.legend(title='#DN', fontsize=legend_fontsize)  # Adding a legend with a title

# Displaying the plot
plt.show()
