import asyncio
from pyppeteer import launch
from pyppeteer.errors import TimeoutError
import requests

login_url = 'https://twitter.com/i/flow/login'

user_name = 'username'
current_password = 'currentpassword'
new_password = 'newpassword'
email = 'example@gmail.com'

async def passChanger():
    browser = await launch(
      headless=True,
      handleSIGINT=False,
      handleSIGTERM=False,
      handleSIGHUP=False
    )
    page = await browser.newPage()
    await page.setViewport({'width': 1500, 'height': 800})
    await asyncio.wait([
      page.goto(login_url),
      page.waitForSelector('input[autocomplete="username"]')
    ])
    await page.type('input[autocomplete="username"]', user_name)
    await page.click('div[class="css-18t94o4 css-1dbjc4n r-sdzlij r-1phboty r-rs99b7 r-ywje51 r-usiww2 r-2yi16 r-1qi8awa r-1ny4l3l r-ymttw5 r-o7ynqc r-6416eg r-lrvibr r-13qz1uu"]')
    await page.waitForSelector('input[autocomplete="current-password"]')
    await page.type('input[autocomplete="current-password"]', current_password)
    await page.click('div[data-testid="LoginForm_Login_Button"]')

    # メールアドレスの認証が必要なとき
    try:
      await page.waitForSelector('div[data-testid="AppTabBar_More_Menu"]')
    except TimeoutError:
      await page.waitForSelector('input[autocomplete="email"]')
      await page.type('input[autocomplete="email"]', email)
      await page.click('div[data-testid="ocfEnterTextNextButton"]')
      await page.waitForSelector('div[data-testid="AppTabBar_More_Menu"]')

      print('timeout')

    await page.click('div[data-testid="AppTabBar_More_Menu"]')

    await page.waitForSelector('a[data-testid="settings"]')
    await page.click('a[data-testid="settings"]')

    await page.waitForSelector('a[href="/settings/password"]')
    await page.click('a[href="/settings/password"]')

    await page.waitForSelector('input[name="current_password"]')
    await page.type('input[name="current_password"]', current_password)
    await page.waitForSelector('input[name="new_password"]')
    await page.type('input[name="new_password"]', new_password)
    await page.waitForSelector('input[name="password_confirmation"]')
    await page.type('input[name="password_confirmation"]', new_password)
    await page.click('div[data-testid="settingsDetailSave"]')
    print('click save')
    await asyncio.sleep(2)
    await page.close()

def main(event, context):
  asyncio.run(passChanger())

  # LINEで送信
  line_notify_token = 'token'
  line_notify_api = 'https://notify-api.line.me/api/notify'
  headers = {'Authorization': f'Bearer {line_notify_token}'}
  data = {'message': 'パスワードを変更しました'}
  requests.post(line_notify_api, headers=headers, data=data)

