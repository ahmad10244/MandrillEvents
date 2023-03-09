

def test_connect_namespace(socketio_client):
    """
    Test to check socketio connect and disconnect to namespace
    :param socketio_client: Pytest Fixture as specified in the ConfTest File
    """
    assert socketio_client.is_connected('/events')
    
    socketio_client.disconnect(namespace="/events")
    assert not socketio_client.is_connected('/events')


def test_on_get_message(socketio_client, caplog):
    """
    Test to check socketio on_message handler
    :param socketio_client: Pytest Fixture as specified in the ConfTest File
    :param caplog: Pytest caplog Fixture
    """
    socketio_client.emit("message", {"event": "connect"}, namespace="/events")
    socketio_client.get_received('/events')
    assert 'Client connected' in caplog.text

    socketio_client.emit("message", {"event": "disconnect"}, namespace="/events")
    socketio_client.get_received('/events')
    assert 'Client disconnected' in caplog.text

    
def test_event_emit(mongo_db_patch, monkeypatch, app_client, webhook_events_json, socketio_client):
    """
    Test to check socketio events emiting on calling webhook API
    :param mongo_db_patch: Pytest Fixture as specified in the ConfTest File
    :param monkeypatch: Pytest monkeypatch Fixture
    :param app_client: Pytest Fixture as specified in the ConfTest File
    :param webhook_events_json: Pytest Fixture as specified in the ConfTest File
    :param socketio_client: Pytest Fixture as specified in the ConfTest File
    """
    monkeypatch.setattr("app.get_mongodb_collection", mongo_db_patch)
    app_client.post("/event", data=webhook_events_json)
    
    received = socketio_client.get_received('/events')

    assert received[0]["name"] == "message"
    assert received[0]["namespace"] == "/events"
    assert type(received[0]["args"]) == list
    assert "event" in received[0]["args"][0]
    assert "ts" in received[0]["args"][0]
