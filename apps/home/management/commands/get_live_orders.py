import os
import django
from django.utils.html import format_html
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ski.settings")  # Adjust if needed
django.setup()
from apps.home.models import Order  # Adjust the import based on your project

# Fetch pending orders
pending_orders = Order.objects.filter(done=False)

if pending_orders.exists():
    # Create an HTML table for the email
    table_rows = "".join([
        f"<tr><td>{order.id}</td><td>{order.name}</td><td>{order.phone}</td>"
        f"<td>{order.location}</td><td>{order.return_date}</td><td>{order.pack or ''}</td></tr>"
        for order in pending_orders
    ])

    html_message = format_html(f"""
        <html>
        <body>
            <h2>רשימת הזמנות </h2>
            <table border="1" cellpadding="5" cellspacing="0" style="border-collapse: collapse;">
                <tr>
                    <th>מספר הזמנה</th>
                    <th>שם</th>
                    <th>טלפון</th>
                    <th>מיקום</th>
                    <th>תאריך החזרה</th>
                    <th>חליפות</th>
                </tr>
                {table_rows}
            </table>
        </body>
        </html>
    """)
    print(html_message)

    # פרטי ה-SMTP של Outlook
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587
    EMAIL_SENDER = "eilamelimelech@gmail.com"
    EMAIL_PASSWORD = "wpws eydb hymb nvdz"
    EMAIL_RECEIVER = "eilamelimelech@gmail.com"

    # יצירת הודעת המייל
    msg = MIMEMultipart()
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER
    msg["Subject"] = "דוח הזמנות ממתינות"
    msg.attach(MIMEText(html_message, "html"))

    try:
        # יצירת חיבור לשרת SMTP של Outlook
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # הפעלת הצפנת TLS
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)  # התחברות עם שם משתמש וסיסמה
        server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())  # שליחת המייל
        server.quit()
        print("✅ האימייל נשלח בהצלחה!")
    except Exception as e:
        print(f"❌ שגיאה בשליחת האימייל: {e}")

else:
    print("❌ לא נמצאו הזמנות ממתינות.")