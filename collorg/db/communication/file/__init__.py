#-*- coding: utf-8 -*-

from collorg.db.core.base_table import Base_table

#import urllib
import uuid
import shutil
import chardet
import hashlib
import os

class File(Base_table):
    #>>> AUTO_COG REL_PART. DO NOT EDIT!
    _cog_schemaname = 'collorg.communication'
    _cog_tablename = 'file'
    _cog_templates_loaded = False

    from .cog import relational as cog_r
    # DIRECT
    _uploader_ = cog_r._uploader_
    # REVERSE
    _rev_attachment_ = cog_r._rev_attachment_
    _rev_user_ = cog_r._rev_user_
    #<<< AUTO_COG REL_PART. Your code goes after
    def __init__(self, db, **kwargs):
        #>>> AUTO_COG DOC. DO NOT EDIT
        """
        * _db : ref. to database. usage: self.db.table(fqtn)
        fields list:
        * cog_oid_ : c_oid, uniq, not null
        * cog_fqtn_ : c_fqtn, not null
        * cog_signature_ : text, inherited
        * cog_test_ : bool, inherited
        * cog_creat_date_ : timestamp, inherited
        * cog_modif_date_ : timestamp, inherited
        * cog_environment_ : c_oid, inherited
        * cog_state_ : text, inherited
        * uploader_ : c_oid, not null, FK
        * name_ : string, not null
        * signature_ : string, PK, not null
        * size_ : string
        * visibility_ : string
        """
        #<<< AUTO_COG DOC. Your code goes after
        self.__tmp_file_name = None
        self.__abs_name = None
        self.__storage_path = None
        super(File, self).__init__(db, **kwargs)
        self.charset = self._cog_controller._charset

    @property
    def _storage_path(self):
        if not self.__storage_path:
            self.__storage_path = '%s/uploaded_files/%s/%s' % (
                self.db._cog_params['upload_dir'],
                self.signature_.value[0:2], self.signature_.value[2:4])
        return self.__storage_path

    @property
    def _abs_path(self):
        return "%s/%s" % (self._storage_path, self.signature_)

    def __store(self):
        """
        moves from tmp dir to definitive location
        """
        if not os.path.exists(self._storage_path):
            os.makedirs(self._storage_path)
        os.rename(self.__tmp_file_name, self._abs_path)

    def __get_public_dir(self):
        base_dir = "{}download/public/{}/{}".format(
            self.db._cog_params['document_root'],
            self.cog_oid_.value[0:2], self.cog_oid_.value[2:4])
        if not os.path.exists(base_dir):
            os.makedirs(base_dir)
        return base_dir

    def __get_public_path(self):
        name = self.name_.value.decode(self.charset)
        if not type(name) is unicode:
            name = unicode(name, chardet.detect(
                name)['encoding']).decode(self.charset)
        abs_link = "%s/%s" % (self.__get_public_dir(), name)
        abs_link = abs_link.encode(self.charset)
        if not os.path.exists(abs_link):
            os.symlink(self._abs_path, abs_link)
        rel_link = "%s/public/%s/%s/%s" % (
            self.db._cog_params['download_prefix'],
            self.cog_oid_.value[0:2], self.cog_oid_.value[2:4],
            name)
        return rel_link

    def make_public_link(self):
        """
        Called if visibility is public at insertion or on modification.
        """
        self.__get_public_path()

    def remove_public_link(self):
        """
        Public link is removed if visibility is switched from public
        to protected or private... Meaning the file has been exposed.
        We should keep this information.
        """
        base_dir = self.__get_public_dir()
        name = self.name_.value.decode(self.charset)
        if not type(name) is unicode:
            name = unicode(name, chardet.detect(
                name)['encoding']).decode(self.charset)
        abs_link = "%s/%s" % (base_dir, name)
        abs_link = abs_link.encode(self.charset)
        if os.path.exists(abs_link):
            os.remove(abs_link)

    def upload(self,
               file_name, sfile_name, user, visibility = None):
        """
        reads from tmp_dir the file uploaded.
        checks if it exists (md5). if not stores it in the corresponding
        directory (/var/collorg/<dbname>/uploaded_files/md[0:1]/md[2:3]/md)
        """
        self.__tmp_file_name = '%s/tmp/%s' % (
            self.db._cog_params['upload_dir'], sfile_name)
        hash_ = hashlib.md5()
        try:
            content = open(self.__tmp_file_name).read()
            size = len(content)
            hash_.update(content)
        except:
            raise RuntimeError("no such file '%s' % (tmp_file_name)")
        digest = hash_.hexdigest()
        self.signature_.set_intention(digest)
        if self.count() == 1:
            return self.get()
        self.name_.set_intention(file_name)
        self.__store()
        self.uploader_.set_intention(user.cog_oid_)
        self.size_.set_intention(size)
        self.visibility_.set_intention(visibility)
        self.insert()
        user.grant_access(self, write = True)
        return self

    def update_visibility(self, visibility):
        assert self.count() == 1
        if self.visibility_.value == 'public':
            self.remove_public_link()
        if visibility == 'public':
            self.make_public_link()
        nself = self()
        nself.visibility_.set_intention(visibility)
        for post in self._rev_attachment_._data_:
            post._wipe_cache()
        self.update(nself)

    def __grant_public_access(self):
        link = "%s://%s%s" % (
            self._cog_controller._url_scheme,
            self._cog_controller._server_name,
            self.__get_public_path())
        return link.encode(self.charset)

    def __session_repos(self, session):
        return "/%s/download/%s" % (
            self.db._cog_params['document_root'], session)

    def remove_session_repos(self, session):
        assert session and uuid.UUID(session)
        session_repos = self.__session_repos(session)
        if os.path.exists(session_repos):
            shutil.rmtree(session_repos)

    def __grant_protected_access(self, session):
        """
        returns the href for the user connected.
        returns -1 if the file is missing.
        """
        session_repos = self.__session_repos(session)
        upload_date = self.cog_creat_date_.value
        upload_string = "%s%s%s%s%s%s" % (
            upload_date.year,
            upload_date.month,
            upload_date.day,
            upload_date.hour, upload_date.minute, upload_date.second)
        session_repos = "%s/%s" % (session_repos, upload_string)
        if not os.path.exists(session_repos):
            os.makedirs(session_repos)
        name = self.name_.value.decode(self.charset)
        if not type(name) is unicode:
            name = unicode(name, chardet.detect(
                name)['encoding']).decode(self.charset)
        abs_link = "%s/%s" % (session_repos, name)
        abs_link = abs_link.encode(self.charset)
        if not os.path.exists(self._abs_path):
            return -1
        if not os.path.exists(abs_link):
            os.symlink(self._abs_path, abs_link)
        rel_link = "%s/%s/%s/%s" % (
            self.db._cog_params['download_prefix'],
            session, upload_string, name)
#        rel_link = urllib.quote(rel_link)
        link = "%s://%s%s" % (
            self._cog_controller._url_scheme,
            self._cog_controller._server_name,
            rel_link)
        return link.encode(self.charset)

    def _grant_access(self):
        """
        construct the symbolink link for the user connected to
        access the content of the file
        """
        session = self.db._cog_controller._session
        if self.visibility_.value != 'public' and not session:
            return
        elif self.visibility_.value == 'public':
            return self.__grant_public_access()
        return self.__grant_protected_access(session)
