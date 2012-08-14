Instructions:
#############

Client install:
---------------

    $ sqlite3 waste.db < waste.sql
    $ cp waste.ini.example waste.ini
    $ ./wasted.py 127.0.0.1

open your browser on http://127.0.0.1:8080


Server install:
---------------

Well, a client is a server, so...

but if you want it secure, do something with SSL and apache like:


    ScriptAlias /waste/ /srv/waste/wasted.py/waste/

	<Location /waste/>
		AuthType Basic
		AuthName "Waste"
		AuthUserFile /srv/waste/htpasswd
		Require valid-user
	</Location>

Then you also have to set the =path= in =waste.ini= and maybe put the database somewhere else:

    [Main]
    path = /waste

    [database]
    # currently only sqlite is supported.
    type = sqlite
    name = /var/lib/waste/waste.db
        
