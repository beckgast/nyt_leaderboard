import json
import requests
import csv
from bs4 import BeautifulSoup as soup 
from datetime import datetime


def get_config():
    with open('config.json', 'r') as config_file:
        config = json.loads(config_file.read())
        return config

def login(username, password):
    login_resp = requests.post(
        'https://myaccount.nytimes.com/svc/lire_ui/login',
        data={
            'login': username,
            'password': password,
            "form_view": "login",
            "remember_me": "Y",
            "auth_token": "H4sIAAAAAAAAA32Qy2rDMBBF/0WQrkJs2Y78gFC6aMDpqo9AdkYejRIR2RaSnDSk+ffKXnZRGAbmMnM5c+8ElBKkInLUujH8iGRJQCvs/SxfVJiFckbzG6kk1w6XBL+NsuhIRVlG4zIrimRJzGU+SBmUiC2klLI0zmkpJNCUISZlksVssrfIBdp62p4nEczAN6NVQTl5b1wVRdfrddXfvOrQrWDoIje2DqwyXg191I3aK2MHMYKPtCne3vefq5Pv9DPwznB17GuxyXfb3eHp9VB/NfuPejMbL9KXRbIN9cc+KDOKM0PvsPE3g4EFhuGsJmJvz6S6E+4c+qB33PlTeGI+kWgt2kCv/6Enj8cPbWnaUiwkWyOAwKxlMpNIMeTEWJazAoGH0EraArYZ5OuQGpdTi0UM8heqt6xXqwEAAA=="
        },
        headers={
            "accept": "application/json",
            "accept-language": "en-US,en;q=0.9",
            "content-type": "application/json",
            "req-details": "[[it:lui]][[kp:off]]",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "sec-gpc": "1",
            "x-pageview-id": "75Jf8ajoTTKJ2R1uf0CShlHy",
            "cookie": "nyt-a=LCvSFl4h-yDMqmVmE6xnVE; purr-cache=<K0<r<C_<G_<S0; nyt-auth-method=username; nyt-gdpr=0; nyt-geo=US; b2b_cig_opt=%7B%22isCorpUser%22%3Afalse%7D; edu_cig_opt=%7B%22isEduUser%22%3Afalse%7D; SIDNY=CA0SJQjUusSOBhCQu8SOBhoSMS3-k-6ccX5Crh9Qj--2QoUYIO6AvCUaQEAnDvAzQQqTskm0ILWzEn5ySSwRK23p-BFgnPJLKW10jj6es0ygBcunCrrYfgRTgKXSIUgCdF4Z8XIBcEAxFwQ=; nyt-b3-traceid=c3f66f58113844558e2adbb70afed698; nyt-purr=cfhhcfhhhckf; nyt-m=93F1799033AE1DA731CFCBF981475556&iue=i.0&imv=i.0&iru=i.1&uuid=s.c0436f49-1195-4757-b7e7-3f8053ef44fb&vp=i.0&igd=i.0&iir=i.0&g=i.0&rc=i.0&pr=l.4.0.0.0.0&imu=i.1&ica=i.0&v=i.0&ifv=i.0&e=i.1643706000&ier=i.0&igf=i.0&ird=i.0&n=i.2&er=i.1641094580&vr=l.4.0.0.0.0&ft=i.0&fv=i.0&prt=i.0&iub=i.0&s=s.core&cav=i.0&igu=i.1&iga=i.0&ira=i.0&t=i.1; nyt-jkidd=uid=78577774&lastRequest=1641094580852&activeDays=%5B0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C1%2C0%2C0%2C0%2C0%2C0%2C0%2C1%5D&adv=2&a7dv=1&a14dv=2&a21dv=2&lastKnownType=regi; datadome=~JAwf.Q9EuY0sCcXFYTf7jagbYkNM.F_ihXBl9c4JJUYhYy_bRxO7Yzgk0T0P3SUW5MprRRB2oIvM9sJpG-Y0xGq-p~ILZLR~.om8~CGmeTXADR3sGXfnH_dw4uOPyW",
            "Referer": "https://myaccount.nytimes.com/auth/login?response_type=cookie&client_id=vi&redirect_uri=https%3A%2F%2Fwww.nytimes.com%2Fsubscription%2Fmultiproduct%2Flp8KQUS.html%3FcampaignId%3D7JFJX%26EXIT_URI%3Dhttps%253A%252F%252Fwww.nytimes.com%252F&asset=masthead",
            "Referrer-Policy": "strict-origin-when-cross-origin"
        }
    )
    login_resp.raise_for_status()
    for cookie in login_resp.json()['data']['cookies']:
        if cookie['name'] == 'NYT-S':
            return cookie['cipheredValue']
    raise ValueError('NYT-S cookie not found')


def get_mini_times(cookie, output):
    url = "https://www.nytimes.com/puzzles/leaderboards"
    response = requests.get(url, cookies={
        'NYT-S': cookie,
    },
    )
    page = soup(response.content, features='html.parser')
    solvers = page.find_all('div', class_='lbd-score')
    current_datetime = datetime.now()
    row=[]
    print('received response@{}'.format(current_datetime))
    for solver in solvers:
        name = solver.find('p', class_='lbd-score__name').text.strip()
        try:
            time = solver.find('p', class_='lbd-score__time').text.strip()
        except:
            time=None
        if time == "--":
            time=None
        if name.endswith("(you)"):
            name_split = name.split()
            name = name_split[0]
        row.append([str(current_datetime), name, time])
    with open(output, 'a') as csvfile:  
        csvwriter = csv.writer(csvfile)              
        csvwriter.writerows(row) 

#boom
if __name__ == '__main__':
    config = get_config()
    cookie = config['cookie']#login(config["username"], config["password"])
    get_mini_times(cookie, "output.csv")