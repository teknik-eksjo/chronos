from . import mail
from flask import current_app, render_template
from flask_mail import Message
from threading import Thread


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, template, **kwargs):
    """Function for sending emails."""
    app = current_app._get_current_object()
    msg = Message(app.config['CHRONOS_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                  sender=app.config['CHRONOS_MAIL_SENDER'], recipients=[to], charset='utf-8')
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    # Sends email using another thread than the flask instance to be able to send it async.
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr
