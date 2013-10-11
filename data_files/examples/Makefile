APPNAME=__DB_NAME__
DIRS=collorg_app/$(APPNAME) sql scripts

install:
	sudo python setup.py -q install
	sudo apache2ctl -k restart

clean_all: clean clean_install

clean: clean_templates
	sudo rm -rf build/ dist/ *.egg-info/
	#find collorg_app/$(APPNAME)/_cog_web_site -name w3display.py -exec rm -f {} \;
	find $(DIRS) -name "*.orig" -exec rm -f {} \;
	find $(DIRS) -name "*.pyc" -exec rm -f {} \;
	find $(DIRS) -name "*~" -exec rm -f {} \;
	for i in `find $(DIRS) -name __pycache__` ; do rmdir $$i ; done

clean_templates:
	for i in `find collorg_app/$(APPNAME)/db -name "*.py" | grep /cog/templates/ | grep -v __init__.py`; do rm $$i ; done
	for i in `find collorg_app/$(APPNAME)/db -name "__init__.py" | grep /cog/templates/`; do rm $$i ; touch $$i ; done

clean_install:
	sudo rm -rf /usr/local/lib/python?.?/dist-packages/$(APPNAME)
	sudo rm -rf /usr/local/lib/python?.?/dist-packages/collorg_app/$(APPNAME)*

restart:
	sudo apache2ctl -k restart
