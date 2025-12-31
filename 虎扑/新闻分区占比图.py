import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')
df = pd.read_csv('虎扑新闻数据.csv')

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

#统计每个分区的数量

top_counts = df['topicName'].value_counts().head(10)

#绘制饼图
plt.figure(figsize=(8, 8))

colors = plt.cm.Set3.colors
plt.pie(top_counts,labels=top_counts.index,autopct='#1.1f%%',colors=colors)
plt.title('新闻分区占比')
#使饼图比例相同
plt.axis('equal')
plt.savefig('新闻分区占比饼图')















































