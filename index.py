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
        else:
            routes.default(connection_id)

    return {"statusCode": 200}
