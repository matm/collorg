DIRS=bin collorg doc data_files test tools

install: restart_apache
	sudo python setup.py -q install
	./tools/reset_cog_db.py collorg_db
	cog make

restart_apache:
	if [ -f /etc/init.d/apache2 ]; then sudo service apache2 restart; fi

clean_all: clean clean_templates clean_install

clean: clean_share restart_apache
	sudo rm -rf build/ dist/ collorg.egg-info/ collorg/collorg.egg-info/
	find $(DIRS) -name "*.orig" -exec rm -f {} \;
	find $(DIRS) -name "*.pyc" -exec rm -f {} \;
	find collorg/db -regextype sed -regex ".*cog/templates/[a-z].*.py" -exec rm -f {} \;
	find collorg/db -regextype sed -regex ".*cog/templates/_[a-z].*.py" -exec rm -f {} \;
	find $(DIRS) -name "*~" -exec rm -f {} \;
	for i in `find $(DIRS) -name __pycache__` ; do rmdir $$i ; done

clean_templates:
	for i in `find collorg -name "*.py" | grep "/cog/templates/" | grep -v __init__.py`; do rm $$i ; done 
	for i in `find collorg -name "__init__.py" | grep "/cog/templates/"`; do rm $$i ; touch $$i ; done 

clean_install:
	sudo rm -rf /usr/local/lib/python?.?/dist-packages/collorg-*-py?.?.egg/
	sudo rm -rf build

clean_share:
	sudo rm -rf /usr/share/collorg

restart:
	sudo apache2ctl -k restart
