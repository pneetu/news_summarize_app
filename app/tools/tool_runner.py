from activities import get_activity_data

def run_tool(name, args):
    if name == "get_activity_data":
        return get_activity_data(**args)

    raise ValueError("Unknown tool")