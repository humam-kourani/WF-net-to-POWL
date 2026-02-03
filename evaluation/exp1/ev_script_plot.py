import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

y_axis = 'Size (|Transitions| + |Places|)'

file_path = r"C:\Users\kourani\PycharmProjects\WF-to-POWL\evaluation\exp1\statistics_time_summary.csv"
df = pd.read_csv(file_path)

df_sorted = df.sort_values(by=y_axis)

x = df_sorted[y_axis]
y1 = df_sorted['WF-to-tree converter']
y2 = df_sorted['WF-to-POWL converter']
y3 = df_sorted['WF-to-POWL-2.0 converter']

poly_fit_1 = np.polyfit(x, y1, 2)
poly_fit_2 = np.polyfit(x, y2, 2)
poly_fit_3 = np.polyfit(x, y3, 2)

trend_1 = np.polyval(poly_fit_1, x)
trend_2 = np.polyval(poly_fit_2, x)
trend_3 = np.polyval(poly_fit_3, x)

plt.figure(figsize=(6, 2.8))

plt.scatter(x, y1, color='r', label='WF-to-tree converter', marker='.')
plt.scatter(x, y2, color='b', label='WF-to-POWL converter', marker='x', s=40)
plt.scatter(x, y3, color='g', label='WF-to-POWL-2.0 converter', marker='+', s=40)

plt.plot(x, trend_1, color='r')
plt.plot(x, trend_2, color='b')
plt.plot(x, trend_3, color='g')

plt.xlabel(y_axis)
plt.ylabel('Time (sec)')

plt.legend()
plt.tight_layout()

plt.grid(True)
plt.savefig(r"C:\Users\kourani\PycharmProjects\WF-to-POWL\evaluation\exp1\ev_time_powl20.png",
            dpi=300,
            bbox_inches="tight")
plt.show()