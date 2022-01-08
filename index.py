import json

from src.routes import Routes


def handler(event, context):
    print(json.dumps(event))

    req_context = event.get("requestContext")
    body = json.loads(event.get("body")) if event.get("body") else None

    routes = Routes()

    if req_context:
        key = req_context.get("routeKey")
        connection_id = req_context.get("connectionId")

        if key == "$connect":
            routes.connect(connection_id)
        elif key == "$disconnect":
            routes.disconnect(connection_id)
        elif key == "searchGame":
            routes.searchGame(connection_id)
        elif key == "setBoats":
            routes.setBoats(connection_id, body)
        elif key == "move":
            routes.move(connection_id, body)
        else:
            routes.default(connection_id)

    return {"statusCode": 200}
