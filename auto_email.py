
import yagmail



def send_email(recipient_email, subject, message):
    assistant="virtualassistantjarivs@gmail.com"
    cd="iumo kydt pwlm swrq"
    yag = yagmail.SMTP(assistant, cd)
    try:
        yag.send(to=recipient_email, subject=subject, contents=message)
        return(f"Email sent to {recipient_email} successfully! ")
    except Exception as e:
        return(f"Error sending email to {recipient_email}: {e}")




