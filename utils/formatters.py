def format_workitem(workitem: dict) -> str:
    fields = workitem.get("fields", {})

    return (
        f"ID: {workitem.get('id')}\n"
        f"Título: {fields.get('System.Title')}\n"
        f"Work Item Type: {fields.get('System.WorkItemType')}\n"
        f"Estado: {fields.get('System.State')} ({fields.get('System.Reason')})\n"
        f"Asignado a: {fields.get('System.AssignedTo', {}).get('displayName')}\n"
        f"Prioridad: {fields.get('Microsoft.VSTS.Common.Priority')}\n"
        f"Inicio Planeado: {format_date_from_iso(fields.get('Custom.FechaInicioPlaneada', ''))}\n"
        f"Esfuerzo: {format_effort(fields.get('Microsoft.VSTS.Scheduling.Effort'))}\n"
        "\n"
        f"Creado por: {fields.get('System.CreatedBy', {}).get('displayName')} el {fields.get('System.CreatedDate', '')}\n"
        f"Último cambio por: {fields.get('System.ChangedBy', {}).get('displayName')} el {fields.get('System.ChangedDate', '')}\n"
        "\n"
        f"URL: {workitem.get('url')}"
    )


def format_workitem_type(workitem_type: dict) -> str:
    name = workitem_type.get("name", "")
    ref_name = workitem_type.get("referenceName", "")
    description = workitem_type.get("description", "")
    is_disabled = workitem_type.get("isDisabled", False)

    # Campos
    fields = workitem_type.get("fields", [])
    formatted_fields = "\n".join(
        [
            f"{f.get('name')} ({f.get('referenceName')}){' [REQUIRED]' if f.get('alwaysRequired') else ''}"
            for f in fields
        ]
    )

    # Estados
    states = workitem_type.get("states", [])
    formatted_states = "\n".join(
        [
            f"{s.get('name')} ({s.get('category')}, color: {s.get('color')})"
            for s in states
        ]
    )

    # Transiciones
    transitions = workitem_type.get("transitions", {})
    formatted_transitions = format_workitem_type_transitions_dict(transitions)

    return (
        f"Tipo de Work Item: {name}\n"
        f"Referencia: {ref_name}\n"
        f"Descripción: {description}\n"
        f"Habilitado: {'No' if is_disabled else 'Sí'}\n\n"
        f"Campos:\n{formatted_fields}\n\n"
        f"Estados:\n{formatted_states}\n\n"
        f"Transiciones:\n{formatted_transitions}"
    )


def format_workitem_type_transitions_dict(transitions: dict) -> str:
    transition_lines = []

    for key, value in transitions.items():
        transition_lines.extend(
            format_workitem_type_transition(key, transition.get("to"))
            for transition in value
        )

    return "\n".join(transition_lines)


def format_workitem_type_transition(from_state: str, to_state: str) -> str:
    return f"De: {from_state} -> A: {to_state}"


def format_workitem_type_state(workitem_type_state: dict) -> str:
    name = workitem_type_state.get("name", "")
    category = workitem_type_state.get("category", "")
    color = workitem_type_state.get("color", "")

    return f"Estado: {name}\nCategoría: {category}\nColor: #{color}\n"


def format_date_from_iso(date: str) -> str:
    """
    Format a date from ISO format to YYYY-MM-DD

    Args:
        date: The date to format

    Returns:
        The formatted date
    """
    return date.split("T")[0]


def format_effort(effort: str) -> str:
    """
    Format a effort in decimal format to hours

    Args:
        effort: The effort to format (e.g. "1.5")

    Returns:
        The formatted hours (e.g. "1 h 30 min")
    """
    hours = int(float(effort))
    minutes = int((float(effort) - hours) * 60)
    return f"{hours} h {minutes} min"
