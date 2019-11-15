# SecondPassAlert
This is a small python automation test that sends a post to a slack channel of your choosing when second pass starts at UCLA.
To run locally you need to download python, pip, the with pip install selenium and requests. In addition you need to download the chrome driver found here https://sites.google.com/a/chromium.org/chromedriver/ that corresponds with your chrome version and link it. if the chrome driver is not found you will have to `chmod +x chromedriver` and then link it with  `cp -f /usr/local/bin/`
Finally replace the constants in the python file with your information. These include USERNAME, PASSWORD, and, WEBHOOK_URL. the last of which you can make here https://api.slack.com/messaging/webhooks
