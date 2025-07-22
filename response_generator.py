def generate_response(data):
    # Format the response based on data type
    if "movies" in data:
        return {"summary": f"{len(data['movies'])} movies analyzed.", "details": data}
    elif "cases" in data:
        return {"summary": f"{len(data['cases'])} court cases processed.", "details": data}
    else:
        return {"summary": "No data found", "details": {}}
