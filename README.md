# asyncio-practice

Python Sync vs. Async

## Test environments

python 3.8.2

- sync: requests (2.26.0)
- async: aiohttp (3.7.4.post0), asyncio (3.4.3)

### sync

```
$ python crawler/udnstar.py
```

For 122 requests, 'crawler/udnstar.py' finished in 42.18 secs.

### async

```
$ python crawler/async_udnstar.py
```

For 122 requests, 'crawler/async_udnstar.py' finished in 2.62 secs.
