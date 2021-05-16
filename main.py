import requests, json, csv, smtplib, time
from datetime import date, timedelta, datetime
from email.message import EmailMessage

token = None
emails = ['flyinvoke@gmail.com', 'tushig.tushig@gmail.com', 'enkhee.ag@gmail.com']
credentials = []
with open("credentials.json", "r") as credentials_json:
    credentials = json.loads(credentials_json.read())

def login():
    params = (
        ('language', 'mn'),
    )
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json;charset=UTF-8',
        'Accept-Language': 'en-US,en;q=0.9',
    }
    data = '{"header":{"languageId":"001","time":"2020-04-18T14:56:05.155Z"},"body":{"type" : "SPWD","username":"' + credentials['username'] + '","password":"' + credentials['password'] + '"}}'
    response = requests.post('https://www.egolomt.mn/api/auth/login', headers=headers, params=params, data=data)
    if(response.status_code == 200):
        response = json.loads(response.content.decode('utf-8'))
        token = response['body']['token'] 
    else:
        raise Exception('Couldn`t login bro')  
    return token

def process(token, page):
    if (page is None):
        return []
    else:
        headers = {
            'Connection': "keep-alive",
            'Accept': "application/json, text/plain, */*",
            'Authorization': "Bearer "+ token,
            'Accept-Language': "en-US,en;q=0.9",
            'Content-Type' : 'application/json;charset=UTF-8'
        }
        today = str(date.today())
        days_before = str((date.today() - timedelta(days=1)))
        params = {
            'accountNumber' : '1505133672',
            'accountType' : 'SBA',
            'fromTxnDate' : days_before,
            'toTxnDate': today,
            'pageNumber': 1
        }
        body = {"header":{"languageId":"001","time":"2020-04-18T14:56:05.155Z"}, "body": params}
        response = requests.post('https://www.egolomt.mn/api/account/statement/inquire?language=mn', data=json.dumps(body), headers=headers)
        if(response.status_code == 200):
            response = json.loads(response.content.decode('utf-8'))
            if ('statements' in response['body']):
                for statement in response['body']['statements']:
                    checkIfSalary(statement)
        else:
            raise Exception('Couldn`t download data bro')

def checkIfSalary(statement):
    if ('remarks' in statement and statement['remarks'].find('150TSB11600') != -1):
        date = datetime.strptime(statement['txnPostedDate'], '%d-%m-%Y %H:%M:%S')
        if (date.today() - date < timedelta(hours=1)):
            for email in emails:
                print("Sending an email to" + email)
                send_email(email)
        else:
            print('here')

def send_email(email):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(credentials['email'], credentials['app_password'])
    msg = EmailMessage()
    message = 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA awraarai. Tsalin yumu okr yumu ali neg n law orchloo AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
    msg.set_content(message)
    msg['Subject'] = 'Salary notification from AWS'
    msg['From'] = 'tushig.tushig@gmail.com'
    msg['To'] = email
    server.send_message(msg)

def lambda_handler():
    token = login()
    if(token is not None):
        process(token, 1)
        print('Successful!')
    else:
        print('Login first bro')

