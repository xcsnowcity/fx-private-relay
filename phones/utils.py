from decouple import config

from twilio.rest import Client


account_sid = config('TWILIO_ACCOUNT_SID', None)
auth_token = config('TWILIO_AUTH_TOKEN', None)
client = Client(account_sid, auth_token)
service = client.proxy.services(config('TWILIO_SERVICE_ID'))


def get_available_numbers():
    numbers = service.phone_numbers.list()
    available_numbers = [
        number.phone_number for number in numbers if number.in_use == 0
    ]
    if len(available_numbers) == 0:
        raise Exception("No available twilio numbers")

    return available_numbers


def get_session_and_participant_with_available_number(
    available_numbers, ttl_minutes, from_num
):
    # Since Twilio doesn't automatically assign phone numbers that are not
    # already in use, we need to keep trying to create a session until we get
    # a session with one of the available numbers.
    while True:
        session = service.sessions.create(ttl=ttl_minutes*60,)
        participant = service.sessions(session.sid).participants.create(
            identifier=from_num
        )
        if participant.proxy_identifier in available_numbers:
            return session, participant
        service.sessions(session.twilio_sid).update(status='closed')


def delete_expired_sessions():
    expired_sessions = Session.objects.filter(
        status='waiting-for-party',
        expiration__lte=datetime.now()
    )
    expired_sessions.delete()
