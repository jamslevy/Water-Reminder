import os, datetime, logging

from utils import defer, Debug
import app_settings 

from model import Subscriber

"""

Deferred Water Reminder Methods

"""

def schedule_checks(phone_number, days_subscribed):
  """ schedule checks at precise intervals throughout day for a subscriber """
  caller = Subscriber.get_by_key_name(str(phone_number))
  # TODO: use caller.zip_code to adjust call times for timezones
  now = datetime.datetime.now()
  if now.hour < 17:
    now_day = (now - datetime.timedelta(days=1))
  else:
    now_day = now
  for day in range(days_subscribed):
    now_day += datetime.timedelta(days=1)
    for check_time in (13, 15, 17):
      check_time -= 4 #for New York. 7 for San Francisco 
      eta = datetime.datetime(year=now_day.year,
      month=now_day.month,day=now_day.day, hour=check_time)
      if eta < now: 
        continue
      defer(scheduled_check, phone_number,caller.call_guid, _eta=eta)

def scheduled_check(phone_number, call_guid):
  """ deferred scheduled check - send reminder if sufficient time has passed """
  caller = Subscriber.get_by_key_name(str(phone_number))
  if caller.call_guid != call_guid:
    logging.critical("Call Guid has been reset - aborting reminder check")
    return
  if caller.last_scan < (datetime.datetime.now() - datetime.timedelta(hours=2)):
    import web_services.twilio
    web_services.twilio.sendTextMessage(
    caller.phone_number, app_settings.REMINDER_MSG)
    logging.info('Sending text message to %s' % caller.key().name())
  else:
    logging.info('Not sending text message to %s' % caller.key().name())
  
