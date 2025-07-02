import httpx

from settings import settings
from utils.http_client import make_get_request, make_patch_request, make_post_request


async def get_workitems_ids_assigned_to_user() -> list[str]:
    """
    Get all workitems assigned to a user

    Returns:
        A list of workitems assigned to the user
    """
    url = f"{settings.AZURE_DEVOPS_BASE_URL}/wiql?api-version={settings.AZURE_DEVOPS_API_VERSION}"
    data = {"query": build_query_to_get_workitems_ids_assigned_to_user()}

    credentials = ("", settings.AZURE_DEVOPS_ACCESS_TOKEN)
    response = await make_post_request(url, "POST", data, credentials=credentials)
    workitems = response.get("workItems", [])
    workitems_ids = [str(workitem["id"]) for workitem in workitems]

    return workitems_ids


async def get_workitems_ids_assigned_to_user_by(columns_where: str) -> list[str]:
    """
    Get all workitems assigned to a user by a list of columns

    Args:
    columns_where: A string of columns to get from the workitems (e.g. "System.Id = 1 AND System.Title = 'Test' AND Sytem.CreatedDate = '2025-07-02'")

    Returns:
        A list of workitems assigned to the user
    """
    url = f"{settings.AZURE_DEVOPS_BASE_URL}/wiql?api-version={settings.AZURE_DEVOPS_API_VERSION}"
    data = {
        "query": build_query_to_get_workitems_ids_assigned_to_user_by(columns_where)
    }

    credentials = ("", settings.AZURE_DEVOPS_ACCESS_TOKEN)
    response = await make_post_request(url, "POST", data, credentials=credentials)
    workitems = response.get("workItems", [])

    workitems_ids = [str(workitem["id"]) for workitem in workitems]

    return workitems_ids


async def get_workitems_ids_assigned_to_user_by_planned_date(
    planned_date: str,
) -> list[str]:
    """
    Get all workitems assigned to a user by a planned date

    Args:
        planned_date: The planned date to get the workitems (e.g. "2025-07-02")

    Returns:
        A list of workitems assigned to the user
    """
    url = f"{settings.AZURE_DEVOPS_BASE_URL}/wiql?api-version={settings.AZURE_DEVOPS_API_VERSION}"
    data = {
        "query": build_query_to_get_workitems_ids_assigned_to_user_by_planned_date(
            planned_date
        )
    }

    credentials = ("", settings.AZURE_DEVOPS_ACCESS_TOKEN)
    response = await make_post_request(url, "POST", data, credentials=credentials)
    workitems = response.get("workItems", [])

    workitems_ids = [str(workitem["id"]) for workitem in workitems]

    return workitems_ids


async def get_workitems_details_by_ids(workitems_ids: str) -> list[dict]:
    """
    Get all workitems details by their IDs

    Args:
        workitems_ids: A string of workitem IDs (comma separated) (e.g. "1,2,3")

    Returns:
        A list of workitems details
    """

    url = f"{settings.AZURE_DEVOPS_BASE_URL}/workitems?ids={workitems_ids}&api-version={settings.AZURE_DEVOPS_API_VERSION}"
    credentials = ("", settings.AZURE_DEVOPS_ACCESS_TOKEN)
    print(url)
    try:
        response = await make_get_request(url, credentials=credentials)
        return response.get("value", [])
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            print(f"Workitems not found: {workitems_ids}")
            return []
        else:
            print(f"Error getting workitems details by ids: {e}")
            raise e
    except Exception as e:
        print(f"Error getting workitems details by ids: {e}")
        return []


async def get_all_workitems_types() -> list[dict]:
    """
    Get all workitem types

    Returns:
        A list of workitem types
    """
    url = f"{settings.AZURE_DEVOPS_BASE_URL}/workitemtypes?api-version={settings.AZURE_DEVOPS_API_VERSION}"
    credentials = ("", settings.AZURE_DEVOPS_ACCESS_TOKEN)
    response = await make_get_request(url, credentials=credentials)

    return response.get("value", [])


