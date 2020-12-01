
import numpy as np
import matplotlib.pyplot as plt 
import seaborn as sns

def get_data():

    base_cond1 = [5,6,7,8]
    base_cond2= [10,2,7,9]
    base_cond3 = [4,7,4,1]
    base_cond4 = [5,6,7,8]

    return base_cond1, base_cond2, base_cond3

results= get_data()
fig= plt.figure()

xdata= np.array([0,1,2,3,4,5,6])/5



sns.set_theme(style="darkgrid")

# Load an example dataset with long-form data
fmri = sns.load_dataset("fmri")
print(fmri)

# Plot the responses for different events and regions
sns.lineplot(x="timepoint", y="signal",
             hue="region", style="event",
             data=fmri)

plt.show()
