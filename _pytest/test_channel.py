import wee_slack
import pytest

slack = wee_slack

def test_channel_stuff(myslack):
    #print myslack.channel[0].get_aliases()
    #print myslack.channel[0].create_buffer()
    print myslack.channel[0].channel_buffer
    print myslack.channel[0].active
    print myslack.message
    print myslack.server[0].get_aliases()
    print "-----------------------"
    print wee_slack.process_message(myslack.message[0].message_json)
    #print myslack.server[0].set_away("byeee")
    #assert False
