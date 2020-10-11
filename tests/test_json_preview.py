from datasette.app import Datasette
import httpx
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
    ds = Datasette([db_path])
    return ds.client


@pytest.mark.asyncio
async def test_default_list(client):
    url = "/test/records.json-preview"
    collected = []
    while url:
        response = await client.get(url)
        url = response.links.get("next", {}).get("url")
        collected.extend(response.json())
    assert len(collected) == 1001
    # They should all be unique:
    assert len(set(d["id"] for d in collected)) == 1001
