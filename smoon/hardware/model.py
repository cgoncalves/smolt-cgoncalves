from datetime import datetime
from sqlalchemy import *
from turbogears.database import metadata, session
from sqlalchemy.ext.assignmapper import assign_mapper
from turbogears import identity

def assign(obj, table, *args, **kw):
    """Map tables to objects with knowledge about the session context."""
    return assign_mapper(session.context, obj, table, *args, **kw)


computer_logical_devices = Table('device', metadata, 
                                 Column("id", INT, autoincrement=True,
                                        nullable=False, primary_key=True),
                                 Column("description", VARCHAR(128),
                                        nullable=False),
                                 Column("bus", TEXT),
                                 Column("driver", TEXT),
                                 Column("class", TEXT,
                                        ForeignKey("classes.klass"),
                                        key="klass"),
                                 Column("date_added", DATETIME),
                                 Column("device_id", VARCHAR(16)),
                                 Column("vendor_id", INT),
                                 Column("subsys_device_id", INT),
                                 Column("subsys_vendor_id", INT))

host_links = Table('host_links', metadata, 
                   Column("id", INT, autoincrement=True, nullable=False, primary_key=True),
                   Column('host_link_id', INT, ForeignKey("host.id"),
                          nullable=False),
                   Column("device_id", INT, ForeignKey("device.id")),
                   Column("rating", INT))

hosts = Table('host', metadata,
              Column("id", INT, autoincrement=True, nullable=False, primary_key=True),
              Column('u_u_id', VARCHAR(36), nullable=False, unique=True),
              Column('o_s', TEXT),
              Column('platform', TEXT),
              Column('bogomips', DECIMAL),
              Column('system_memory', INT),
              Column('system_swap', INT),
              Column('vendor', TEXT),
              Column('system', TEXT),
              Column('cpu_vendor', TEXT),
              Column('cpu_model', TEXT),
              Column('num_cp_us', INT),
              Column('cpu_speed', DECIMAL),
              Column('language', TEXT),
              Column('default_runlevel', INT),
              Column('kernel_version', TEXT),
              Column('formfactor', TEXT),
              Column('last_modified', DATETIME, default=0, nullable=False),
              Column('rating', INT, nullable=False, default=0),
              Column('selinux_enabled', BOOLEAN, nullable=False),
              Column('selinux_enforce', TEXT))

fas_links = Table('fas_link', metadata,
                  Column("id", INT, autoincrement=True, nullable=False,
                         primary_key=True),
                  Column('u_u_id', VARCHAR(36), ForeignKey("host.u_u_id"),
                         nullable=False),
                  Column("user_name", VARCHAR(255), nullable=False))

hardware_classes = Table('classes', metadata,
                         Column("class", VARCHAR(24), nullable=False, primary_key=True, key="klass"),
                         Column("description", TEXT, key="class_description"))

computer_devices = join(computer_logical_devices,
                        hardware_classes,
                        computer_logical_devices.c.klass == 
                            hardware_classes.c.klass)

hardware_by_class = Table("CLASS", metadata,
                          Column('device_id', VARCHAR(16), primary_key=True),
                          Column('description', VARCHAR(128)),
                          Column('bus', TEXT),
                          Column("driver", TEXT),
                          Column("vendor_id", INT),
                          Column("subsys_vendor_id", INT),
                          Column("subsys_device_id", INT),
                          Column("date_added", DATETIME),
                          Column("cnt", INT),
                          Column("class", TEXT, key="klass"))

archs = Table("ARCH", metadata,
                  Column("platform", TEXT, primary_key=True),
                  Column("cnt", INT))
oses = Table("OS", metadata,
                  Column("o_s", TEXT, primary_key=True, key="os"),
                  Column("cnt", INT))
runlevels = Table("RUNLEVEL", metadata,
                      Column("default_runlevel", INT, primary_key=True, key="runlevel"),
                      Column("cnt", INT))
num_cpus = Table("NUM_CPUS", metadata,
                     Column("num_cp_us", INT, primary_key=True, key="num_cpus"),
                     Column("cnt", INT))
vendors = Table("VENDOR", metadata,
                    Column("vendor", TEXT, primary_key=True),
                    Column("cnt", INT))
systems = Table("SYSTEM", metadata,
                    Column("system", TEXT, primary_key=True),
                    Column("cnt", INT))
cpu_vendors = Table("CPU_VENDOR", metadata,
                    Column("cpu_vendor", TEXT, primary_key=True),
                    Column("cnt", INT))
kernel_versions = Table("KERNEL_VERSION", metadata,
                            Column("kernel_version", TEXT, primary_key=True),
                            Column("cnt", INT))
formfactors = Table("FORMFACTOR", metadata,
                         Column("formfactor", TEXT, primary_key=True),
                         Column("cnt", INT))
languages = Table("LANGUAGE", metadata,
                      Column('language', TEXT, primary_key=True),
                      Column('cnt', INT))

class Host(object):
    pass

class ComputerLogicalDevice(object):
    pass

class HostLink(object):
    def __init__(self, rating=0):
        self.rating = rating

class FasLink(object):
    def __init__(self, uuid, user_name):
        self.uuid = uuid
        self.user_name = user_name

class HardwareClass(object):
    pass

class HardwareByClass(object):
    pass

class Arch(object):
    pass
class OS(object):
    pass
class Runlevel(object):
    pass
class NumCPUs(object):
    pass
class Vendor(object):
    pass
class System(object):
    pass
class CPUVendor(object):
    pass
class KernelVersion(object):
    pass
class FormFactor(object):
    pass
class Language(object):
    pass
class Foo(object):
    pass

assign(Foo, hosts,
       properties = {'clds': relation(ComputerLogicalDevice, secondary=host_links)})

assign(Host, hosts,
       properties = {
          'uuid' : hosts.c.u_u_id,
          'os': hosts.c.o_s,
          'num_cpus': hosts.c.num_cp_us,
          '_devices': relation(HostLink,
                               cascade="all, delete-orphan",
                               backref=backref('host'),
                               lazy=None),
          'devices': relation(HostLink, cascade='all, delete-orphan'),
          'fas_account': relation(FasLink, uselist=False)})

assign(ComputerLogicalDevice,
       computer_devices,
       properties = {"_host_links": relation(HostLink,
                                            cascade="all, delete-orphan",
                                            backref=backref('device'),
                                            lazy=None),
                     "host_links": relation(HostLink,
                                            cascade="all, delete-orphan")})

assign(HostLink, host_links)

assign(FasLink, fas_links, properties = {'hosts': relation(Host),
                                         'uuid': fas_links.c.u_u_id})

assign(HardwareClass,
       hardware_classes,
       properties = {'devices': relation(ComputerLogicalDevice)})

assign(HardwareByClass, hardware_by_class)
assign(OS, oses, order_by=desc(oses.c.cnt))
assign(Arch, archs, order_by=desc(archs.c.cnt))
assign(Runlevel, runlevels, order_by=desc(runlevels.c.cnt))
assign(NumCPUs, num_cpus, order_by=desc(num_cpus.c.cnt))
assign(Vendor, vendors, order_by=desc(vendors.c.cnt))
assign(System, systems, order_by=desc(systems.c.cnt))
assign(CPUVendor, cpu_vendors, order_by=desc(cpu_vendors.c.cnt))
assign(KernelVersion, kernel_versions, order_by=desc(kernel_versions.c.cnt))
assign(FormFactor, formfactors, order_by=desc(formfactors.c.cnt))
assign(Language, languages, order_by=desc(languages.c.cnt))


