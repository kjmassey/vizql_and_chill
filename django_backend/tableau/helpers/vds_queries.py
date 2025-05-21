def all_content_query(ds_luid: str, initial=False) -> dict:
    """
    Query the Site Content datasource and return all fields
    """

    print("++++ DS LUID: ", ds_luid)

    all_content_query = {
        "datasource": {"datasourceLuid": f"{ds_luid}"},
        "options": {"debug": True},
        "query": {
            "fields": [
                {"fieldCaption": "Created At (Local)"},
                {"fieldCaption": "Extracts Incremented At (Local)"},
                {"fieldCaption": "Extracts Refreshed At (Local)"},
                {"fieldCaption": "First Published At (Local)"},
                {"fieldCaption": "Last Published At (Local)"},
                {"fieldCaption": "Last Accessed At (Local)"},
                {"fieldCaption": "Updated At (Local)"},
                {"fieldCaption": "Admin Insights Published At"},
                {"fieldCaption": "Controlled Permissions Enabled"},
                {"fieldCaption": "Controlling Permissions Project LUID"},
                {"fieldCaption": "Controlling Permissions Project Name"},
                {"fieldCaption": "Metric Definition Data Source ID"},
                {"fieldCaption": "Has Definition Filters"},
                {"fieldCaption": "Metric Definition Aggregation"},
                {"fieldCaption": "Metric Definition Number Format"},
                {"fieldCaption": "Created At"},
                {"fieldCaption": "Data Source Content Type"},
                {"fieldCaption": "Data Source Database Type"},
                {"fieldCaption": "Data Source Is Certified"},
                {"fieldCaption": "Description"},
                {"fieldCaption": "Extracts Incremented At"},
                {"fieldCaption": "Extracts Refreshed At"},
                {"fieldCaption": "First Published At"},
                {"fieldCaption": "Has Incrementable Extract"},
                {"fieldCaption": "Has Refresh Scheduled"},
                {"fieldCaption": "Has Refreshable Extract"},
                {"fieldCaption": "Is Data Extract"},
                {"fieldCaption": "Item Hyperlink"},
                {"fieldCaption": "Item ID"},
                {"fieldCaption": "Item LUID"},
                {"fieldCaption": "Item Name"},
                {"fieldCaption": "Item Parent Project ID"},
                {"fieldCaption": "Item Parent Project Level"},
                {"fieldCaption": "Item Parent Project Name"},
                {"fieldCaption": "Item Parent Project Owner Email"},
                {"fieldCaption": "Item Revision"},
                {"fieldCaption": "Item Type"},
                {"fieldCaption": "Last Accessed At"},
                {"fieldCaption": "Last Published At"},
                {"fieldCaption": "Adjustable Filter Options"},
                {"fieldCaption": "Nested Projects Permissions Enabled"},
                {"fieldCaption": "Owner Email"},
                {"fieldCaption": "Project Level"},
                {"fieldCaption": "Metric Definition ID for Related Metric"},
                {"fieldCaption": "Metric Time Granularity"},
                {"fieldCaption": "Site Hyperlink"},
                {"fieldCaption": "Site LUID"},
                {"fieldCaption": "Site Name"},
                {"fieldCaption": "Size (bytes)"},
                {"fieldCaption": "Size (MB)"},
                {"fieldCaption": "Storage Quota (bytes)"},
                {"fieldCaption": "Top Parent Project Name"},
                {"fieldCaption": "Total Size (bytes)"},
                {"fieldCaption": "Total Size (MB)"},
                {"fieldCaption": "Updated At"},
                {"fieldCaption": "View Title"},
                {"fieldCaption": "View Type"},
                {"fieldCaption": "View Workbook ID"},
                {"fieldCaption": "View Workbook Name"},
                {"fieldCaption": "Workbook Shows Sheets As Tabs"},
            ]
        },
    }

    if initial:
        all_content_query["query"]["filters"] = [
            {
                "field": {"fieldCaption": "Item Type"},
                "filterType": "SET",
                "values": ["View"],
                "context": True,
            },
            {
                "field": {"fieldCaption": "Updated At"},
                "filterType": "TOP",
                "howMany": 250,
                "fieldToMeasure": {"fieldCaption": "Updated At", "function": "MAX"},
                "direction": "TOP",
            },
        ]

    return all_content_query


def query_single_item_from_site_content(ds_luid: str, item_luid: str) -> dict:
    """
    Query the Site Content datasource for a single item. Return luid, name, type and url
    """

    single_item_query = {
        "datasource": {"datasourceLuid": ds_luid},
        "options": {"debug": True},
        "query": {
            "fields": [
                {"fieldCaption": "Item LUID", "fieldAlias": "luid"},
                {"fieldCaption": "Item Name", "fieldAlias": "name"},
                {"fieldCaption": "Item Type", "fieldAlias": "type"},
                {"fieldCaption": "Item Hyperlink", "fieldAlias": "url"},
            ],
            "filters": [
                {
                    "field": {"fieldCaption": "Item LUID"},
                    "filterType": "SET",
                    "values": [item_luid],
                }
            ],
        },
    }

    return single_item_query
