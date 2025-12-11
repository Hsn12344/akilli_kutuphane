from flask_mail import Message
from threading import Thread
from flask import current_app


def send_async_mail(app, msg):
    with app.app_context():
        app.extensions['mail'].send(msg)


def send_email(subject, recipients, body):
    try:
        app = current_app._get_current_object()

        msg = Message(
            subject=subject,
            sender=app.config['MAIL_USERNAME'],
            recipients=recipients,
            body=body
        )

        Thread(target=send_async_mail, args=(app, msg)).start()
        return True

    except Exception as e:
        print("E-posta gönderilemedi:", e)
        return False


# ✅ 1️⃣ KULLANICI KAYIT MAİLİ
def send_welcome_email(user_email, user_name):
    subject = "Kütüphaneye Hoş Geldiniz!"
    body = f"""
Merhaba {user_name},

Kütüphane sistemimize kaydınız başarıyla tamamlandı.
Artık kitap ödünç alabilir ve tüm işlemlerinizi sistem üzerinden yönetebilirsiniz.

İyi okumalar dileriz.
"""
    send_email(subject, [user_email], body)


# ✅ 2️⃣ TESLİM TARİHİ HATIRLATMA MAİLİ
def send_due_reminder(user_email, book_title, due_date):
    subject = "📅 Kitap Teslim Hatırlatması"
    body = f"""
Merhaba,

'{book_title}' adlı kitabın son teslim tarihi:
{due_date.strftime('%d.%m.%Y')}

Lütfen gecikme yaşamamak için kitabınızı zamanında iade ediniz.
"""
    send_email(subject, [user_email], body)


# ✅ 3️⃣ GECİKME CEZASI MAİLİ (10 TL / GÜN)
def send_late_fine_email(user_email, book_title, delay_days, fine_amount):
    subject = "⏰ Geç İade Cezası Bildirimi"
    body = f"""
Merhaba,

'{book_title}' adlı kitabı {delay_days} gün gecikmeli iade ettiniz.

Uygulanan gecikme cezası:
{delay_days} gün × 10 TL = {fine_amount} TL
"""
    send_email(subject, [user_email], body)
