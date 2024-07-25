# Kharon Service

This is the utility you must install on the private machine.

It does a couple of things:

1. Start SSH Server
2. Communicate with Kharon Server to exchange keys and authentify.
3. Regular health check on your server.

For now, Kharon will always look for `$KHARON_REMOTE_HOST:8080`, but more customization are coming! Please submit an issue if you
need this feature to help prioritization.