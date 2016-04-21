import matplotlib.pyplot as plt
import numpy as np


# Pie diagram
labels = ['Popular categories used', 'Popular categories missed']
values = [67,163]
plt.subplot(aspect=True)
plt.pie(values,colors=['r','b'],labels=labels)
plt.show()