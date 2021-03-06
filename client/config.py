
import os,re
import commands
import os_detect

SMOON_URL = "http://www.smolts.org/"
SECURE = 0


#Only a fool would edit what lays beyond here
#Are you that fool?

HW_UUID = "/etc/smolt/hw-uuid"
PUB_UUID = "/etc/smolt/pub-uuid"
#ADMIN_TOKEN = "/etc/sysconfig/smolt-token"


#These are the defaults taken from the source code.
#fs_types = get_config_attr("FS_TYPES", ["ext2", "ext3", "xfs", "reiserfs"])
#fs_mounts = get_config_attr("FS_MOUNTS", ["/", "/home", "/etc", "/var", "/boot"])
#fs_m_filter = get_config_attr("FS_M_FILTER", False)
#fs_t_filter = get_config_attr("FS_T_FILTER", False)

FS_T_FILTER=False
FS_M_FILTER=True
FS_MOUNTS=commands.getoutput('rpm -ql filesystem').split('\n')


#This will attempt to find the distro.
#Uncomment any of the OS lines below to hardcode.
OS = os_detect.get_os_info()

#For Redhat
#try:
#    OS = file('/etc/redhat-release').read().strip()
#except IOError:
#    OS = "Shadowman!"

##For SuSE
#try:
#    OS = file('/etc/SuSE-release').read().split('\n')[0].strip()
#    reOS = re.compile('\(\w*\)$')
#    OS = reOS.sub( '', OS ).strip()
#except IOError:
#    OS = "It's a Lizard man!, It changes Colours!"
#
#
#For Debian
#try:
    #this is a bit of a kludge, as /etc/debian-release is
    #somewhat incomplete in what it gives you
    #I also figure this should work better in
    #ubuntu
#    OS = file('/etc/issue.net').read().strip()
#except IOError:
#    OS = "The swirl, it's Spinning!"


##For Frugalware
#try:
#    OS = file('/etc/frugalware-release').read().strip()
#except IOError:
#    OS = "Too cheap to have a version!"
#
##For Mythvantage
#try:
#    OS = file('/etc/mythvantage-release').read().strip()
#except IOError:
#    OS = "The OS doesn't really exist but in the minds of Holywood"
#
##For Slackware
#try:
#    OS = file('/etc/slackware-version').read().strip()
#except IOError:
#    OS = "Quit slacking you kids!"
#
##For Archlinux
#try:
#    if os.path.exists('/etc/arch-release'):
#        archfile = file('/etc/issue')
#        archfile.readline()
#        archrelease = archfile.readline()
#        archrelease = archrelease.split('\\r')
#        OS = archrelease[0]
#    else:
#        OS = "It's an impossibly tall Arch!"
#except IOError:
#    OS = "It's an impossibly tall Arch!"
#
##For Crux
#try:
#    if os.path.exists('/etc/issue'):
#        cruxfile = open('/etc/issue')
#        cruxrelease = cruxfile.read().strip()
#        if cruxrelease.find("CRUX") >= 0:
#            return "CRUX"
#    else:
#        return "Chuck Norris"
#except IOError:
#    return "Chuck Norris"
#For Gentoo
#try:
#    OS = file('/etc/gentoo-release').read().strip()
#except IOError:
#    OS = "It's the fastest penguin!"


#For non RH Distros
#HW_UUID = "/etc/smolt/hw-uuid"

