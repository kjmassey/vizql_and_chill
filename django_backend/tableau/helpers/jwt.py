import jwt
import datetime
import uuid
from tableau.creds.tableau_creds import (
    CONNECTED_APP_NAME,
    CONNECTED_APP_CLIENT_ID,
    CONNECTED_APP_SECRET_ID,
    CONNECTED_APP_SECRET_VALUE,
)


def generate_login_jwt():
    token = jwt.encode(
        {
            "iss": CONNECTED_APP_CLIENT_ID,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=10),
            "jti": str(uuid.uuid4()),
            "aud": "tableau",
            "sub": "kyle.massey@gmail.com",
            # SCOPES EXPLAINED: https://help.tableau.com/current/online/en-us/connected_apps_scopes.htm
            "scp": [
                "tableau:projects:*",
                "tableau:workbooks:*",
                "tableau:datasources:*",
                "tableau:views:*",
                "tableau:views:embed",
                "tableau:users:*",
                "tableau:content:*",
                "tableau:viz_data_service:read",
            ],
        },
        CONNECTED_APP_SECRET_VALUE,
        algorithm="HS256",
        headers={"kid": CONNECTED_APP_SECRET_ID, "iss": CONNECTED_APP_CLIENT_ID},
    )

    return token
