# ponddy_download_sprout_video
```
pipenv shell
pipenv install
```

Download by {month}, Search pages {start_page} to {end_page} of sprout
```
python main.py -u {username} -p {password} -s {start_page} -e {end_page} -y {year} -m {month}
```

```
-p, dest='password', help='Password', type=str
-u, dest='username', help='Username', type=str
-s, dest='start', help='Start', type=int
-e, dest='end', help='End', type=int
-y, dest='year', help='Year', type=int
-m, dest='month', help='Month', type=int
```
