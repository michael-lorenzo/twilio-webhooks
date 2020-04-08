# twilio-webhooks

A collection of webhooks for [Twilio](https://www.twilio.com/) using [Flask](https://palletsprojects.com/p/flask/).

# Installation

```console
pip install twilio-webhooks
```

**Availible webhooks:**

- [SMSCommand](#SMSCommand) - When receiving a properly formated SMS runs a user-defined callable.
- [ReceiveFax](#ReceiveFax) - When receving a fax saves a pdf file to a user-defined path.

# SMSCommand

**Webhook URL format:**

> http://example.com/smscommand

You set this under "Phone Numbers / Manage Numbers / Active Numbers". Click your desired phone number. Look under a section called "Messaging", and with the "CONFIGURE WITH" drop-down menu select "Webhooks, TwiML Bins, Functions, Studio or Proxy". Now under the "A MESSAGE COMES IN" drop-down menu select "Webhook" and in the adjacent box place your URL.

**Callback format:**

The callable should accept two arguments.

1. A string containing who the SMS is from in E.164 format.
2. A string that is either emtpy or the arg (see below) sent in the SMS.

A return value will be sent as a reply.

**SMS Format:**

> `command` [`arg`]

- `command` (**required**) is a case-insensitive string that was assigned to a user-defined callable. 
- `arg` (**optional**) will be passed to the callable as the second argument.

**Deployment:**

Deploy this as you would any other Flask app. See [Deployment Options](https://flask.palletsprojects.com/en/1.1.x/deploying/) for more information.

**Example Code:**

```python
import psutil
import wakeonlan
from twilio_webhooks import SMSCommand

# Simple example

def cpu_usage(from_, arg):
    """Check CPU usage"""
    return f"CPU Usage: {psutil.cpu_percent()}%"

# Complex example

def wake_on_lan(from_, arg):
    """Use wake-on-lan to wake a computer"""
    # make sure the number is mine
    if from_ != "+12125551234":
        return
    computers = {"office": "ff.ff.ff.ff.ff.f1", "gaming": "ff.ff.ff.ff.ff.f2"}
    # Clean up arg in case I send a sloppy SMS
    arg = arg.strip().lower()
    if arg in computers:
        wakeonlan.send_magic_packet(computers[arg])
        return f'Computer "{arg}" is waking up.'


sc = SMSCommand("your_twilio_auth_token")
sc.assign("cpu", cpu_usage)
sc.assign("wol", wake_on_lan)

app = sc.wsgi()
```

Now if you send an SMS to the twilio number you selected earlier that says this (remember the command part is case-insensitive):

> Cpu

you should get a reply like this

> CPU Usage: 5.2%

or this:

> Wol office

should reply:

> Computer "office" is waking up.

# ReceiveFax

**Deployment:**

Deploy this as you would any other Flask app. See [Deployment Options](https://flask.palletsprojects.com/en/1.1.x/deploying/) for more information.

**Example:**

```python
from twilio_webhooks import ReceiveFax

app = ReceiveFax("your_twilio_auth_token", '/path/to/save/pdf').wsgi()
```

Incoming faxes will now be saved to the path of your choice.

# Notes:

* Your twilio auth token can be found under "Dashboard / Settings / General". You must click it to view it.
