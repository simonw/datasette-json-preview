from datasette import hookimpl
from datasette.utils.asgi import Response


@hookimpl
def register_output_renderer(datasette):
    return {
        "extension": "json-preview",
        "render": json_preview,
    }


def json_preview(data, columns, rows):
    next_url = data.get("next_url")
    headers = {}
    if next_url:
        headers["link"] = '<{}>; rel="next"'.format(next_url)
    return Response.json([dict(zip(columns, row)) for row in rows], headers=headers)
