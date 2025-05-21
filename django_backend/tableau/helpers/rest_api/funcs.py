import tableauserverclient as TSC
import requests

from tableau.helpers.vds_queries import (
    all_content_query,
    query_single_item_from_site_content,
)
from tableau.creds.tableau_creds import POD_URL, SITE_NAME, PAT_NAME, PAT_SECRET
import json
import base64
import math
from rest_framework.response import Response
import traceback
from tableau.helpers.jwt import generate_login_jwt


def get_server_and_auth(
    url: str, site_name: str, pat_name=None, pat_secret=None, jwt=None
) -> tuple:
    """
    Get Tableau Server and Tableau Auth objects
    """

    server = TSC.Server(url, use_server_version=True)

    if pat_name and pat_secret:
        tab_auth = TSC.PersonalAccessTokenAuth(pat_name, pat_secret, site_id=site_name)

    elif jwt:
        tab_auth = TSC.TableauAuth(jwt_token=jwt, site_id=site_name)

    return server, tab_auth


def get_datasource_metadata(ds_dict: dict) -> dict:
    """
    Get VDS metadata of a datasource
    """

    server, tab_auth = get_server_and_auth(
        ds_dict["url"],
        ds_dict["site_name"],
        pat_name=ds_dict["pat_name"],
        pat_secret=ds_dict["pat_secret"],
    )

    with server.auth.sign_in(tab_auth):
        token = server.auth_token
        headers = {
            "X-Tableau-Auth": token,
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        req_url = f"{ds_dict['url']}/api/v1/vizql-data-service/read-metadata"
        req_body = {"datasource": {"datasourceLuid": ds_dict["luid"]}}

        response = requests.post(req_url, headers=headers, json=req_body, verify=False)

        return response.json()


def get_datasources(ds_dict: dict) -> dict:
    """
    Get datasources
    """

    server, tab_auth = get_server_and_auth(
        ds_dict["url"],
        ds_dict["site_name"],
        pat_name=ds_dict["pat_name"],
        pat_secret=ds_dict["pat_secret"],
    )

    with server.auth.sign_in(tab_auth):
        all_datasources = list(TSC.Pager(server.datasources))

        return [d.__dict__ for d in all_datasources]


def do_vds_query(query_dict: dict) -> dict:
    """
    Perform VDS query
    """

    server, tab_auth = get_server_and_auth(
        query_dict["url"],
        query_dict["site_name"],
        pat_name=query_dict["pat_name"],
        pat_secret=query_dict["pat_secret"],
    )

    with server.auth.sign_in(tab_auth):
        token = server.auth_token
        headers = {
            "X-Tableau-Auth": token,
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        req_url = f"{query_dict['url']}/api/v1/vizql-data-service/query-datasource"
        req_body = query_dict["query"]

        response = requests.post(req_url, headers=headers, json=req_body, verify=False)

        return response.json()


def do_site_content_query(ds_dict: dict) -> dict:
    """
    Perform Site Content query
    """

    query_dict = {
        "url": POD_URL,
        "site_name": SITE_NAME,
        "pat_name": PAT_NAME,
        "pat_secret": PAT_SECRET,
        "query": all_content_query(
            ds_dict["ds_luid"], initial=ds_dict.get("initial", False)
        ),
    }

    return do_vds_query(query_dict)


def do_single_item_query(ds_dict: dict) -> dict:
    """
    Perform single item query
    """

    query_dict = {
        "url": POD_URL,
        "site_name": SITE_NAME,
        "pat_name": PAT_NAME,
        "pat_secret": PAT_SECRET,
        "query": query_single_item_from_site_content(
            ds_dict["ds_luid"], ds_dict["item_luid"]
        ),
    }

    return do_vds_query(query_dict)


def get_workbook_preview_image(wb_dict: dict) -> dict:
    """
    Get workbook preview image
    """

    jwt = generate_login_jwt()

    server = TSC.Server(POD_URL, use_server_version=True)
    tab_auth = TSC.JWTAuth(jwt, site_id=SITE_NAME)

    with server.auth.sign_in(tab_auth):
        token = server.auth_token
        headers = {
            "X-Tableau-Auth": token,
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        req_url = f"{POD_URL}/api/3.25/sites/{server.site_id}/workbooks/{wb_dict['wb_luid']}/previewImage"

        response = requests.get(req_url, headers=headers, verify=False)

        encoded_img = base64.b64encode(response.content).decode("utf-8")

        return encoded_img


def get_workbooks_for_user(user_luid: str) -> list:
    """
    Get workbooks for user
    """

    server, tab_auth = get_server_and_auth(
        POD_URL,
        SITE_NAME,
        pat_name=PAT_NAME,
        pat_secret=PAT_SECRET,
    )

    user_wbs = []

    with server.auth.sign_in(tab_auth):
        token = server.auth_token
        headers = {
            "X-Tableau-Auth": token,
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        req_url = (
            f"{POD_URL}/api/3.25/sites/{server.site_id}/users/{user_luid}/workbooks"
        )

        response = requests.get(req_url, headers=headers, verify=False)

        for wb in response.json()["workbooks"]["workbook"]:
            user_wbs.append(wb)

        page_number = int(response.json()["pagination"].get("pageNumber"))
        page_size = int(response.json()["pagination"].get("pageSize"))
        total_count = int(response.json()["pagination"].get("totalAvailable"))
        total_pages = math.ceil(total_count / page_size)

        for page in range(2, total_pages + 1):
            response = requests.get(
                f"{req_url}?pageNumber={page}",
                headers=headers,
            )

            for wb in response.json()["workbooks"]["workbook"]:
                user_wbs.append(wb)

        return response.json()


def perform_content_search(search_dict: str) -> list:
    """
    Perform content search
    """

    try:
        server, tab_auth = get_server_and_auth(
            POD_URL,
            SITE_NAME,
            pat_name=PAT_NAME,
            pat_secret=PAT_SECRET,
        )

        page_index = search_dict.get("pageIndex", 0)
        search_results = []
        resp_dict = {}

        with server.auth.sign_in(tab_auth):
            token = server.auth_token
            headers = {
                "X-Tableau-Auth": token,
                "Content-Type": "application/json",
                "Accept": "application/json",
            }

            req_url = f"{POD_URL}/api/-/search?terms={search_dict["term"]}&filter=type:eq:{search_dict['objectType']}&limit={search_dict['limit']}&page={page_index}"

            print("+++++ REQ URL: ", req_url)

            response = requests.get(req_url, headers=headers, verify=False)

            print()

            total_results = response.json()["hits"]["total"]
            page_size = response.json()["hits"]["limit"]
            total_pages = math.ceil(total_results / page_size)

            resp_dict["pagination"] = {
                "pageIndex": page_index,
                "pageSize": page_size,
                "totalAvailable": total_results,
                "totalPages": total_pages,
            }

            for hit in response.json()["hits"]["items"]:
                search_results.append(hit)

            if search_dict.get("getAll"):

                for page in range(1, total_pages):
                    req_url = f"{POD_URL}/api/-/search?terms={search_dict["term"]}&filter=type:eq:{search_dict['objectType']}&limit={search_dict['limit']}&page={page}"

                    response = requests.get(req_url, headers=headers, verify=False)

                    for hit in response.json()["hits"]["items"]:
                        search_results.append(hit)

            resp_dict["results"] = search_results

            return resp_dict

    except Exception as e:
        resp_dict["pagination"] = {
            "pageIndex": page_index,
            "pageSize": page_size,
            "totalAvailable": total_results,
            "totalPages": total_pages,
        }

        resp_dict["results"] = search_results

        return resp_dict


def get_item_tags(item_dict: dict) -> list:
    """
    Get item tags
    """

    server, tab_auth = get_server_and_auth(
        POD_URL,
        SITE_NAME,
        pat_name=PAT_NAME,
        pat_secret=PAT_SECRET,
    )

    with server.auth.sign_in(tab_auth):
        # view = server.views.get_by_id(item_dict["item_luid"])

        # return {"view_luid": view.id, "view_name": view.name, "tags": view.tags}
        token = server.auth_token
        headers = {
            "X-Tableau-Auth": token,
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        req_url = (
            f"{POD_URL}/api/3.25/sites/{server.site_id}/views/{item_dict['item_luid']}"
        )
        response = requests.get(req_url, headers=headers, verify=False)

        return response.json()


def get_user_recommendations(user_dict: dict) -> list:
    """
    Get user recommendations
    """

    server, tab_auth = get_server_and_auth(
        POD_URL,
        SITE_NAME,
        pat_name=PAT_NAME,
        pat_secret=PAT_SECRET,
    )

    with server.auth.sign_in(tab_auth):
        token = server.auth_token
        headers = {
            "X-Tableau-Auth": token,
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        req_url = (
            f"{POD_URL}/api/3.25/sites/{server.site_id}/recommendations/?type=workbook"
        )

        print("+++++ REQ URL: ", req_url)

        response = requests.get(req_url, headers=headers, verify=False)

        return response.json()


def get_user_favorites(user_dict: dict) -> list:
    """
    Get user favorites
    """

    server, tab_auth = get_server_and_auth(
        POD_URL,
        SITE_NAME,
        pat_name=PAT_NAME,
        pat_secret=PAT_SECRET,
    )

    with server.auth.sign_in(tab_auth):
        token = server.auth_token
        headers = {
            "X-Tableau-Auth": token,
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        req_url = f"{POD_URL}/api/3.25/sites/{server.site_id}/favorites/{user_dict['user_luid']}?pageSize=1000"

        response = requests.get(req_url, headers=headers, verify=False)

        resp_json = response.json()

        for item in resp_json["favorites"]["favorite"]:
            print(item.keys())

            if "project" in item.keys():
                item["type"] = "project"

            elif "workbook" in item.keys():
                item["type"] = "workbook"

            elif "view" in item.keys():
                item["type"] = "view"

            elif "datasource" in item.keys():
                item["type"] = "datasource"

            else:
                item["type"] = "unknown"

        return resp_json


def add_item_to_favorites(item_dict: dict) -> dict:
    """
    Add item to favorites
    """

    print("++++++ GOT TO 355")

    server, tab_auth = get_server_and_auth(
        POD_URL,
        SITE_NAME,
        pat_name=PAT_NAME,
        pat_secret=PAT_SECRET,
    )

    with server.auth.sign_in(tab_auth):
        token = server.auth_token
        headers = {
            "X-Tableau-Auth": token,
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        req_url = f"{POD_URL}/api/3.25/sites/{server.site_id}/favorites/{item_dict['user_luid']}/"
        req_body = {"favorite": {"label": item_dict["label"]}}

        req_body["favorite"][item_dict["item_type"].lower()] = {
            "id": item_dict["item_luid"]
        }

        print("++++ FAVE REQ BODY: ")
        print(req_body)

        response = requests.put(req_url, headers=headers, json=req_body, verify=False)

        return response.json()


def remove_item_from_favorites(item_dict: dict) -> dict:
    """
    Remove item from favorites
    """

    server, tab_auth = get_server_and_auth(
        POD_URL,
        SITE_NAME,
        pat_name=PAT_NAME,
        pat_secret=PAT_SECRET,
    )

    with server.auth.sign_in(tab_auth):
        token = server.auth_token
        headers = {
            "X-Tableau-Auth": token,
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        req_url = f"{POD_URL}/api/3.25/sites/{server.site_id}/favorites/{item_dict['user_luid']}/{item_dict['item_type'].lower()}s/{item_dict['item_luid']}"
        print("+++++ REQ URL")
        print(req_url)

        response = requests.delete(req_url, headers=headers, verify=False)

        return response.content


def get_url_to_item(item_dict: dict) -> dict:
    """
    Get URL to item
    """

    server, tab_auth = get_server_and_auth(
        POD_URL,
        SITE_NAME,
        pat_name=PAT_NAME,
        pat_secret=PAT_SECRET,
    )

    with server.auth.sign_in(tab_auth):
        token = server.auth_token

        if item_dict["item_type"] == "project":

            resp = requests.get(
                f"{POD_URL}/api/3.25/sites/{server.site_id}/projects/?filter=name:eq:{item_dict['item_name']}",
                headers={"X-Tableau-Auth": token, "Accept": "application/json"},
                verify=False,
            )

            return resp.json()
