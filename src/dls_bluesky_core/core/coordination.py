import uuid


def group_uuid(name: str) -> str:
    """
    Returns a unique but human-readable string, to assist debugging orchestrated groups.

    Args:
        name (str): A human readable name

    Returns:
        readable_uid (str): name appended with a unique string
    """
    return f"{name}-{str(uuid.uuid4())[:6]}"