async def get_workitem_type_by_name(name: str) -> dict:
    """
    Get a workitem type by its name

    Args:
        name: The name of the workitem type (e.g. "Task", "Bug", "Feature")

    Returns:
        A workitem type
    """
    url = f"{settings.AZURE_DEVOPS_BASE_URL}/workitemtypes/{name}?api-version={settings.AZURE_DEVOPS_API_VERSION}"
    credentials = ("", settings.AZURE_DEVOPS_ACCESS_TOKEN)

    response = await make_get_request(url, credentials=credentials)

    return response


async def get_workitem_type_states(workitem_type_name: str) -> list[dict]:
    """
    Get all workitem type states

    Args:
        workitem_type_name: The name of the workitem type (e.g. "Task", "Bug", "Feature")

    Returns:
        A list of workitem type states
    """
    url = f"{settings.AZURE_DEVOPS_BASE_URL}/workitemtypes/{workitem_type_name}/states?api-version={settings.AZURE_DEVOPS_API_VERSION}"
    credentials = ("", settings.AZURE_DEVOPS_ACCESS_TOKEN)
    response = await make_get_request(url, credentials=credentials)

    return response.get("value", [])


async def get_workitem_type_transitions(workitem_type_name: str) -> dict:
    """
    Get all workitem type transitions

    Args:
        workitem_type_name: The name of the workitem type (e.g. "Task", "Bug", "Feature")

    Returns:
        A dictionary of workitem type transitions
    """
    workitem_type = await get_workitem_type_by_name(workitem_type_name)
    return workitem_type.get("transitions", [])


async def get_workitem_transitions_allowed(
    workitem_type_name: str, workitem_state_name: str
) -> list[dict]:
    """
    Get a list of allowed transitions for a workitem

    Args:
        workitem_type_name: The name of the workitem type (e.g. "Task", "Bug", "Feature")
        workitem_state_name: The name of the workitem state (e.g. "To Do", "In Progress", "Done")

    Returns:
        A list of allowed transitions
    """
    workitem_type_transitions = await get_workitem_type_transitions(workitem_type_name)
    return workitem_type_transitions.get(workitem_state_name, [])


async def update_workitem_state(workitem_id: str, workitem_state_name: str) -> bool:
    """
    Update the state of a workitem

    Args:
        workitem_id: The ID of the workitem
        workitem_state_name: The name of the allowed workitem state (e.g. "To Do", "In Progress", "Done")
    """
    try:
        body = [
            {
                "op": "add",
                "path": "/fields/System.State",
                "value": workitem_state_name,
            }
        ]

        url = f"{settings.AZURE_DEVOPS_BASE_URL}/workitems/{workitem_id}?api-version={settings.AZURE_DEVOPS_API_VERSION}"
        credentials = ("", settings.AZURE_DEVOPS_ACCESS_TOKEN)

        await make_patch_request(url, body, credentials=credentials)

        return True
    except Exception as e:
        print(f"Error updating workitem state: {e}")
        return False


def build_query_to_get_workitems_ids_assigned_to_user() -> str:
    """
    Build a query to get all workitems assigned to a user

    Returns:
        A query to get all workitems assigned to a user
    """
    return "SELECT [System.Id] FROM WorkItems WHERE [System.AssignedTo] = @Me ORDER BY [System.ChangedDate] DESC"


def build_query_to_get_workitems_ids_assigned_to_user_by(columns_where: str) -> str:
    """
    Build a query to get all workitems assigned to a user by a list of columns

    Args:
        columns_where: A string of columns to get from the workitems (e.g. "System.Id = 1 AND System.Title = 'Test'")

    Returns:
        A query to get all workitems assigned to a user by a list of columns
    """
    return f"SELECT [System.Id] FROM WorkItems WHERE [System.AssignedTo] = @Me AND {columns_where} ORDER BY [System.Id] DESC"


def build_query_to_get_workitems_ids_assigned_to_user_by_planned_date(
    planned_date: str,
) -> str:
    """
    Build a query to get all workitems assigned to a user by a planned date

    Args:
        planned_date: The planned date to get the workitems (e.g. "2025-07-02")

    Returns:
        A query to get all workitems assigned to a user by a planned date
    """
    return f"SELECT [System.Id] FROM WorkItems WHERE [System.AssignedTo] = @Me AND Custom.FechaInicioPlaneada = '{planned_date}' ORDER BY [System.Id] DESC"
