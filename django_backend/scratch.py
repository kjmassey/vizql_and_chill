import tableauserverclient as TSC
import csv


from tableau.creds.tableau_creds import PAT_NAME, PAT_SECRET, POD_URL, SITE_NAME

server = TSC.Server(POD_URL, use_server_version=True)
tab_auth = TSC.PersonalAccessTokenAuth(PAT_NAME, PAT_SECRET, site_id=SITE_NAME)

items = []

with server.auth.sign_in(tab_auth):
    all_workbooks = list(TSC.Pager(server.workbooks))
    all_views = list(TSC.Pager(server.views))
    all_datasources = list(TSC.Pager(server.datasources))

    for workbook in all_workbooks:
        items.append(
            {
                "luid": workbook.id,
                "name": workbook.name,
                "type": "workbook",
            }
        )

    print("GOT WORKBOOKS")

    for view in all_views:
        items.append(
            {
                "luid": view.id,
                "name": view.name,
                "type": "view",
                "workbook": view.workbook_id,
            }
        )

    print("GOT VIEWS")

    for datasource in all_datasources:
        items.append(
            {
                "luid": datasource.id,
                "name": datasource.name,
                "type": "datasource",
            }
        )

    print("GOT DATASOURCES")

    with open("tableau_items.csv", "w", newline="") as csvfile:
        fieldnames = ["luid", "name", "type", "workbook"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for item in items:
            writer.writerow(item)
