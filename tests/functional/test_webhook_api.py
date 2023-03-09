

def test_main_page(app_client):
    """
    Test to check whether the main page loads correctly
    :param app_client: Pytest Fixture as specified in the ConfTest File
    """
    response = app_client.get("/")
    assert response.status_code == 200
    assert "Recent events" in response.text


def test_new_event_from_mandrill_no_form_data(app_client):
    """
    Test to check whether the webhook return bad request erorr on empty form data
    :param app_client: Pytest Fixture as specified in the ConfTest File
    """
    response = app_client.post("/event")
    assert response.status_code == 400
    assert "msg" in response.text


def test_new_event_from_mandrill_wrong_form_data(app_client, webhook_events_wrong_json):
    """
    Test to check whether the webhook return bad request erorr on wrong form data
    :param app_client: Pytest Fixture as specified in the ConfTest File
    :param webhook_events_wrong_json: Pytest Fixture as specified in the ConfTest File
    """
    response = app_client.post("/event",
                               data=webhook_events_wrong_json)
    assert response.status_code == 400
    assert "msg" in response.text


def test_new_event_from_mandrill_complete_form_data(monkeypatch, app_client, webhook_events_json, mongo_db_patch):
    """
    Test to check whether the webhook return OKon correct form data
    :param monkeypatch: Pytest monkeypatch Fixture
    :param app_client: Pytest Fixture as specified in the ConfTest File
    :param webhook_events_json: Pytest Fixture as specified in the ConfTest File
    :param mongo_db_patch: Pytest Fixture as specified in the ConfTest File
    """
    monkeypatch.setattr("app.get_mongodb_collection", mongo_db_patch)

    response = app_client.post("/event",
                               data=webhook_events_json)

    assert response.status_code == 200
    assert response.text == ""
