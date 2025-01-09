import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import env

# BEFORE:
# echo "export SENDGRID_API_KEY='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'" > sendgrid.env
# echo "sendgrid.env" >> .gitignore
# source ./sendgrid.env

def send(subject:str = 'Résultat shodan', message:str = ""):
    message = Mail(
        from_email='neutrino.particule@gmail.com',
        to_emails='kotinass2003@gmail.com',
        subject=subject,
        html_content=message
    )

    try:
        # Send the email
        sg = SendGridAPIClient(env.SENDGRID_API)
        response = sg.send(message)
        print("email sent")
    except Exception as e:
        print(e)