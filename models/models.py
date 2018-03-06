# coding: utf-8
from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


# class Branch(Base):
#     __tablename__ = 'branch'
#
#     idbranch = Column(Integer, primary_key=True, server_default=text("nextval('branch_idbranch_seq'::regclass)"))
#     name = Column(String)
#     address = Column(String)
#     isterminal = Column(String)
#     company_idcompany = Column(ForeignKey('company.idcompany'))
#
#     company = relationship('Company')


# class Bu(Base):
#     __tablename__ = 'bus'
#
#     idbus = Column(Integer, primary_key=True, server_default=text("nextval('bus_idbus_seq'::regclass)"))
#     description = Column(String)
#     model = Column(String)
#     brand = Column(String)
#     status = Column(String)
#     owner_idowner = Column(ForeignKey('owner.idowner'))
#     company_idcompany = Column(ForeignKey('company.idcompany'))
#
#     company = relationship('Company')
#     owner = relationship('Owner')


class Busroute(Base):
    __tablename__ = 'busroute'

    idbusroute = Column(Integer, primary_key=True, server_default=text("nextval('busroute_idbusroute_seq'::regclass)"))
    description = Column(String)
    branch_idbranch_origin = Column(ForeignKey('branch.idbranch'))
    branch_idbranch_dest = Column(ForeignKey('branch.idbranch'))
    company_idcompany = Column(ForeignKey('company.idcompany'), nullable=False, server_default=text("nextval('busroute_company_idcompany_seq'::regclass)"))

    branch = relationship('Branch', primaryjoin='Busroute.branch_idbranch_dest == Branch.idbranch')
    branch1 = relationship('Branch', primaryjoin='Busroute.branch_idbranch_origin == Branch.idbranch')
    company = relationship('Company')


class BusrouteSchedule(Base):
    __tablename__ = 'busroute_schedule'

    idbusroute_schedule = Column(Integer, primary_key=True, server_default=text("nextval('busroute_schedule_idbusroute_schedule_seq'::regclass)"))
    schedule_idschedule = Column(ForeignKey('schedule.idschedule'))
    busroute_idbusroute = Column(ForeignKey('busroute.idbusroute'))
    company_idcompany = Column(ForeignKey('company.idcompany'))

    busroute = relationship('Busroute')
    company = relationship('Company')
    schedule = relationship('Schedule')


class Busticket(Base):
    __tablename__ = 'busticket'

    idbusticket = Column(Integer, primary_key=True, server_default=text("nextval('busticket_idbusticket_seq'::regclass)"))
    ticketnumber = Column(String)
    traveldate = Column(DateTime(True))
    client = Column(String)
    company_idcompany = Column(ForeignKey('company.idcompany'))
    busroute_schedule_idbusroute = Column(ForeignKey('busroute_schedule.idbusroute_schedule'))
    bus_idbus = Column(ForeignKey('bus.idbus'))
    price_idprice = Column(ForeignKey('price.idprice'))
    discount_iddiscount = Column(ForeignKey('discount.iddiscount'))

    bu = relationship('Bu')
    busroute_schedule = relationship('BusrouteSchedule')
    company = relationship('Company')
    discount = relationship('Discount')
    price = relationship('Price')


# class Company(Base):
#     __tablename__ = 'company'
#
#     idcompany = Column(Integer, primary_key=True, server_default=text("nextval('company_idcompany_seq'::regclass)"))
#     name = Column(String)
#     address = Column(String)
#     rfc = Column(String)
#     customer_idcustomer = Column(ForeignKey('customer.idcustomer'))
#
#     customer = relationship('Customer')


# class Customer(Base):
#     __tablename__ = 'customer'
#
#     idcustomer = Column(Integer, primary_key=True, server_default=text("nextval('customer_idcustomer_seq'::regclass)"))
#     name = Column(String)
#     email = Column(String)
#     status = Column(String)
#     type = Column(String)


# class Discount(Base):
#     __tablename__ = 'discount'
#
#     iddiscount = Column(Integer, primary_key=True, server_default=text("nextval('discount_iddiscount_seq'::regclass)"))
#     descripcion = Column(String)
#     status = Column(String)
#     amount = Column(Numeric)
#     company_idcompany = Column(ForeignKey('company.idcompany'))
#
#     company = relationship('Company')


# class Group(Base):
#     __tablename__ = 'group'
#
#     idgroup = Column(Integer, primary_key=True, server_default=text("nextval('group_idgroup_seq'::regclass)"))
#     name = Column(String)
#     description = Column(String)
#     group_idcompany = Column(ForeignKey('company.idcompany'))
#
#     company = relationship('Company')


# class Owner(Base):
#     __tablename__ = 'owner'
#
#     idowner = Column(Integer, primary_key=True, server_default=text("nextval('owner_idowner_seq'::regclass)"))
#     fullname = Column(String)
#     company_idcompany = Column(Integer)


# class Price(Base):
#     __tablename__ = 'price'
#
#     idprice = Column(Integer, primary_key=True, server_default=text("nextval('price_idprice_seq'::regclass)"))
#     amount = Column(Numeric, server_default=text("0"))
#     busroute_idbusroute_schedule = Column(ForeignKey('busroute_schedule.idbusroute_schedule'))
#     company_idcompany = Column(ForeignKey('company.idcompany'))
#
#     busroute_schedule = relationship('BusrouteSchedule')
#     company = relationship('Company')


# class Schedule(Base):
#     __tablename__ = 'schedule'
#
#     idschedule = Column(Integer, primary_key=True, server_default=text("nextval('schedule_idschedule_seq'::regclass)"))
#     checkout = Column(String)
#     company_idcompany = Column(ForeignKey('company.idcompany'))
#
#     company = relationship('Company')


# class User(Base):
#     __tablename__ = 'user'
#
#     iduser = Column(Integer, primary_key=True, server_default=text("nextval('user_iduser_seq'::regclass)"))
#     username = Column(String)
#     fullname = Column(String)
#     status = Column(String)
#     company_idcompany = Column(ForeignKey('company.idcompany'))
#
#     company = relationship('Company')


class UserGroup(Base):
    __tablename__ = 'user_group'

    iduser_group = Column(Integer, primary_key=True, server_default=text("nextval('user_group_iduser_group_seq'::regclass)"))
    group_idgroup = Column(ForeignKey('group.idgroup'))
    user_iduser = Column(ForeignKey('user.iduser'))
    company_idcompany = Column(ForeignKey('company.idcompany'))

    company = relationship('Company')
    group = relationship('Group')
    user = relationship('User')
