Jiawen Wang 260683456
- You'll need to install Stripe; In particular I used this tutorial https://testdriven.io/blog/django-stripe-tutorial/
- You'll need to change the `MEDIA_ROOT`, located at the very end of `settings.py` to point to a directory on your local computer
- You'll need to have redis-server running for chatroom functionality. On my Mac, I just used `brew install redis` and ran the standard version with no configuration file with `redis-server` and making sure that running `redis-cli ping` returns `PONG`