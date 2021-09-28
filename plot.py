import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df=pd.read_csv('Electric four-wheelers models available in market.csv')
xvalue=df.Manufacturer
yvalue=df.Driving
fig, ax = plt.subplots()

y_pos = np.arange(len(xvalue))
error = np.random.rand(len(xvalue))

ax.barh(y_pos, yvalue ,xerr=error, align='center')
ax.set_yticks(y_pos)
ax.set_yticklabels(xvalue)
ax.invert_yaxis()  # labels read top-to-bottom
ax.set_xlabel('Driving range (km/full charge')
ax.set_ylabel('Manufacturer/Models (Cars')

plt.show()
