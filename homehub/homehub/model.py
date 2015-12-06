from sqlalchemy import *
from sqlalchemy.orm import relationship, backref

from homehub.meta import session
from homehub.homehub.base import Base

import datetime

class EventFamily(Base):
    __tablename__ = 'event_family'
    id			    = Column(Integer, primary_key = True)
    name            = Column(Text, nullable=False)

class EventType(Base):
    __tablename__ = 'event_type'
    id			    = Column(Integer, primary_key = True)
    name            = Column(Text, nullable=False)
    family_id       = Column(Integer, ForeignKey('event_family.id'))
    EventFamily          = relationship(EventFamily, backref='EventType',
                                   foreign_keys='event_family.id')



class Event(Base):
    __tablename__ = 'event'
    #__table_args__ =
    id			    = Column(Integer, primary_key = True)
    type            = Column(Integer, ForeignKey('event_type.id'))
    when		    = Column(DateTime(timezone=True))
    blurb           = Column(Text, nullable=True)
    EventType       = relationship(EventType, backref='Event',
                                   foreign_keys='event_type.id')




"""

    reserved_by		    = Column(Integer, ForeignKey('users_user.id'))
    held		    = Column(Boolean, default = False)
    locked		    = Column(Boolean, default = False)

    CheckConstraint('hold_reserved', 'held = true AND reserved_by IS NOT NULL OR held = false')
    CheckConstraint('locked_reserved', 'locked = true AND reserved_by IS NOT NULL OR locked = false')

    ReservedBy = relationship('User', backref='Reserved', foreign_keys='MillerRecord.reserved_by')
    # deprecated
    #LockedBy = relationship('User', backref='Locked', foreign_keys='MillerRecord.locked_by')

    # DJ field cannot be null to prevent ambiguity from whether to code an unchecked checkbox as NULL or NO



    def __init__(self):
        pass

    def __repr__(self):
        return "Row id = %d" % self.id


    @property
    def title(self):
        if self.old_title:
            return self.old_title
        else:
            c = LexSession.query(Case).get(self.lmi_case_id)
            if c is not None:
                return c.title

    @property
    def casenumber(self):
        if self.old_casenumber:
            return self.old_casenumber
        else:
            c = LexSession.query(Case).get(self.lmi_case_id)
            return c.bare_civil_action_number

    @property
    def district(self):
        return LexSession.query(Case).get(self.lmi_case_id).court.common_abbreviation

    @staticmethod
    def __codes_to_string(party_codes):
        if not party_codes:
            return ""
        else:
            codes = []
            for pc in party_codes:
                if pc.code == 0:
                    continue
                if pc.uncertain:
                    codes.append(str(pc.code)+'?')
                else:
                    codes.append(str(pc.code))

            return ', '.join(sorted(set(codes)))


    @staticmethod
    def getTotalRecords():
        return session.query(func.count(MillerRecord.id)).first()[0]


    @staticmethod
    def getNumRemaining():
        done = session.query(func.count(distinct(MillerRecord.id))) \
            .outerjoin(PartyCode, PartyCode.rid == MillerRecord.id) \
            .filter( \
                or_( \
                    MillerRecord.code != None,  \
                    and_(MillerRecord.code == None, PartyCode.code != None) \
                    ) \
                ) \
            .first()[0]
        return MillerRecord.getTotalRecords() - done

    # RECORD SELECTION METHOD
    @staticmethod
    def getNextRecord():
        rec = session.query(MillerRecord) \
            .outerjoin(PartyCode, PartyCode.rid == MillerRecord.id) \
            .filter(MillerRecord.reserved_by==current_user.id) \
            .filter(MillerRecord.held != True) \
            .first()
        return rec


    '''
	# TODO: consider changing this to look for PartyCodes, not Audits....
    # failed, but possibly useful, code:
    #.outerjoin(MillerAudit.rid) \
    #.exists().where(MillerAudit.rid == MillerRecord.id)

    select miller_npe.id from miller_npe
    where miller_npe.locked_by is null
    and miller_npe.code is null
    and not exists (
    select 1 from miller_audit where miller_audit.rid = miller_npe.id
    )
    '''

    @property
    def code_string(self):
        pcs = session.query(PartyCode).filter(PartyCode.rid == self.id).all()
        if pcs:
            return self.__codes_to_string(pcs)
        elif self.code:
            return self.code
        else:
            return None

    @property
    def pat_owner_string(self):
        if self.patent_owner:
            return self.patent_owner
        else:
            pcs = session.query(PartyCode) \
                .filter(PartyCode.rid == self.id) \
                .filter(PartyCode.code == 0) \
                .all()
            if pcs:
                pos = []
                for pc in pcs:
                    party_name = LexSession.query(Party).get(pc.party_id)
                    pos.append(party_name.litigating_entity.longest_raw_name)
                return ', '.join(sorted(set(pos)))

    @property
    def alleged_infr_string(self):
        if self.alleged_infringer:
            return self.alleged_infringer
        else:
            pcs = session.query(PartyCode) \
                .filter(PartyCode.rid == self.id) \
                .filter(PartyCode.code != 0, PartyCode.code != None) \
                .all()
            if pcs:
                pos = []
                for pc in pcs:
                    party_name = LexSession.query(Party).get(pc.party_id)
                    pos.append(party_name.litigating_entity.longest_raw_name)
                return ', '.join(sorted(set(pos)))



    def lock(self):
        if self.reserved_by and self.reserved_by != current_user.id:
            return False
        else:
            self.reserved_by = current_user.id
            self.locked = True
            self.held = False
            session.commit()
            return True

    def hold(self):
        if self.reserved_by and self.reserved_by != current_user.id:
            return False
        else:
            self.reserved_by = current_user.id
            self.held = True
            session.commit()
            return True


    def reserve(self):
        if self.reserved_by and self.reserved_by != current_user.id:
            return False
        else:
            self.reserved_by = current_user.id
            session.commit()
            return True

    # record all audit info on unlock
    def release(self, cancel=False):
        if not self.reserved_by and self.reserved_by == current_user.id:
            return False
        else:
            self.reserved_by = None
            self.locked = False
            self.held = False
            if not cancel:
                self.__addReviewer()
                ma = MillerAudit(self.id, current_user.id)
                session.add(ma)
            session.commit()
            return True





    def __addReviewer(self):
        reviewers = [x.strip() for x in self.who.split(',')] if self.who else []
        if current_user.initials not in reviewers:
            reviewers.append(current_user.initials)
        self.who = ','.join(reviewers)
        #session.commit()  -- no commit




class MillerAudit(Base):
    __tablename__ = 'miller_audit'
    #__table_args__ = {'autoload':True }

    id			    = Column(Integer, primary_key = True)
    rid			    = Column(Integer, ForeignKey('miller_npe.id'), nullable = False)
    uid			    = Column(Integer, ForeignKey('users_user.id'))
    edit_date		    = Column(DateTime(timezone=False))

    User = relationship('User', backref='Audits')
    Record = relationship('MillerRecord', backref='Audits')



    def __init__(self, rid, uid):
        self.rid = rid
        self.uid = uid
        self.edit_date = datetime.datetime.now()

    def __repr__(self):
        #return "<Edit made to record %d by user %s at %s>"  % (self.id, self.uid, self.edit_date)
        return "<Edit made to record %d by user %s at %s>"  % (self.id, self.User.name, self.edit_date)

class PartyCode(Base):
    __tablename__ = 'miller_lit_ent'
    #__table_args__ = {'autoload':True }
    rid			    = Column(Integer, ForeignKey('miller_npe.id'), nullable=False,  primary_key = True)
    party_id		    = Column(Integer, nullable = False, primary_key = True)
    uncertain		    = Column(Boolean, nullable = False)
    code		    = Column(Integer, nullable = False)


    Record = relationship('MillerRecord', backref='PartyCodes')

    def __init__(self, rid, party_id, code, uncertain=False):
        self.rid = rid
        self.party_id = party_id
        self.uncertain = uncertain
        self.code = code

    def __repr__(self):
        #return "<Edit made to record %d by user %s at %s>"  % (self.id, self.uid, self.edit_date)
        return "<id %d Record %d party %d code %d uncertain? %s>"  % (self.id, self.rid, self.party_id, self.code, \
                                                                      self.uncertain)

"""
