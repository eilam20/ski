import base64
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import requests
API_URL = "https://eilam20.pythonanywhere.com/api/pending-orders/"

USERNAME = "sharon"
PASSWORD = "8213517"

# Encode credentials in Base64 for Basic Authentication
credentials = f"{USERNAME}:{PASSWORD}".encode("utf-8")
auth_header = base64.b64encode(credentials).decode("utf-8")
headers = {"Authorization": f"Basic {auth_header}"}
today_date = datetime.today().strftime("%d/%m/%Y")  # Format: DD/MM/YYYY

response = requests.get(API_URL, headers=headers)

# Fetch pending orders
if response.status_code == 200:
    pending_orders = response.json()

    if pending_orders:
        # Create an HTML table for the email
        table_rows = "".join([
            f"<tr><td>{order['id']}</td><td>{order['name']}</td><td>{order['phone']}</td>"
            f"<td>{order['location']}</td><td>{order['return_date']}</td><td>{order['pack'] or ''}</td></tr>"
            for order in pending_orders
        ])

        html_message = f"""
            <html>
            <body>
                <h2>דוח השכרות פעילות - {today_date}</h2>
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
        """

        # פרטי ה-SMTP של Outlook
        SMTP_SERVER = "smtp.gmail.com"
        SMTP_PORT = 587
        EMAIL_SENDER = "eilamelimelech@gmail.com"
        EMAIL_PASSWORD = "wpws eydb hymb nvdz"
        EMAIL_RECEIVER1 = "eilamelimelech@gmail.com"
        EMAIL_RECEIVER2 = "s0522614095@gmail.com"

        # יצירת הודעת המייל
        msg = MIMEMultipart()
        msg["From"] = EMAIL_SENDER
        msg["To"] = EMAIL_RECEIVER1
        msg["Subject"] = f"השכרות פעילות- {today_date}"
        msg.attach(MIMEText(html_message, "html"))

        try:
            # יצירת חיבור לשרת SMTP של Outlook
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.starttls()  # הפעלת הצפנת TLS
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)  # התחברות עם שם משתמש וסיסמה
            server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER1, msg.as_string())  # שליחת המייל
            server.quit()
            print("✅ האימייל נשלח בהצלחה!")
        except Exception as e:
            print(f"❌ שגיאה בשליחת האימייל: {e}")

        # יצירת הודעת המייל
        msg = MIMEMultipart()
        msg["From"] = EMAIL_SENDER
        msg["To"] = EMAIL_RECEIVER2
        msg["Subject"] = f"השכרות פעילות- {today_date}"
        msg.attach(MIMEText(html_message, "html"))

        try:
            # יצירת חיבור לשרת SMTP של Outlook
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.starttls()  # הפעלת הצפנת TLS
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)  # התחברות עם שם משתמש וסיסמה
            server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER2, msg.as_string())  # שליחת המייל
            server.quit()
            print("✅ האימייל נשלח בהצלחה!")
        except Exception as e:
            print(f"❌ שגיאה בשליחת האימייל: {e}")

    else:
        print("❌ לא נמצאו הזמנות ממתינות.")
else:
    print('error')