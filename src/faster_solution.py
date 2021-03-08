import numpy as np
import pandas as pd
from tqdm import tqdm


memory = {}
clusters = {}


def add_to_memory(user_id, value):
    if value != "":
        if value in memory:
            memory[value].add(user_id)
            return
        memory[value] = {user_id}


def main():
    df = pd.read_json('contacts.json')
    npdata = df.values

    print(df.head())
    
    for row in tqdm(npdata, total=npdata.shape[0]):
        user_id = row[0]
        add_to_memory(user_id, row[4])
        add_to_memory(user_id, row[1])
        add_to_memory(user_id, row[2])
        
    for _, ids in tqdm(memory.items(), total=len(memory.items())):
        temp_cluster = set(ids)
        
        # Check if any of these ids have cluster.
        for uid in ids:
            if uid in clusters:
                temp_cluster.update(clusters[uid])
        
        for uid in temp_cluster:
            clusters[uid] = temp_cluster

    output = []

    for user_id, trace in tqdm(sorted(clusters.items()), total=len(clusters.items())):
        contacts = np.sum(npdata[list(trace), 3])
        trace = "-".join([str(trace) for trace in sorted(trace)])
        answer = "{},{}".format(trace, contacts)
        output.append({"ticket_id": user_id,  "ticket_trace/contact": answer})

    output_df = pd.DataFrame(output)
    print(output_df.head(20))

    filename = input("Save as: ")
    output_df.to_csv(filename, index=False)


main()
