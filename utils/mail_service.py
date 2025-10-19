from flask_mail import Message
from flask import current_app
from threading import Thread

def send_async_mail(app, msg):
    with app.app_context():
        current_app.mail.send(msg)

def send_email(subject, recipients, body):
    try:
        from app import app  # Flask ana uygulaması
        msg = Message(subject, sender=current_app.config['MAIL_USERNAME'], recipients=recipients)
        msg.body = body
        Thread(target=send_async_mail, args=(app, msg)).start()
        return True
    except Exception as e:
        print("E-posta gönderilemedi:", e)
        return False

def send_welcome_email(user_email, user_name):
    subject = "Kütüphaneye Hoş Geldiniz!"
    body = f"Merhaba {user_name},\n\nKütüphane sistemimize kaydınız başarıyla tamamlandı.\nİyi okumalar!"
    send_email(subject, [user_email], body)

def send_due_reminder(user_email, book_title, due_date):
    subject = "Kitap Teslim Hatırlatması"
    body = f"Merhaba,\n\n'{book_title}' kitabının teslim tarihi {due_date.strftime('%d.%m.%Y')}.\nLütfen zamanında iade ediniz."
    send_email(subject, [user_email], body)
