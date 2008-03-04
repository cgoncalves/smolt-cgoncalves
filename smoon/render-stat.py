#!/usr/bin/python
__requires__ = "Turbogears[future]"
import pkg_resources
pkg_resources.require("TurboGears")

from turbogears.view import engines
import turbogears.view
import turbogears.util as tg_util
from turbogears import view, database, errorhandling, config
from itertools import izip
from inspect import isclass
from turbogears import update_config, start_server
import cherrypy
cherrypy.lowercase_api = True
from os.path import *
import sys
import time
from hardware.wiki import *
from turboflot import TurboFlot

# first look on the command line for a desired config file,
# if it's not on the command line, then
# look for setup.py in this directory. If it's not there, this script is
# probably installed
if len(sys.argv) > 1:
    update_config(configfile=sys.argv[1], 
        modulename="hardware.config")
elif exists(join(dirname(__file__), "setup.py")):
    update_config(configfile="dev.cfg",modulename="hardware.config")
else:
    update_config(configfile="prod.cfg",modulename="hardware.config")

from sqlalchemy import *

from hardware.model import *
from hardware.hwdata import DeviceMap

#bind = metadata.bind
from turbogears.widgets import Tabber
tabs = Tabber()

# the path, where to store the generated pages
page_path = "hardware/static/stats"

engine = engines.get('genshi', None)
turbogears.view.load_engines()

def _process_output(output, template, format):
    """Produces final output form from the data returned from a
    controller method.

    @param tg_format: format of desired output (html or json)
    @param output: the output returned by the controller
    @param template: HTML template to use
    """
    if isinstance(output, dict):
        from turbogears.widgets import js_location

        css = tg_util.setlike()
        js = dict(izip(js_location, iter(tg_util.setlike, None)))
        include_widgets = {}
        include_widgets_lst = config.get("tg.include_widgets", [])

        if config.get("tg.mochikit_all", False):
            include_widgets_lst.insert(0, 'turbogears.mochikit')
            
        for i in include_widgets_lst:
            widget = tg_util.load_class(i)  
            if isclass(widget):
                widget = widget()
            include_widgets["tg_%s" % i.split(".")[-1]] = widget
            for script in widget.retrieve_javascript():
                if hasattr(script, "location"):
                    js[script.location].add(script)
                else:
                    js[js_location.head].add(script)
            css.add_all(widget.retrieve_css())

        for value in output.itervalues():
            if hasattr(value, "retrieve_css"):
                retrieve = getattr(value, "retrieve_css")
                if callable(retrieve):
                    css.add_all(value.retrieve_css())
            if hasattr(value, "retrieve_javascript"):
                retrieve = getattr(value, "retrieve_javascript")
                if callable(retrieve):
                    for script in value.retrieve_javascript():
                        if hasattr(script, "location"):
                            js[script.location].add(script)
                        else:
                            js[js_location.head].add(script)
        output.update(include_widgets)
        output["tg_css"] = css
        #output.update([("tg_js_%s" % str(l), js[l]) for l in js_location])
        for l in iter(js_location):
            output["tg_js_%s" % str(l)] = js[l]

        output["tg_flash"] = output.get("tg_flash")

        return engine.render(output, format=format, template=template)



stats = {}
# somehow this has to be first, cause it binds us to
# an sqlalchemy context
stats['total_hosts'] = session.query(Host).count()

class ByClass(object):
    def __init__(self):
        self.data = {}

    def fetch_data(self):
        classes = session.query(HardwareClass).select()
        count = {}
        types = {}
        vendors = {}
        total_hosts = 0
        
        # We only want hosts that detected hardware (IE, hal was working properly)
        total_hosts = select([func.count(func.distinct(host_links.c.host_link_id))],
                             hosts.c.id == host_links.c.host_link_id)\
                        .execute().fetchone()[0]

        for cls in classes:
            type = cls.cls 

            #devs = select([computer_logical_devices], computer_logical_devices.c.cls == type).alias("devs")
            devs = computer_logical_devices
            types = select([devs, 
                            func.count(func.distinct(host_links.c.host_link_id)).label('c')], 
                           and_(devs.c.cls == type, 
                                host_links.c.device_id == devs.c.id), 
                           #from_obj=[ host_links.join(devs, host_links.c.device_id == devs.c.id) ],
                           group_by=host_links.c.device_id, 
                           order_by=[desc('c')], 
                           limit=100).execute().fetchall();
	    
