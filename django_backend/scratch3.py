# REQUEST

import requests

url = r"https://10ax.online.tableau.com/api/v1/vizql-data-service/read-metadata"
api_token = "PjNwzWw2TEyK7NN8cpVjKw|LDvcI0683Uta4Raw3u8imOEbrqz9yJ8S|f8dbec1d-2217-42b0-868a-229a2ff090bb"

headers = {
    "content-type": "application/json",
    "X-Tableau-Auth": api_token,
}

ds_luid = "b9eb0dff-d2e4-4658-a051-676f2318cadf"

req_body = {"datasource": {"datasourceLuid": ds_luid}}

resp = requests.post(
    url,
    headers=headers,
    json=req_body,
)

print(resp.json())

with open("scratch3.json", "w") as f:
    f.write(resp.text)
