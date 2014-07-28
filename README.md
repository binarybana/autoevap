# AutoEvap

Uses the awesome InfluxDB for time series logging of temperature, thermostat activity, and sprinkler status.

Eventually this will encompass analysis routines to determine if wasting all this water has actually saved me any money! Stay tuned.

## TODO

* Cherrypy Server
  * Separate cherrypy server from control logic
  * Add in authentication and status reporting to cherrypy
* General Software
  * Run everything on boot from init scripts (man I wish I had systemd on my pi)
  * Setup DS2484 controller after module loading but before these scripts
  * Work on pulling data out in analytics to make sure I'm recording the right things
  * Check datalog summary output against these analytics
* Weather reporting (wunderground api)