#            devs = select([computer_logical_devices.c.id], 
#                          and_(computer_logical_devices.c.cls == type,
#                               old_hosts_clause())).alias("devs")
#            devs = computer_logical_devices
            count = select([func.count(func.distinct(host_links.c.host_link_id))], 
                           and_(devs.c.cls == type, 
                                host_links.c.device_id == devs.c.id)).execute().fetchone()[0] 
            
            device = computer_logical_devices
            vendors = select([func.count(device.c.vendor_id).label('cnt'), 
                              device.c.vendor_id], 
                             device.c.cls==type, 
                             order_by=[desc('cnt')], 
                             group_by=device.c.vendor_id).execute().fetchall()

            self.data[type] = (total_hosts, count, types, vendors)
    
    
    def __getitem__(self, key):
        return self.data[key]

    pass


byclass_cache = ByClass()
byclass_cache.fetch_data()

for type in byclass_cache.data.keys():
    type=type
    pci_vendors = DeviceMap('pci')
    (total_hosts, count, types, vendors) = byclass_cache[type]

    engine = engines.get('genshi', None)
    t=engine.load_template('hardware.templates.deviceclass')

    out_html = _process_output(dict(types=types, type=type, 
                                    total_hosts=total_hosts, count=count, 
                                    pci_vendors=pci_vendors, vendors=vendors, 
                                    tabs=tabs), template=t, format='html')

    fname = "%s/by_class_%s.html" % (page_path, type)
    f = open(fname, "w")
    f.write(out_html)
    f.close()

# Save some memory
del byclass_cache
del out_html

stats = {}
stats['total_hosts'] = session.query(Host).count()
total_hosts = stats['total_hosts']
flot = {}
# Arch calculation
stats['archs'] = session.query(Arch).select()
archs = []
counts = []
i = 0
for arch in stats['archs']:
    archs.append([i + .5, arch.platform])
    counts.append([i, arch.cnt])
    i += 1
flot['archs'] = TurboFlot([
    {   'data' : counts,
        'bars' : { 'show' : True },
        'label' : 'Archs', }],
    {   'xaxis' : { 'ticks' : archs }, } )
stats['os'] = session.query(OS).select(limit=15)
stats['runlevel'] = session.query(Runlevel).select()
stats['num_cpus'] = session.query(NumCPUs).select()
stats['vendors'] = session.query(Vendor).select(limit=100)
stats['systems'] = session.query(System).select(limit=100)
stats['cpu_vendor'] = session.query(CPUVendor).select(limit=100)
stats['kernel_version'] = session.query(KernelVersion).select(limit=20)
stats['formfactor'] = session.query(FormFactor).select(limit=8)
stats['language'] = session.query(Language).select()
stats['selinux_enabled'] = session.query(SelinuxEnabled).select()
stats['selinux_enforce'] = session.query(SelinuxEnforced).select()
stats['selinux_policy'] = session.query(SelinuxPolicy).select()
stats['languagetot'] = stats['total_hosts']

stats['sys_mem'] = []
stats['sys_mem'].append(("less than 256mb", 
                         session.query(Host).filter(Host.c.system_memory<256).count()))
stats['sys_mem'].append(("between 256mb and 512mb", 
                         session.query(Host).filter(and_(Host.c.system_memory>=256, 
                                                 Host.c.system_memory<512)).count()))
stats['sys_mem'].append(("between 512mb and 1023mb", 
                         session.query(Host).filter(and_(Host.c.system_memory>=512, 
                                                 Host.c.system_memory<1024)).count()))
stats['sys_mem'].append(("between 1024mb and 2047mb", 
                         session.query(Host).filter(and_(Host.c.system_memory>=1024, 
                                                 Host.c.system_memory<2048)).count()))
