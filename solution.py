output = []

def get_row_relation(row, user_ids, memory):
    current_user_id = row.get("Id")
    if current_user_id not in memory:
        memory.append(current_user_id)
        
        order_id = row.get("OrderId")
        email = row.get("Email")
        phone = row.get("Phone")
        
        if order_id == "" and email == "" and phone == "":
            return user_ids

        if order_id != "":
            orderid_link_df = df.loc[(df["OrderId"] == order_id) & (df["Id"] != current_user_id)]
            user_ids = user_ids.union(orderid_link_df["Id"].unique())
            for _, oi_row in orderid_link_df.iterrows():
                user_ids = user_ids.union(get_row_relation(oi_row, user_ids, memory))

        if email != "":
            email_link_df = df.loc[(df["Email"] == email) & (df["Id"] != current_user_id)]
            user_ids = user_ids.union(email_link_df["Id"].unique())
            for _, email_row in email_link_df.iterrows():
                user_ids = user_ids.union(get_row_relation(email_row, user_ids, memory))

        if phone != "":
            phone_link_df = df.loc[(df["Phone"] == phone) & (df["Id"] != current_user_id)]
            user_ids = user_ids.union(phone_link_df["Id"].unique())
            for _, phone_row in phone_link_df.iterrows():
                user_ids = user_ids.union(get_row_relation(phone_row, user_ids, memory))
    
    return user_ids

for _, row in tqdm(df.iterrows(), total=df.shape[0]):
    current_user_id = row.get("Id")
    order_id = row.get("OrderId")
    email = row.get("Email")
    phone = row.get("Phone")
    
    user_ids = {current_user_id}
    
    memory = []
    
    # Noise
    if order_id == "" and email == "" and phone == "":
        output.append({"id": current_user_id, "trace": str(user_ids)})
        continue

    user_ids = user_ids.union(get_row_relation(row, user_ids, memory))
        
#     if order_id != "":
#         orderid_link_df = df.loc[(df["OrderId"] == order_id) & (df["Id"] != current_user_id)]
#         # If relation found.
#         if orderid_link_df.shape[0] > 0:
#             user_ids = user_ids.union(orderid_link_df["Id"].unique())
#             for _, oi_row in orderid_link_df.iterrows():
#                 user_ids = user_ids.union(get_row_relation(oi_row, user_ids, memory))
            
#     if email != "":
#         email_link_df = df.loc[(df["Email"] == email) & (df["Id"] != current_user_id)]
#         # If relation found.
#         if email_link_df.shape[0] > 0:
#             user_ids = user_ids.union(email_link_df["Id"].unique())
#             for _, email_row in email_link_df.iterrows():
#                 user_ids = user_ids.union(get_row_relation(email_row, user_ids, memory))
        
#     if phone != "":
#         phone_link_df = df.loc[(df["Phone"] == phone) & (df["Id"] != current_user_id)]
#         # If relation found.
#         if phone_link_df.shape[0] > 0:
#             user_ids = user_ids.union(phone_link_df["Id"].unique())
#             for _, phone_row in phone_link_df.iterrows():
#                 user_ids = user_ids.union(get_row_relation(phone_row, user_ids, memory))

    output.append({"id": current_user_id, "trace": str(sorted(user_ids))})
    
    if current_user_id > 24:
        break
