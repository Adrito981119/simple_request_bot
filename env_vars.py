import os

#env vars
_token = os.environ['TOKEN']
_target = os.environ['TARGET']
_channel = os.environ['ID_CHANNEL']


def get_my_token(): return _token

def get_log_chat(): return _target

def get_channel(): return _channel
