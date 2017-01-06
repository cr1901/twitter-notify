import time

# Notification wrapper
class Notification:
    Timeline, Direct = range(2)

    def __init__(self, sender, text, sort_id, msg_type=Timeline):
        self.sender = sender
        self.text = text
        self.id = sort_id
        self.msg_type = msg_type

# Source object of Twitter notifications
class Source:
    def __init__(self, api, num_msgs=20, sleep_time=90):
        self.api = api
        self.msgs = dict() # "Windows" of most recent 20 messages after startup.
        self.dms = dict()
        # self.dms = []
        self.num_msgs= num_msgs
        self.sleep_time = sleep_time

    def __iter__(self):
        return self.get_msgs()

    def get_msgs(self):
        mentions = self.api.mentions_timeline(self.num_msgs)
        messages = self.api.direct_messages(self.num_msgs)
        tmp_msgs = dict()
        tmp_dms = dict()
        new_replies = False
        new_dms = False

        # for m, d in zip(reversed(mentions), reversed(messages)):
        for m in reversed(mentions):
            msg = Notification(m.user.screen_name, m.text, m.id)
            # if not m.id in self.msgs:
            if not msg.id in self.msgs:
                new_replies = True
                tmp_msgs[msg.id] = msg
                yield msg

        for d in reversed(messages):
            dm = Notification(d.sender.screen_name, d.text, d.id, Notification.Direct)
            # if not d.id in self.dms:
            if not dm.id in self.dms:
                new_dms = True
                tmp_dms[dm.id] = dm
                yield dm


        # Replace message dict with those seen this iter of API call.
        # Don't bother if nothing to do.
        if new_replies:
            self.msgs = tmp_msgs
        if new_dms:
            self.dms = tmp_dms

        time.sleep(90)
