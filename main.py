import os
import requests

from argparse import ArgumentParser

from bs4 import BeautifulSoup


HOST = 'https://sproutvideo.com'


def login(username, password):
    req = requests.Session()

    res = req.get(f'{HOST}/login')
    soup = BeautifulSoup(res.text, 'html.parser')
    data = {}

    for form in soup.select('.new_user_session input'):
        data[form.get('name')] = form.get('value')

    data.update({
        'user_session[email]': username,
        'user_session[password]': password,
    })
    req.post(f'{HOST}/user_sessions', data=data)

    return req


def get_videos(req, page):
    res = req.get(f'{HOST}/videos?page={page}')
    soup = BeautifulSoup(res.text, 'html.parser')
    elements = soup.select('.video-tr.deployed .video-title a')
    result = []
    for element in elements:
        video_id = element.get('href').split('/')[-1]
        date = '-'.join(element.text.split('-')[0:3])
        result.append((video_id, date))

    return result


def download_video(req, video_id):
    if not os.path.exists('videos'):
        os.makedirs('videos')

    res = req.get(
        f'{HOST}/videos/{video_id}/download',
        params={'type': 'sd'},
        stream=True,
    )
    filename = res.headers['Content-Disposition'].split('filename=')[1]
    with open(os.path.join('videos', f'{filename}'), 'wb') as video:
        [video.write(chunk) for chunk in res]


def main():
    parser = ArgumentParser(description='Video Download....')
    parser.add_argument('-u', dest='username', help='Username', type=str, required=True)  # noqa: E501
    parser.add_argument('-p', dest='password', help='Password', type=str, required=True)  # noqa: E501
    parser.add_argument('-s', dest='start', help='Start', type=int, required=True)  # noqa: E501
    parser.add_argument('-e', dest='end', help='End', type=int, required=True)  # noqa: E501
    parser.add_argument('-y', dest='year', help='Year', type=int, required=True)  # noqa: E501
    parser.add_argument('-m', dest='month', help='Month', type=int, required=True)  # noqa: E501
    args = parser.parse_args()

    req = login(args.username, args.password)
    for page in range(args.start, args.end+1):
        for video_id, date in get_videos(req, page):
            video_date = date.split('-')[0:2]
            print(f'Get {video_id} at {date}', end=': ')
            if int(video_date[0]) != args.year or int(video_date[1]) != args.month:  # noqa: E501
                print('skip')
                continue

            download_video(req, video_id)
            print('done')


if __name__ == '__main__':
    main()
