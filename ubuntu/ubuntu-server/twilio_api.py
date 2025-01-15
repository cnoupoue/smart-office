from twilio.rest import Client
import env

client = Client(env.TWILIO_SID, env.TWILIO_TOKEN)

def send(message:str):
    message = client.messages.create(
        messaging_service_sid=env.TWILIO_MESSAGE_SERVICE_SID,
        body=message,
        to=env.TWILIO_DESTINATION_NUMBER
    )
    print("sms sent")
