import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

y_axis = 'Size (|Transitions| + |Places|)'

file_path = r"C:\Users\kourani\PycharmProjects\WF-to-POWL\evaluation\exp1\statistics.csv"
df = pd.read_csv(file_path)

df_sorted = df.sort_values(by=y_axis)

x = df_sorted[y_axis]
y1 = df_sorted['WF-to-POWL converter']
y2 = df_sorted['WF-to-tree coverter']

poly_fit_1 = np.polyfit(x, y1, 2)
poly_fit_2 = np.polyfit(x, y2, 2)

trend_1 = np.polyval(poly_fit_1, x)
trend_2 = np.polyval(poly_fit_2, x)

plt.figure(figsize=(12, 4))

plt.scatter(x, y1, color='b', label='WF-to-POWL converter', marker='o')
plt.scatter(x, y2, color='r', label='WF-to-tree converter', marker='s')

plt.plot(x, trend_1, color='b')
plt.plot(x, trend_2, color='r')

plt.xlabel(y_axis)
plt.ylabel('Time (sec)')

plt.legend()

plt.grid(True)
plt.show()