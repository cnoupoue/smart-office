from twilio.rest import Client
import env

client = Client(env.TWILIO_SID, env.TWILIO_TOKEN)

def send(message:str):
    message = client.messages.create(
        messaging_service_sid='MG188042bc9a590cc663250e41c6c538cc',
        body=message,
        to='+32467794640'
    )
    print("sms sent")
