from mcp.server.fastmcp import FastMCP

from services import workitems
from utils.formatters import (
    format_workitem,
    format_workitem_type,
    format_workitem_type_state,
    format_workitem_type_transition,
)

mcp = FastMCP()


@mcp.tool("get_workitems_ids_assigned_to_user")
async def get_workitems_ids_assigned_to_user():
    """
    Get all workitems assigned to a user

    Returns:
        A list of workitems assigned to the user

    Example:
        get_workitems_ids_assigned_to_user()
        Returns:
            Workitems ids found: 1,2,3
    """
    workitems_ids = await workitems.get_workitems_ids_assigned_to_user()

    if workitems_ids:
        result = f"Workitems ids found: {','.join(workitems_ids)}"
    else:
        result = "No workitems found"

    return result


@mcp.tool("get_workitems_ids_assigned_to_user_by")
async def get_workitems_ids_assigned_to_user_by(columns_where: str):
    """
    Get all workitems assigned to a user by a list of columns

    Args:
        columns_where: A string of column (ReferenceName) to get from the workitems (e.g. "System.Id = 1 AND System.Title = 'Test'")

    Returns:
        A list of workitems assigned to the user
    """
    workitems_ids = await workitems.get_workitems_ids_assigned_to_user_by(columns_where)

    if workitems_ids:
        result = f"Workitems ids found: {','.join(workitems_ids)}"
    else:
        result = "No workitems found"

    return result


@mcp.tool("get_workitems_ids_assigned_to_user_by_planned_date")
async def get_workitems_ids_assigned_to_user_by_planned_date(planned_date: str):
    """
    Get all workitems assigned to a user by a planned date (Custom.FechaInicioPlaneada referenceName is required)

    Args:
        planned_date: The planned date to get the workitems (e.g. "2025-07-02")

    Returns:
        A list of workitems assigned to the user
    """
    workitems_ids = await workitems.get_workitems_ids_assigned_to_user_by_planned_date(
        planned_date
    )

    if workitems_ids:
        result = f"Workitems ids found: {','.join(workitems_ids)}"
    else:
        result = "No workitems found"

    return result


@mcp.tool("get_workitems_details_by_ids")
async def get_workitems_details_by_ids(workitems_ids: str):
    """
    Get a workitem by its ID

    Args:
        workitems_ids: A list of workitem IDs (comma separated)

    Returns:
        A list of workitems details
    """
    workitems_details = await workitems.get_workitems_details_by_ids(workitems_ids)

    if workitems_details:
        result = "\n\n".join(
            format_workitem(workitem_detail) for workitem_detail in workitems_details
        )
    else:
        result = "No workitems found"

    return result


@mcp.tool("get_all_workitems_types")
async def get_all_workitems_types():
    """
    Get all workitem types

    Returns:
        A list of workitem types
    """
    workitem_types = await workitems.get_all_workitems_types()
    result = "\n\n".join(
        format_workitem_type(workitem_type) for workitem_type in workitem_types
    )

    return result


@mcp.tool("get_workitem_type_by_name")
async def get_workitem_type_by_name(name: str):
    """
    Get a workitem type by its name

    Args:
        name: The name of the workitem type (e.g. "Task", "Bug", "Feature")

    Returns:
        A workitem type
    """
    workitem_type = await workitems.get_workitem_type_by_name(name)
    result = format_workitem_type(workitem_type)

    return result


@mcp.tool("get_workitem_type_states")
async def get_workitem_type_states(workitem_type_name: str):
    """
    Get all workitem type states
    """
    workitem_type_states = await workitems.get_workitem_type_states(workitem_type_name)
    result = "\n\n".join(
        format_workitem_type_state(workitem_type_state)
        for workitem_type_state in workitem_type_states
    )

    return result


@mcp.tool("get_workitem_transition_list_allowed")
async def get_workitem_transition_list_allowed(
    workitem_type_name: str, workitem_state_name: str
):
    """
    Get a list of allowed transitions for a workitem
    """
    transitions = await workitems.get_workitem_transition_list_allowed(
        workitem_type_name, workitem_state_name
    )

    if transitions:
        result = "\n\n".join(
            format_workitem_type_transition(
                workitem_type_name, transition.get("to", "")
            )
            for transition in transitions
        )
    else:
        result = "No transitions allowed for this workitem state"

    return result


if __name__ == "__main__":
    mcp.run()