stats['sys_mem'].append(("more than 2048mb", 
                         session.query(Host).filter(Host.c.system_memory>=2048).count()))

stats['swap_mem'] = []
stats['swap_mem'].append(("less than 512mb", 
                          session.query(Host).filter(Host.c.system_swap<512).count()))
stats['swap_mem'].append(("between 512mb and 1027mb", 
                          session.query(Host).filter(and_(Host.c.system_swap>=512, 
                                                  Host.c.system_swap<1024)).count()))
stats['swap_mem'].append(("between 1024mb and 2047mb", 
                          session.query(Host).filter(and_(Host.c.system_swap>=1024, 
                                                  Host.c.system_swap<2048)).count()))
stats['swap_mem'].append(("more than 2048mb", 
                          session.query(Host).filter(Host.c.system_swap>=2048).count()))

stats['cpu_speed'] = []
stats['cpu_speed'].append(("less than 512mhz", 
                           session.query(Host).filter(Host.c.cpu_speed<512).count()))
stats['cpu_speed'].append(("between 512mhz and 1023mhz", 
                           session.query(Host).filter(and_(Host.c.cpu_speed>=512, 
                                                   Host.c.cpu_speed<1024)).count()))
stats['cpu_speed'].append(("between 1024mhz and 2047mhz", 
                           session.query(Host).filter(and_(Host.c.cpu_speed>=1024, 
                                                   Host.c.cpu_speed<2048)).count()))
stats['cpu_speed'].append(("more than 2048mhz", 
                           session.query(Host).filter(Host.c.cpu_speed>=2048).count()))

stats['bogomips'] = []
stats['bogomips'].append(("less than 512", 
                          session.query(Host).filter(Host.c.bogomips<512).count()))
stats['bogomips'].append(("between 512 and 1023", 
                          session.query(Host).filter(and_(Host.c.bogomips>=512, 
                                                  Host.c.bogomips<1024)).count()))
stats['bogomips'].append(("between 1024 and 2047", 
                          session.query(Host).filter(and_(Host.c.bogomips>=1024, 
                                                  Host.c.bogomips<2048)).count()))
stats['bogomips'].append(("between 2048 and 4000", 
                          session.query(Host).filter(and_(Host.c.bogomips>=2048, 
                                                  Host.c.bogomips<4000)).count()))
stats['bogomips'].append(("more than 4000", 
                          session.query(Host).filter(Host.c.system_memory>=4000).count()))

stats['bogomips_total'] = session.query(Host).filter(Host.c.bogomips > 0).sum(Host.c.bogomips * Host.c.num_cpus)
stats['cpu_speed_total'] = session.query(Host).filter(Host.c.cpu_speed > 0).sum(Host.c.cpu_speed * Host.c.num_cpus)
stats['cpus_total'] = session.query(Host).sum(Host.c.num_cpus)
stats['registered_devices'] = session.query(ComputerLogicalDevice).count()

t=engine.load_template('hardware.templates.stats')
out_html=_process_output(dict(stat=stats, tabs=tabs, 
                              total_hosts=total_hosts, getOSWikiLink=getOSWikiLink, flot=flot), 
                         template=t, format='html')

fname = "%s/stats.html" % (page_path)
f = open(fname, "w")
f.write(out_html)
f.close()

# Save some memory
del out_html
del stats

devices = {}
devices['total'] = session.query(HostLink).count()
devices['count'] = session.query(ComputerLogicalDevice).count()
devices['total_hosts'] = session.query(Host).count()
devices['totalList'] = session.query(TotalList).select(limit=100)
devices['uniqueList'] = session.query(UniqueList).select(limit=100)
devices['classes'] = session.query(HardwareClass).select()


t=engine.load_template('hardware.templates.devices')

out_html = _process_output(dict(devices=devices, tabs=tabs, 
                                total_hosts=total_hosts), 
                           template=t, format='html')
fname = "%s/devices.html" % (page_path)
f = open(fname, "w")
f.write(out_html)
f.close()

# Save some memory
del devices
del out_html
