import os
import sys
import psycopg2.extras
import configparser

def get_cog_infos():
    """
    Reads the cog_config_file (.cog/config in the application repository)
    and returns the config_file_name and repos path.
    Exists with an error message if no config file is found.
    """
    cog_path = None
    while os.path.realpath('.') != '/':
#        print(os.path.realpath('.'), os.path.exists('.cog/config'))
        if os.path.exists('.cog/config'):
            config = configparser.ConfigParser()
            config.read_file(open('.cog/config'))
            db_name = config.get('core', 'database')
            cog_path = os.path.realpath('.')
            return cog_path, db_name
        os.chdir('..')
    raise RuntimeError("no collorg repository found here\n")

def connect(
    dbname, user = 'collorg', password = '', host = 'localhost', port = '5432'):
    password = password and "password=%s" % (password.replace("'", "\'")) or ""
    dsn = "dbname=%s user=%s host=%s port=%s %s" % (
        dbname, user, host, port, password)
    db = psycopg2.connect(dsn)
    cursor = db.cursor(cursor_factory = psycopg2.extras.DictCursor)
    return db, cursor

def cursor(db):
    return db.cursor(cursor_factory = psycopg2.extras.DictCursor)

def ini_connect(config_file_name):
    name = config_file_name
    config_file = '/etc/collorg/%s' % (config_file_name)
    params = {}
    #!! sslmod = '', async = '', NOT USED
    try:
        assert os.path.exists(config_file)
    except:
        sys.stderr.write("config file '%s' not found!\n" % (config_file))
        raise RuntimeError("Config file '%s' not found" % config_file)
    config = configparser.ConfigParser()
    config.read_file(open(config_file))
    password = config.get('database', 'password')
    user = config.get('database', 'user')
    port = config.get('database', 'port')
    host = config.get('database', 'host')
    params['user'] = user
    params['password'] = password
    params['port'] = port
    params['host'] = host
    params['name'] = name
    params['debug'] = config.get('application', 'debug', fallback = False)
    params['icon'] = config.get(
        'application', 'icon', fallback = '/collorg/images/collorg.ico')
    params['url'] = config.get('application', 'url')
    params['url_scheme'] = config.get('application', 'url_scheme')
    params['charset'] = config.get(
        'application', 'charset', fallback = 'utf-8')
    params['upload_dir'] = config.get(
        'application', 'uplodad_dir',
        fallback = '/var/collorg/%s' % (config_file_name))
    params['application_basedir'] = config.get(
        'application', 'basedir', fallback = '/usr/share/collorg')
    params['templates_path'] = config.get(
        'application', 'templates_path',
        fallback = '%s/www/templates' % params['application_basedir'])
    params['document_root'] = config.get(
        'application', 'document_root',
        fallback = '/var/www/%s/' % (config_file_name))
    params['uploader'] = config.get(
        'application', 'uploader', fallback = '/collorg_uploader')
    params['download_prefix'] = config.get(
        'application', 'download_prefix', fallback = '/download')
    params['user_photo_url'] = config.get(
        'application', 'user_photo_url', fallback = "")
    params['site_title'] = config.get(
        'application', 'site_title',
        fallback = '<span class="grey">C</span>oll<span class="grey">o</span>rg')
    params['session_cache_host'] = config.get(
        'application', 'session_cache_host')
    params['session_cache_port'] = config.get(
        'application', 'session_cache_port')
    params['session_cache_buff_size'] = config.get(
        'application', 'session_cache_buff_size', fallback = 4096)
    params['smtp_server'] = config.get(
        'mail', 'smtp_server', fallback = None)
    params['mail_prefix'] = config.get(
        'mail', 'mail_prefix', fallback = '[collorg]')
    params['error_report_to'] = config.get('mail', 'error_report_to')
    db, cursor = connect(name, user, password, host, port)
    return name, db, cursor, params
