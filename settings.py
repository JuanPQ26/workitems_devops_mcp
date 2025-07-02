import os

import dotenv

dotenv.load_dotenv()


class Settings:
    AZURE_DEVOPS_API_VERSION = "7.0"
    USER_AGENT = "workitems-devops-mcp/1.0"

    AZURE_DEVOPS_ACCESS_TOKEN = os.getenv("AZURE_DEVOPS_ACCESS_TOKEN")
    AZURE_DEVOPS_PROJECT = os.getenv("AZURE_DEVOPS_PROJECT")
    AZURE_DEVOPS_ORGANIZATION = os.getenv("AZURE_DEVOPS_ORGANIZATION")

    AZURE_DEVOPS_BASE_URL = f"https://dev.azure.com/{AZURE_DEVOPS_ORGANIZATION}/{AZURE_DEVOPS_PROJECT}/_apis/wit"


settings = Settings()
