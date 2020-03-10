import json
import urllib.request
import uuid

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

sns.set(color_codes=True)

host = "http://localhost"
envoy_port = "8080"
envoy_admin_port = "9901"
envoy_admin_url = "%s:%s/clusters?format=json" % (host, envoy_admin_port)

cluster_name = "echo_cluster"

# get all instance_ids
response = json.loads(urllib.request.urlopen(envoy_admin_url).read())
echo_cluster = next(x for x in response['cluster_statuses'] if x['name'] == cluster_name)

distribution_count = {}

# fill distribution dict
for x in echo_cluster['host_statuses']:
    port = x['address']['socket_address']['port_value']
    response = str(urllib.request.urlopen("%s:%s" % (host, port)).read())
    instance_id = response[20:32]
    distribution_count[instance_id] = 0

id_key = uuid.uuid4()
req = urllib.request.Request("%s:%s/echo/key/%s" % (host, envoy_port, id_key))

for x in range(500):
    response = str(urllib.request.urlopen(req).read())
    instance_id = response[20:32]
    if instance_id in distribution_count:
        distribution_count[instance_id] = distribution_count[instance_id] + 1

fake = pd.DataFrame({'instance_id': list(distribution_count.keys()), 'requests': list(distribution_count.values())})
fig = sns.barplot(x='instance_id', y='requests', data=fake, color='blue')
plt.title("requests distribution")
plt.show()
