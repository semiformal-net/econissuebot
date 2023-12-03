A simple API that returns the current economist issue number (eg, 9346)

# The rss feed

I used Proquest to generate an rss feed for new entries to the economist,

1. Visit the [economist page on proquest](https://www.proquest.com/publication/41716/citation/90145D7431246D5PQ/1)

2. Click _RSS feed_

# gcp

This runs in app engine. The rss feed is entered as a secret.

1. Make a GCP project

2. Add a secret called `feed` containing the url from above

3. Grant the [right permissions](https://tsmx.net/integrating-gcp-secret-manager-with-app-engine-environment-variables/#Granting_Secret_Manager_rights_to_the_GAE_service_account)

4. update the `PROJECT_ID` in `app.yml` (it should be a big number 211821181654). you double check, click the dots beside the secret in secret manager and click _copy resource name_
