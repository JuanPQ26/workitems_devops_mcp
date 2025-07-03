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
        workitems_ids: A string of workitem IDs (comma separated) (e.g. "1,2,3")

    Returns:
        A list of workitems details (one per workitem)
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
        A list of workitem types details
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
        A workitem type details
    """
    workitem_type = await workitems.get_workitem_type_by_name(name)
    result = format_workitem_type(workitem_type)

    return result


@mcp.tool("get_workitem_type_states")
async def get_workitem_type_states(workitem_type_name: str):
    """
    Get all workitem type states

    Args:
        workitem_type_name: The name of the workitem type (e.g. "Task", "Bug", "Feature")

    Returns:
        A list of workitem type states
    """
    workitem_type_states = await workitems.get_workitem_type_states(workitem_type_name)
    result = "\n\n".join(
        format_workitem_type_state(workitem_type_state)
        for workitem_type_state in workitem_type_states
    )

    return result


@mcp.tool("get_workitem_transitions_allowed")
async def get_workitem_transitions_allowed(
    workitem_type_name: str, workitem_state_name: str
):
    """
    Get a list of allowed transitions for a workitem

    Args:
        workitem_type_name: The name of the workitem type (e.g. "Task", "Bug", "Feature")
        workitem_state_name: The name of the workitem state (e.g. "To Do", "In Progress", "Done")

    Returns:
        A list of allowed transitions for the workitem
    """
    transitions = await workitems.get_workitem_transitions_allowed(
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


@mcp.tool("update_workitem_state")
async def update_workitem_state(workitem_id: str, workitem_state_name: str):
    """
    Update the state of a workitem

    Args:
        workitem_id: The ID of the workitem
        workitem_state_name: The name of the workitem state to set (e.g. "To Do", "In Progress", "Done")

    Returns:
        A message with the result of the operation
    """
    result = await workitems.update_workitem_state(workitem_id, workitem_state_name)

    if result:
        return "Workitem state updated successfully"
    else:
        return "Failed to update workitem state"


@mcp.tool("update_workitem_planned_date")
async def update_workitem_planned_date(workitem_id: str, planned_date: str):
    """
    Update the planned date of a workitem

    Args:
        workitem_id: The ID of the workitem
        planned_date: The planned date to set take into account the timezone (e.g. in colombia "2025-07-02T00:00:00Z" + 5h)

    Returns:
        A message with the result of the operation
    """
    result = await workitems.update_workitem_planned_date(workitem_id, planned_date)

    if result:
        return "Workitem planned date updated successfully"
    else:
        return "Failed to update workitem planned date"


@mcp.tool("update_workitem_real_effort")
async def update_workitem_real_effort(workitem_id: str, real_effort: str):
    """
    Update the real effort of a workitem

    Args:
        workitem_id: The ID of the workitem
        real_effort: The real effort to set (e.g. "1.0", "2.0", "3.5")

    Returns:
        A message with the result of the operation
    """
    result = await workitems.update_workitem_real_effort(workitem_id, real_effort)

    if result:
        return "Workitem real effort updated successfully"
    else:
        return "Failed to update workitem real effort"


@mcp.tool("update_workitem_description")
async def update_workitem_description(workitem_id: str, description: str):
    """
    Update the description of a workitem

    Args:
        workitem_id: The ID of the workitem
        description: The description to set and you can add tags like <ul>, <b>, <br>, <a href>, etc.

    Returns:
        A message with the result of the operation
    """
    result = await workitems.update_workitem_description(workitem_id, description)

    if result:
        return "Workitem description updated successfully"
    else:
        return "Failed to update workitem description"


@mcp.tool("update_workitems_planned_date")
async def update_workitems_planned_date(workitems_ids: str, planned_date: str):
    """
    Update the planned date of a list of workitems

    Args:
        workitems_ids: A string of workitem IDs (comma separated) (e.g. "1,2,3")
        planned_date: The planned date to set (e.g. "2025-07-02T00:00:00Z")

    Returns:
        A message with the result of the operation
    """
    result = await workitems.update_workitems_planned_date(workitems_ids, planned_date)

    if result:
        return f"Workitems planned date updated successfully: {','.join(result)}"
    else:
        return "Failed to update workitems planned date"


@mcp.tool("add_workitem_comment")
async def add_workitem_comment(workitem_id: str, comment: str):
    """
    Add a comment to a workitem

    Args:
        workitem_id: The ID of the workitem
        comment: The comment to add (e.g. "This is a test comment")

    Returns:
        A message with the result of the operation
    """
    result = await workitems.add_workitem_comment(workitem_id, comment)

    if result:
        return "Workitem comment added successfully"
    else:
        return "Failed to add workitem comment"


if __name__ == "__main__":
    mcp.run()
