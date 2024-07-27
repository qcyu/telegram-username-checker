import cloudscraper
from bs4 import BeautifulSoup

scraper = cloudscraper.create_scraper(
    browser={
        'browser': 'chrome',
        'platform': 'windows',
        'desktop': True
    }
)


def get_user(username: str):
    url = f'https://fragment.com/username/{username}'
    response = scraper.get(url)
    response.encoding = 'utf-8'
    if response.status_code == 403:
        return "Response code is 403.\nYour request likely was flagged by Cloudflare and it requires captcha, try to slow down or change IP"

    soup = BeautifulSoup(response.text, 'html.parser')
    status_section = soup.find(class_='tm-section-header-status')

    if not status_section:  # note that some usernames might be blocked by Telegram, even if status is free
        return '✅ free'

    status_class = status_section.get('class', [])
    status_dict = {
        'tm-status-taken': '❌ taken',
        'tm-status-avail': '💶 for sale',
        'tm-status-unavail': '❌ unavailable'
    }

    for status in status_dict.keys():
        if status in status_class:
            return status_dict[status]


def main():
    print("1 - print only avaiable | 2 - print all")
    select = int(input("Select: "))
    if select not in [1, 2]:
        return main()

    with open('usernames.txt', 'r') as file:
        for line in file:
            username = line.strip().lower()
            if len(username) >= 4:
                status = get_user(username)
                if select == 1:
                    if status == '✅ free':
                        print(f'{username} | {status}')
                        with open('available.txt', 'a') as u:
                            u.write(f"{username}\n")
                if select == 2:
                    if status:
                        print(f'{username} | {status}')
                        if status == '✅ free':
                            with open('available.txt', 'a') as u:
                                u.write(f"{username}\n")
    print("Available usernames was saved into available.txt")


if __name__ == '__main__':
    main()
