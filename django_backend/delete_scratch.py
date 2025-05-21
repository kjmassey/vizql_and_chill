import csv
import pandas as pd
import random
import time

import tableauserverclient as TSC
from tableau.creds.tableau_creds import PAT_NAME, PAT_SECRET, POD_URL, SITE_NAME

with open("./luids_for_deletes.csv", "r") as f:
    reader = csv.DictReader(f)
    data = list(reader)

    for row in data:
        # Convert the 'size' field to an integer
        row["size"] = int(row["size"])

    total_space_saved_mb = 0
    large_items_mb = 0
    medium_items_mb = 0
    small_items_mb = 0

    row_count = len(data)

    ids_chosen = []
    luids_to_delete = []

    print("About to enter while loop")
    while total_space_saved_mb < 4000:
        print("Space saved so far: ", total_space_saved_mb)

        # Get 800 mb from large items
        while large_items_mb < 1000:
            filtered_data = [row for row in data if int(row["size"]) >= 150]
            rand_index = random.randint(0, len(filtered_data) - 1)

            row_id = filtered_data[rand_index]["id"]

            if not row_id in ids_chosen:
                print("Chosen ID: ", row_id)
                ids_chosen.append(row_id)
                luids_to_delete.append(data[int(row_id) - 1]["luid"])

                large_items_mb += int(data[int(row_id) - 1]["size"])
                print("Large Items MB: ", large_items_mb)

                new_found = True

            else:
                print("Have to loop again for a unique number...")

            time.sleep(0.25)

        # Get 2.5 gb from medium items
        while medium_items_mb < 2500:
            filtered_data = [
                row for row in data if int(row["size"]) >= 25 and int(row["size"]) < 150
            ]
            rand_index = random.randint(0, len(filtered_data) - 1)

            row_id = filtered_data[rand_index]["id"]

            if not row_id in ids_chosen:
                print("Chosen ID: ", row_id)
                ids_chosen.append(row_id)
                luids_to_delete.append(data[int(row_id) - 1]["luid"])

                medium_items_mb += int(data[int(row_id) - 1]["size"])
                print("Medium Items MB: ", medium_items_mb)

                new_found = True

            else:
                print("Have to loop again for a unique number...")

            time.sleep(0.25)

        # Get 700 mb from small items
        while small_items_mb < 500:
            filtered_data = [row for row in data if int(row["size"]) < 25]
            rand_index = random.randint(0, len(filtered_data) - 1)

            row_id = filtered_data[rand_index]["id"]

            if not row_id in ids_chosen:
                print("Chosen ID: ", row_id)
                ids_chosen.append(row_id)
                luids_to_delete.append(data[int(row_id) - 1]["luid"])

                small_items_mb += int(data[int(row_id) - 1]["size"])
                print("Small Items MB: ", small_items_mb)

                new_found = True

            else:
                print("Have to loop again for a unique number...")

            time.sleep(0.25)

        total_space_saved_mb = large_items_mb + medium_items_mb + small_items_mb

print("Total Space Saved: ", total_space_saved_mb)

server = TSC.Server(POD_URL, use_server_version=True)
tab_auth = TSC.PersonalAccessTokenAuth(PAT_NAME, PAT_SECRET, site_id=SITE_NAME)

with server.auth.sign_in(tab_auth):
    for luid in luids_to_delete:
        try:
            print("Deleting item with LUID: ", luid)
            server.workbooks.delete(luid)
        except Exception as e:
            print("Error deleting item with LUID: ", luid)
            print(e)

# # Get 3 gb from medium items
# while medium_items_mb < 3000:

#     if total_space_saved_mb < 5000:
#         filtered_data = [
#             row
#             for row in data
#             if int(row["size"]) >= 25 and int(row["size"]) < 300
#         ]
#         rand_index = random.randint(0, len(filtered_data) - 1)

#         row_id = filtered_data[rand_index]["id"]

#         if not row_id in ids_chosen:
#             print("Chosen ID: ", row_id)
#             ids_chosen.append(row_id)

#             medium_items_mb += int(data[int(row_id) - 1]["size"])
#             total_space_saved_mb += medium_items_mb
#             print("Total Space Saved: ", total_space_saved_mb)
#             print("Medium Items MB: ", medium_items_mb)

#             new_found = True

#         else:
#             print("Have to loop again for a unique number...")

#     time.sleep(0.25)

# new_found = False

# while not new_found:
#     rand_id = random.randint(0, row_count - 1)

#     if not rand_id in ids_chosen:
#         ids_chosen.append(rand_id)
#         print("Chosen ID: ", rand_id)

#         new_found = True

#     else:
#         print("Have to loop again for a unique number...")

# space_saved_mb += int(data[rand_id]["size"])

# time.sleep(0.25)

# print("+++++ # IDs Chosen: ", len(ids_chosen))
# print("+++++ Space Saved: ", space_saved_mb)
