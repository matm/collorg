#-*- coding: UTF-8 -*-

from collorg.db.application.communication.ticket import Ticket
from collorg.utils.mail import Mail

class Error(Ticket):
    #>>> AUTO_COG REL_PART. DO NOT EDIT!
    _cog_schemaname = 'collorg.application.communication'
    _cog_tablename = 'error'
    _cog_templates_loaded = False

    from .cog import relational as cog_r
    # REVERSE
    _rev_error_traceback_ = cog_r._rev_error_traceback_
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
        * title_ : string, inherited, PK, not null
        * introductory_paragraph_ : string, inherited
        * text_ : wiki, inherited, not null
        * author_ : c_oid, inherited, not null
        * public_ : bool, inherited
        * comment_ : bool, inherited
        * expiry_date_ : timestamp, inherited
        * important_ : bool, inherited
        * broadcast_ : bool, inherited
        * visibility_ : string, inherited, not null
        * kind_ : ticket_kind, inherited
        * priority_ : ticket_priority, inherited
        * status_ : ticket_status, inherited
        * hit_ : int4
        """
        #<<< AUTO_COG DOC. Your code goes after
        super(Error, self).__init__(db, **kwargs)

    def set_mail_subject(self, mail):
        mail.set_subject(unicode("[collorg error]{} {}".format(
            self.db._cog_params['mail_prefix'],
            self.title_.value), 'utf-8') or "")

    def mail(self):
        exp = self.db._cog_params['error_report_to']
        recipient = [exp]
        if self._cog_controller.user is not None:
            exp = self._cog_controller.user.email_.value
        mail = Mail(self.db)
        mail.set_from(exp)
        mail.set_to(recipient)
        self.set_mail_subject(mail)
        self.set_mail_body(mail)
        mail.send()

    def hit(self, fqtn, method, traceback):
        self.title_.value = "{}->{}: {}".format(
            fqtn, method, traceback.splitlines()[-1])
        self.text_.value = "-"
        author = self.db.table("collorg.actor.user")
        author.email_.value = self.db._cog_params['error_report_to']
        self._author_ = author
        if not self.exists():
            self.insert()
            error_traceback = self._rev_error_traceback_
            error_traceback.hit(traceback)
            error = self.get()
            error.text_.value = traceback
            error.mail()
        else:
            error_traceback = self._rev_error_traceback_
            error_traceback.hit(traceback)
            nself = self()
            nself.hit_.value = self.get().hit_.value + 1
            self.update(nself)
