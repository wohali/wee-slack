import pytest
import collections
import sys

sys.path.append(".")
#sys.path.append(str(pytest.config.rootdir))

from wee_slack import SlackServer
from wee_slack import Channel
from wee_slack import User
from wee_slack import Message
from wee_slack import SearchList
import wee_slack


class FakeWeechat():
    """
    this is the thing that acts as "w." everywhere..
    basically mock out all of the weechat calls here i guess
    """
    WEECHAT_RC_OK = True

    def __init__(self):
        pass
        #print "INITIALIZE FAKE WEECHAT"
    def prnt(*args):
        output = "("
        for arg in args:
            if arg != None:
                output += "{}, ".format(arg)
        print "w.prnt {}".format(output)
    def hdata_get(*args):
        return "0x000001"
    def hdata_pointer(*args):
        return "0x000002"
    def hdata_time(*args):
        return "1355517519"
    def hdata_string(*args):
        return "testuser"
    def buffer_new(*args):
        return "0x8a8a8a8b"

    def __getattr__(self, name):
        def method(*args):
            pass
            #print "called {}".format(name)
            #if args:
            #    print "\twith args: {}".format(args)
        return method

@pytest.fixture
def mock_weechat():
    wee_slack.w = FakeWeechat()
    wee_slack.config = wee_slack.PluginConfig()
    wee_slack.debug_string = None
    wee_slack.slack_debug = "debug_buffer_ptr"
    wee_slack.STOP_TALKING_TO_SLACK = False
    pass


@pytest.fixture
def server(mock_weechat, monkeypatch):
    def mock_connect_to_slack(*args):
        return True
    monkeypatch.setattr(SlackServer, 'connect_to_slack', mock_connect_to_slack)
    myserver = SlackServer('xoxo-12345')
    myserver.server_buffer_name = 'test.slack.com'
    myserver.identifier = 'test.slack.com'
    myserver.nick = 'myusername'
    return myserver

@pytest.fixture
def myservers(server):
    servers = SearchList()
    servers.append(server)
    return servers

@pytest.fixture
def normalChannel(monkeypatch, server):
    """
    A basic wee-slack channel.
    """
    def mock_buffer_prnt(*args):
        print "called buffer_prnt\n\twith args: {}".format(args)
        return

    def mock_create_buffer(*args):
        return "0x101010"

    def mock_do_nothing(*args):
        #print args
        return True

    #monkeypatch.setattr(Channel, 'create_buffer', mock_create_buffer)
    monkeypatch.setattr(Channel, 'attach_buffer', mock_do_nothing)
    monkeypatch.setattr(Channel, 'set_topic', mock_do_nothing)
    monkeypatch.setattr(Channel, 'set_topic', mock_do_nothing)
    monkeypatch.setattr(Channel, 'buffer_prnt', mock_buffer_prnt)

    chan = {
        "name": "#test-chan",
        "id": "C2147483705",
        "is_open": "True",
        "last_read": "0",
        "prepend_name": "",
        "members": [],
        "topic": {"value": "sometopic"},
    }
    mychannel = Channel(server, **chan)
    return mychannel

@pytest.fixture
def mychannels(normalChannel):
    channels = SearchList()
    channels.append(normalChannel)
    return channels

@pytest.fixture
def user(monkeypatch, server):
    wee_slack.domain = None
    pass
    myuser = User(server, "testuser", 'U2147483697', presence="away")
    myuser.color = ''
    return myuser

@pytest.fixture
def myusers(monkeypatch, user):
    users = SearchList()
    users.append(user)
    return users

@pytest.fixture
def mymessages():
    msg = {
        "type": "message",
        "channel": "C2147483705",
        "user": "U2147483697",
        "text": "Was there was there was there what was there was there what was there was there there was there.",
        "ts": "1482960137.003543",
        "source_team": "T061EG9R6",
        "_server": "test.slack.com"
    }
    m = Message(msg)
    return [m]


Slack = collections.namedtuple('Slack', 'server channel user message')

@pytest.fixture
def myslack(monkeypatch, myservers, mychannels, myusers, mymessages):
    return Slack(myservers, mychannels, myusers, mymessages)
