from db import db


class CustomerModel(db.Model):
    __tablename__ = 'customer'

    idcustomer = db.Column('idcustomer', db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(60))
    status = db.Column(db.String(15))
    typec = db.Column(db.String(15))
    company = db.relationship('CompanyModel', backref="customer", lazy="dynamic")

    def json(self):
        return {
            'id': self.idcustomer,
            'name': self.name,
            'email': self.email,
            'status': self.status,
            'typec': self.typec,
            'company': [c.json() for c in self.company]
        }


class CompanyModel(db.Model):
    __tablename__ = 'company'

    idcompany = db.Column('idcompany', db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    address = db.Column(db.String(250))
    rfc = db.Column(db.String(50))
    customer_idcustomer = db.Column(db.Integer, db.ForeignKey('customer.idcustomer'))
    branch = db.relationship('BranchModel', backref="company", lazy='dynamic')
    owner = db.relationship('OwnerModel', backref="company", lazy='dynamic')
    discount = db.relationship('DiscountModel', backref="company", lazy='dynamic')
    group = db.relationship('GroupModel', backref="company", lazy="dynamic")
    schedule = db.relationship('ScheduleModel', backref="company", lazy="dynamic")
    user = db.relationship('UserModel', backref="company", lazy="dynamic")

    def json(self):
        return {
            'id': self.idcompany,
            'name': self.name,
            'address': self.address,
            'rfc': self.rfc,
            'branch': [b.json() for b in self.branch]
        }


class BranchModel(db.Model):
    __tablename__ = "branch"

    idbranch = db.Column('idbranch', db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    address = db.Column(db.String(150))
    isterminal = db.Column(db.Integer)
    company_idcompany = db.Column(db.Integer, db.ForeignKey('company.idcompany'))
    origin = db.relationship('BusrouteModel', backref="branch", lazy="dynamic")

    def json(self):
        return {
            'id': self.idbranch,
            'name': self.name,
            'address': self.address,
            'isterminal': self.isterminal
        }


busroute_schedule = db.Table('busroute_schedule',
  db.Column('idbusroute_schedule', db.Integer, primary_key=True),
  db.Column('busroute_idbusroute', db.Integer, db.ForeignKey('busroute.idbusroute', onupdate="CASCADE", ondelete="RESTRICT")),
  db.Column('schedule_idschedule', db.Integer, db.ForeignKey('schedule.idschedule', onupdate="CASCADE", ondelete="RESTRICT"))
  )


class BusrouteModel(db.Model):
    __tablename__ = 'busroute'

    idbusroute = db.Column('idbusroute', db.Integer, primary_key=True)
    description = db.Column(db.String(100))
    branch_idbranch = db.Column(db.Integer, db.ForeignKey('branch.idbranch'))


class DiscountModel(db.Model):
    __tablename__ = 'discount'

    iddiscount = db.Column('iddiscount', db.Integer, primary_key=True)
    descripcion = db.Column(db.String(100))
    status = db.Column(db.String(15))
    amount = db.Column(db.Numeric(12,2))
    company_idcompany = db.Column(db.Integer, db.ForeignKey('company.idcompany'))


class OwnerModel(db.Model):
    __tablename__ = 'owner'

    idowner = db.Column('idowner', db.Integer, primary_key=True)
    fullname = db.Column(db.String(100))
    company_idcompany = db.Column(db.ForeignKey('company.idcompany'))
    bus = db.relationship('BusModel', backref="bus", lazy="dynamic")


class PriceModel(db.Model):
    __tablename__ = 'price'

    idprice = db.Column('idprice', db.Integer, primary_key=True)
    amount = db.Column(db.Numeric(12,2), server_default="0")
    # busroute_idbusroute_schedule = Column(ForeignKey('busroute_schedule.idbusroute_schedule'))
    company_idcompany = db.Column(db.Integer, db.ForeignKey('company.idcompany'))


class ScheduleModel(db.Model):
    __tablename__ = 'schedule'

    idschedule = db.Column('idschedule', db.Integer, primary_key=True)
    checkout = db.Column(db.String(20))
    company_idcompany = db.Column(db.Integer, db.ForeignKey('company.idcompany'))
    busrouteschedule = db.relationship('BusrouteModel', secondary=busroute_schedule, backref=db.backref('busroute', lazy="dynamic"))


user_group = db.Table('user_group',
  db.Column('iduser_group', db.Integer, primary_key=True),
  db.Column('user_iduser', db.Integer, db.ForeignKey('user.iduser', onupdate="CASCADE", ondelete="RESTRICT")),
  db.Column('group_idgroup', db.Integer, db.ForeignKey('group.idgroup', onupdate="CASCADE", ondelete="RESTRICT"))
  )


class UserModel(db.Model):
    __tablename__ = 'user'

    iduser =db.Column('iduser', db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    fullname = db.Column(db.String(100))
    status = db.Column(db.String(15))
    company_idcompany = db.Column(db.Integer, db.ForeignKey('company.idcompany'))
    ugroups = db.relationship('GroupModel', secondary=user_group, backref=db.backref('group', lazy='dynamic'))


class GroupModel(db.Model):
    __tablename__ = 'group'

    idgroup = db.Column('idgroup', db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.String(150))
    group_idcompany = db.Column(db.Integer, db.ForeignKey('company.idcompany'))


class BusModel(db.Model):
    __tablename__ = "bus"

    idbus = db.Column('idbus', db.Integer, primary_key=True)
    description = db.Column(db.String(150))
    carmodel = db.Column(db.String(50))
    brand = db.Column(db.String(50))
    status = db.Column(db.Integer)
    owner_idowner = db.Column(db.Integer, db.ForeignKey('owner.idowner'))

    def json(self):
        return {
            'id': self.idbus,
            'description': self.description,
            'carmodel': self.carmodel,
            'brand': self.brand,
            'status': self.status
        }


class BusticketModel(db.Model):
    __tablename__ = "busticket"

    idbusticket = db.Column('idbusticket', db.Integer, primary_key=True)
    ticketnumber = db.Column(db.String(15))
    traveldate = db.Column(db.DateTime)
    client = db.Column(db.String(50))
    # busroute_schedule_idbusroute = db.Column(db.Integer, db.ForeignKey('busroute_schedule.idbusroute_schedule'))
    # bus_idbus = db.Column(db.Integer, db.ForeignKey('bus.idbus'))
    # price_idprice = db.Column(db.Integer, db.ForeignKey('price.idprice'))
    # discount_iddiscount = db.Column(db.Integer, db.ForeignKey('discount.iddiscount'))
    # busroute_schedule = db.relationship('busroute_schedule')
