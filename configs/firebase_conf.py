import os

import firebase_admin
from firebase_admin import credentials


def init_firebase():
    cred = credentials.Certificate(
        {
            "type": os.getenv("GCP_SERVICE_ACCOUNT_TYPE"),
            "project_id": os.getenv("GCP_SERVICE_ACCOUNT_PROJECT_ID"),
            "private_key_id": os.getenv("GCP_SERVICE_ACCOUNT_PRIVATE_KEY_ID"),
            "private_key": os.getenv("GCP_SERVICE_ACCOUNT_PRIVATE_KEY")[1:-1].replace(
                "\\n", "\n"
            ),
            "client_email": os.getenv("GCP_SERVICE_ACCOUNT_CLIENT_EMAIL"),
            "client_id": os.getenv("GCP_SERVICE_ACCOUNT_CLIENT_ID"),
            "auth_uri": os.getenv("GCP_SERVICE_ACCOUNT_AUTH_URI"),
            "token_uri": os.getenv("GCP_SERVICE_ACCOUNT_TOKEN_URI"),
            "auth_provider_x509_cert_url": os.getenv(
                "GCP_SERVICE_ACCOUNT_AUTH_PROVIDER_X509_CERT_URL"
            ),
            "client_x509_cert_url": os.getenv(
                "GCP_SERVICE_ACCOUNT_CLIENT_X509_CERT_URL"
            ),
            "universe_domain": os.getenv("GCP_SERVICE_ACCOUNT_UNIVERSE_DOMAIN"),
        }
    )

    try:
        firebase_admin.initialize_app(cred)
    except ValueError:
        pass
