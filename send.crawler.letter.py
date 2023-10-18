import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from dotenv import load_dotenv
import datetime

load_dotenv()

# 主旨時間
current_datetime = datetime.datetime.now()
current_datetime_str = current_datetime.strftime('%Y-%m-%d %H:%M:%S')

# 你的郵件設置
smtp_server = os.getenv("SMTP_SERVER")
smtp_port = os.getenv("SMTP_PORT")
smtp_username = os.getenv("USERNAME")
smtp_password = os.getenv("PASSWORD")
sender_email = os.getenv("SENDER_EMAIL")
recipient_email = os.getenv("RECIPIENT_EMAIL")

# 創建郵件
message = MIMEMultipart()
message['From'] = sender_email
message['To'] = recipient_email
message['Subject'] = f'{current_datetime_str} 爬蟲資料'

# 添加郵件內文
message.attach(MIMEText('這是工作資料的附件。', 'plain'))

# 添加附件
with open('job_data.csv', 'rb') as file:
    part = MIMEApplication(file.read(), Name='job_data.csv')
    part['Content-Disposition'] = f'attachment; filename="job_data.csv"'
    message.attach(part)

# 連接到 SMTP 伺服器並發送郵件
try:
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()  # 建立加密傳輸
    server.login(smtp_username, smtp_password)
    server.sendmail(sender_email, recipient_email, message.as_string())
    server.quit()
    print('郵件已成功發送')
except Exception as e:
    print('郵件發送失敗:', str(e))
