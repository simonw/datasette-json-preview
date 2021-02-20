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
async def test_default(client):
    next_url = "/test/records.json-preview"
    collected = []
    while next_url:
        response = await client.get(next_url.replace("http://localhost", ""))
        next_url = response.links.get("next", {}).get("url")
        collected.extend(response.json())
    assert len(collected) == 1001
    # They should all be unique:
    assert len(set(d["id"] for d in collected)) == 1001


@pytest.mark.asyncio
async def test_extra_total(client):
    next_url = "/test/records.json-preview?_extra=total"
    collected = []
    while next_url:
        response = await client.get(next_url.replace("http://localhost", ""))
        next_url = response.links.get("next", {}).get("url")
        json = response.json()
        assert set(json.keys()) == {"rows", "total"}
        collected.extend(json["rows"])
        assert json["total"] == 1001
    assert len(collected) == 1001
    # They should all be unique:
    assert len(set(d["id"] for d in collected)) == 1001


@pytest.mark.asyncio
async def test_extra_next_url(client):
    next_url = "/test/records.json-preview?_extra=next_url"
    collected = []
    while next_url:
        response = await client.get(next_url.replace("http://localhost", ""))
        next_url = response.links.get("next", {}).get("url")
        json = response.json()
        assert set(json.keys()) == {"rows", "next_url"}
        collected.extend(json["rows"])
        assert next_url == json["next_url"]
    assert len(collected) == 1001
    assert len(set(d["id"] for d in collected)) == 1001
