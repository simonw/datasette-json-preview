from datasette import hookimpl
from datasette.utils.asgi import Response


@hookimpl
def register_output_renderer(datasette):
    return {
        "extension": "json-preview",
        "render": json_preview,
    }


def json_preview(data, columns, rows, request):
    extras = request.args.getlist("_extra")
    next_url = data.get("next_url")
    headers = {}
    if next_url:
        headers["link"] = '<{}>; rel="next"'.format(next_url)

    rows_gen = (dict(zip(columns, row)) for row in rows)

    # Default if no ?_extra= is just the rows
    if not extras:
        return Response.json(list(rows_gen), headers=headers)

    to_return = {
        "rows": list(rows_gen),
    }

    if "total" in extras:
        to_return["total"] = data["filtered_table_rows_count"]

    if "next_url" in extras:
        to_return["next_url"] = next_url

    return Response.json(
        to_return,
        headers=headers,
    )
