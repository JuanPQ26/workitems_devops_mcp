import asyncio

from services import workitems
from utils.formatters import format_workitem_type

workitem_type_name = "Task"


async def main():
    workitem_type = await workitems.get_workitem_type_by_name(workitem_type_name)
    result = format_workitem_type(workitem_type)

    print(result)

    return result


if __name__ == "__main__":
    asyncio.run(main())
