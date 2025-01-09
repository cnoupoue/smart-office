import env
import webex_api
import shodan_api
import sendgrid_api
import twilio_api
import time
import threading
import mongo_api
from mqtt import MQTT

def encapsulate_into_vuln_html(list):
    vulnerabilities_table = ""
    for vuln in list:
        vulnerabilities_table += f"""
        <tr>
        <td style="padding: 8px; border: 1px solid #ddd;">{vuln['cve_id']}</td>
        <td style="padding: 8px; border: 1px solid #ddd; color: #f0ad4e;">{vuln['severity']}</td>
        <td style="padding: 8px; border: 1px solid #ddd;">{vuln['base_score']}</td>
        <td style="padding: 8px; border: 1px solid #ddd;">{vuln['impact']}</td>
        <td style="padding: 8px; border: 1px solid #ddd; text-align: justify;">{vuln['description']}</td>
        </tr>
        """
    return f"""
<div style="font-family: Arial, sans-serif; line-height: 1.5; color: #333;">
  <h2 style="color: #d9534f;">Rapport de vulnérabilités pour Ubuntu server (89.168.47.217)</h2>
  
  <!-- Start Table for Multiple Vulnerabilities -->
  <table style="width: 100%; border-collapse: collapse;">
    <thead>
      <tr style="background-color: #f8f8f8;">
        <th style="padding: 10px; text-align: left; border: 1px solid #ddd; font-weight: bold;">CVE ID</th>
        <th style="padding: 10px; text-align: left; border: 1px solid #ddd; font-weight: bold;">Severity</th>
        <th style="padding: 10px; text-align: left; border: 1px solid #ddd; font-weight: bold;">Base Score</th>
        <th style="padding: 10px; text-align: left; border: 1px solid #ddd; font-weight: bold;">Impact on Availability</th>
        <th style="padding: 10px; text-align: left; border: 1px solid #ddd; font-weight: bold;">Description</th>
      </tr>
    </thead>
    <tbody>
      <!-- Loop to Insert Each Vulnerability Entry -->
      {vulnerabilities_table}
    </tbody>
  </table>
  <!-- End Table -->

</div>     
"""

def execute_command():
    # get and send short shodan results via sms
    msg_for_sms = shodan_api.get_vuln_message_for_sms()
    twilio_api.send(msg_for_sms)
    webex_api.send_message("SMS envoyé!")

    def send_email():
        # get and send long shodan results via email
        list_vuln_for_email = shodan_api.get_vuln_list_for_email()
        sendgrid_api.send(message=encapsulate_into_vuln_html(list_vuln_for_email))
        webex_api.send_message("Email envoyé!")

    # Create threads for email
    email_thread = threading.Thread(target=send_email)
    email_thread.start()
    email_thread.join()

def save_mqtt_logs():
    MQTTC = MQTT(sub_callback = callback, 
                 secured=True, 
                 ca_certs="mosquitto.org.crt",
                 certfile="clientcrt.pem",
                 keyfile="clientkey.pem")
    MQTTC.connect("test.mosquitto.org", 8883)
    MQTTC.publish("test", "hello")
    MQTTC.subscribe("test")
    while True:
        time.sleep(2)
def callback(topic, message):
    print(topic, message)
def start_webex_handler():
    print("Waiting for new messages...")
    webex_api.init()
    while True:
        command = webex_api.wait_for_command()

        if command == 'shodan':
            print("command received")
            message = "Requête shodan envoyé. Vous recevrez les résultats par mail (prend quelques minutes) et SMS."
            webex_api.send_message(message)
            execute_command()

        time.sleep(1)  # Check for new messages every 10 seconds

threading.Thread(target=save_mqtt_logs).start()
# start_webex_handler()
