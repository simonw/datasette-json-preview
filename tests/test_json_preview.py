from datasette.app import Datasette
import pytest
import sqlite_utils


@pytest.fixture(scope="session")
def client(tmp_path_factory):
    db_directory = tmp_path_factory.mktemp("dbs")
    db_path = db_directory / "test.db"
    db = sqlite_utils.Database(db_path)
    db["records"].insert_all(
        ({"id": i, "name": "This is record {}".format(i)} for i in range(1, 1002)),
        pk="id",
    )
    ds = Datasette([str(db_path)])
    return ds.client


@pytest.mark.asyncio
async def test_default_dict(client):
    next_url = "/test/records.json-preview"
    collected = []
    while next_url:
        response = await client.get(next_url.replace("http://localhost", ""))
        next_url_from_header = response.links.get("next", {}).get("url")
        next_url = response.json()["next_url"]
        assert next_url_from_header == next_url
        collected.extend(response.json()["rows"])
        assert response.json()["total"] == 1001
    assert len(collected) == 1001
    # They should all be unique:
    assert len(set(d["id"] for d in collected)) == 1001
