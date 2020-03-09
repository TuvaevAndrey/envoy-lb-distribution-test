import urllib.request

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

sns.set(color_codes=True)

distribution_count = {}

url = "http://localhost:8080/echo"

for x in range(500):
    response = str(urllib.request.urlopen(url).read())
    instance_id = response[20:32]
    if instance_id in distribution_count:
        distribution_count[instance_id] = distribution_count[instance_id] + 1
    else:
        distribution_count[instance_id] = 0

fake = pd.DataFrame({'instance_id': list(distribution_count.keys()), 'requests': list(distribution_count.values())})
fig = sns.barplot(x='instance_id', y='requests', data=fake, color='blue')
plt.title("requests distribution")
plt.show()
