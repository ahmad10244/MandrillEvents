import json

import pytest
import mongomock

from app import app, socketio


mandrill_events_json = {
    "mandrill_events": [
        {
            "event": "send",
            "msg": {
                "ts": 1365109999,
                "subject": "This an example webhook message",
                "email": "example.webhook@mandrillapp.com",
                "sender": "example.sender@mandrillapp.com",
                "tags": [
                    "webhook-example"
                ],
                "opens": [],
                "clicks": [],
                "state": "sent",
                "metadata": {
                    "user_id": 111
                },
                "_id": "exampleaaaaaaaaaaaaaaaaaaaaaaaaa",
                "_version": "exampleaaaaaaaaaaaaaaa"
            },
            "_id": "exampleaaaaaaaaaaaaaaaaaaaaaaaaa",
            "ts": 1678229076
        },
        {
            "event": "open",
            "msg": {
                "ts": 1365109999,
                "subject": "This an example webhook message",
                "email": "example.webhook@mandrillapp.com",
                "sender": "example.sender@mandrillapp.com",
                "tags": [
                    "webhook-example"
                ],
                "opens": [
                    {
                        "ts": 1365111111
                    }
                ],
                "clicks": [
                    {
                        "ts": 1365111111,
                        "url": "http://mandrill.com"
                    }
                ],
                "state": "sent",
                "metadata": {
                    "user_id": 111
                },
                "_id": "exampleaaaaaaaaaaaaaaaaaaaaaaaaa5",
                "_version": "exampleaaaaaaaaaaaaaaa"
            },
            "_id": "exampleaaaaaaaaaaaaaaaaaaaaaaaaa5",
            "ip": "127.0.0.1",
            "location": {
                "country_short": "US",
                "country": "United States",
                "region": "Oklahoma",
                "city": "Oklahoma City",
                "latitude": 35.4675598145,
                "longitude": -97.5164337158,
                "postal_code": "73101",
                "timezone": "-05:00"
            },
            "user_agent": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; en-US; rv:1.9.1.8) Gecko/20100317 Postbox/1.1.3",
            "user_agent_parsed": {
                "type": "Email Client",
                "ua_family": "Postbox",
                "ua_name": "Postbox 1.1.3",
                "ua_version": "1.1.3",
                "ua_url": "http://www.postbox-inc.com/",
                "ua_company": "Postbox, Inc.",
                "ua_company_url": "http://www.postbox-inc.com/",
                "ua_icon": "http://cdn.mandrill.com/img/email-client-icons/postbox.png",
                "os_family": "OS X",
                "os_name": "OS X 10.6 Snow Leopard",
                "os_url": "http://www.apple.com/osx/",
                "os_company": "Apple Computer, Inc.",
                "os_company_url": "http://www.apple.com/",
                "os_icon": "http://cdn.mandrill.com/img/email-client-icons/macosx.png",
                "mobile": False
            },
            "ts": 1678229076
        },
        {
            "event": "click",
            "msg": {
                "ts": 1365109999,
                "subject": "This an example webhook message",
                "email": "example.webhook@mandrillapp.com",
                "sender": "example.sender@mandrillapp.com",
                "tags": [
                    "webhook-example"
                ],
                "opens": [
                    {
                        "ts": 1365111111
                    }
                ],
                "clicks": [
                    {
                        "ts": 1365111111,
                        "url": "http://mandrill.com"
                    }
                ],
                "state": "sent",
                "metadata": {
                    "user_id": 111
                },
                "_id": "exampleaaaaaaaaaaaaaaaaaaaaaaaaa6",
                "_version": "exampleaaaaaaaaaaaaaaa"
            },
            "_id": "exampleaaaaaaaaaaaaaaaaaaaaaaaaa6",
            "ip": "127.0.0.1",
            "location": {
                "country_short": "US",
                "country": "United States",
                "region": "Oklahoma",
                "city": "Oklahoma City",
                "latitude": 35.4675598145,
                "longitude": -97.5164337158,
                "postal_code": "73101",
                "timezone": "-05:00"
            },
            "user_agent": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; en-US; rv:1.9.1.8) Gecko/20100317 Postbox/1.1.3",
            "user_agent_parsed": {
                "type": "Email Client",
                "ua_family": "Postbox",
                "ua_name": "Postbox 1.1.3",
                "ua_version": "1.1.3",
                "ua_url": "http://www.postbox-inc.com/",
                "ua_company": "Postbox, Inc.",
                "ua_company_url": "http://www.postbox-inc.com/",
                "ua_icon": "http://cdn.mandrill.com/img/email-client-icons/postbox.png",
                "os_family": "OS X",
                "os_name": "OS X 10.6 Snow Leopard",
                "os_url": "http://www.apple.com/osx/",
                "os_company": "Apple Computer, Inc.",
                "os_company_url": "http://www.apple.com/",
                "os_icon": "http://cdn.mandrill.com/img/email-client-icons/macosx.png",
                "mobile": False
            },
            "url": "http://mandrill.com",
            "ts": 1678229076
        }
    ]
}


socketio_events = [
    {
        "event": "send",
        "ts": 1678229076
    },
    {
        "event": "open",
        "ts": 1678229076
    },
    {
        "event": "click",
        "ts": 1678229076
    }
]


@pytest.fixture()
def app_fixture():
    """
    Create Flask app object
    """
    return app


@pytest.fixture()
def socketio_fixture():
    """
    Create Flask socketio object
    """
    return socketio


@pytest.fixture()
def app_client(app_fixture):
    """
    Create Flask app test_client object
    :param app_fixture: Pytest Fixture as specified in the ConfTest File
    """
    return app_fixture.test_client()


@pytest.fixture()
def socketio_client(socketio_fixture, app_fixture):
    """
    Create Flask socketio test_client object
    :param socketio_fixture: Pytest Fixture as specified in the ConfTest File
    :param app_fixture: Pytest Fixture as specified in the ConfTest File
    """
    return socketio_fixture.test_client(app_fixture, namespace="/events")


@pytest.fixture()
def mongo_db_patch():
    """
    Create monkeypatch for connection to mock mongodb instance
    """
    def get_mongodb_collection():
        return mongomock.MongoClient().db.collection
    
    return get_mongodb_collection


@pytest.fixture()
def webhook_events_json():
    """
    Create json object for webhook testing
    """
    return {"mandrill_events": json.dumps(mandrill_events_json["mandrill_events"])}


@pytest.fixture()
def webhook_events_wrong_json():
    """
    Create empty json object for webhook testing
    """
    return {}


@pytest.fixture()
def webhook_events_empty_event_list():
    """
    Create empty event_list json object for webhook testing
    """
    return {"mandrill_events": json.dumps([])}


@pytest.fixture()
def socketio_events_emit():
    """
    Create socketio emit events json object
    """
    return socketio_events
