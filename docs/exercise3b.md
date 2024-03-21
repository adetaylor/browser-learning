# Exercise 3b: encryption

Do the same thing, but:

* Use `https_server.py` instead of `http_server.py`
* Navigate to `https://localhost:4443/exercise1b.html` instead of `http://localhost:8000/exercise1b.html` (note _both_ the different number, and the extra `s` on the end of `http`)
* Use a slightly different `tcpdump` command:

```
sudo tcpdump -i lo -A 'tcp port 4443'
```

What do you see now?