import pandas as pd
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
matplotlib.use('TkAgg', force=True)
sns.set_theme(style="whitegrid")
sns.set_style({'font.family': 'Times New Roman'})

# Create individual dataframes. In practice, these might come from different sources or computations.
# Here, we're just creating some example data.

# TMCD
# data1 = {
#     'x_values': [600, 550, 1030, 1100, 1070, 1078, 1152, 1112, 1011, 1520, 2170],  # 1 to 100
#     'y_values': [78, 125, 240, 370, 400, 700, 2100, 3013, 3695, 6843, 7630]  # Some calculation to generate values
# }
data1 = {
    'x_values': [78, 125, 240, 400, 700, 2100, 3013, 6843, 7630],
    'y_values': [600, 550, 1030, 1070, 1078, 1112, 1152, 1520, 2170]
}
df1 = pd.DataFrame(data1)

# SBFT
data2 = {
    'x_values': [16, 141, 250, 438, 500, 516],
    'y_values': [205, 220, 240, 280, 360, 450]
}
df2 = pd.DataFrame(data2)

# Third dataset
data3 = {
    'x_values': [1, 2],
    'y_values': [3, 4]
}
df3 = pd.DataFrame(data3)

line_color = 'gray'
bar_width = 0.4
ticks_fontsize = 13
labels_fontsize = 16
legend_fontsize = 13
title_fontsize = 17

# Create a new figure with a certain size
plt.figure(figsize=(9, 5))

# Plotting the first line
sns.lineplot(x='x_values', y='y_values', data=df1, label='TMCD', marker='*', color=line_color)

# Plotting the second line
sns.lineplot(x='x_values', y='y_values', data=df2, label='SBFT', marker='o', color=line_color)

# # Plotting the third line
# sns.lineplot(x='x_values', y='y_values', data=df3, label='Line 3', marker='x')

# plt.rcParams['font.sans-serif'] = ['SimSun']

# Customizing the visuals
plt.title('吞吐量与延迟的取舍', fontsize=title_fontsize)
plt.xlabel('延迟（毫秒）', fontsize=labels_fontsize)  # Custom x-axis title
plt.ylabel('交易吞吐量', fontsize=labels_fontsize)  # Custom y-axis title
plt.legend(title='类别', fontsize=legend_fontsize)  # Adding a legend with a title

# Displaying the plot
plt.show()
