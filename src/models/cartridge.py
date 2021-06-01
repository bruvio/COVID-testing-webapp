from db import db


class CartridgeModel(db.Model):
    __tablename__ = 'cartridges'

    id = db.Column(db.Integer, primary_key=True)
    cartridgeId = db.Column(db.String(80))
    testStatus = db.Column(db.String(80))
    departmentName = db.Column(db.String(80))
    boxName = db.Column(db.String(80))
    pattern = db.Column(db.String(80))
    hospitalName = db.Column(db.String(80))
    operatorName = db.Column(db.String(80))
    organisationId = db.Column(db.String(80))
    participantId = db.Column(db.String(80))
    trustName = db.Column(db.String(80))

    submissionDateTime = db.Column(db.DateTime)
    testStartDateTime = db.Column(db.DateTime)
    lastUpdatedDateTime = db.Column(db.DateTime)



    def __init__(self, cartridgeId, departmentName, boxName,pattern,hospitalName,operatorName,organisationId,participantId,trustName,submissionDateTime,testStatus="Incomplete",testStartDateTime=None,lastUpdatedDateTime=None):
        self.cartridgeId = cartridgeId
        self.departmentName = departmentName
        self.boxName = boxName
        self.pattern = pattern
        self.hospitalName = hospitalName
        self.operatorName = operatorName
        self.organisationId = organisationId
        self.participantId = participantId
        self.trustName = trustName
        self.submissionDateTime = submissionDateTime
        self.testStatus = testStatus
        self.testStartDateTime = testStartDateTime
        self.lastUpdatedDateTime = lastUpdatedDateTime


    def json(self):
        return {'cartridgeId': self.cartridgeId, 'testStatus': self.testStatus}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
