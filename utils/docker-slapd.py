#!/usr/bin/env python
import docker
import os

BUILD_DIR = '/tmp/build_dir_slapd/'
SLAPD_PASSWORD = 'Secret007!'
SLAPD_DOMAIN = 'openforce.org'
SLAPD_ORGANIZATION = 'Openforce AB'

def mkdir_build_dir():
  try:
    os.mkdir(BUILD_DIR)
  except FileExistsError as e:
    pass 

def create_slapd_debconf():
  with open(os.path.join(BUILD_DIR, 'slapd.debconf'), 'w') as f:
    f.write("""slapd slapd/password1\tstring\t{slapd_password}
slapd slapd/password2\tstring\t{slapd_password}
slapd slapd/domain\tstring\t{slapd_domain}
slapd slapd/allow_ldap_v2\tboolean\ttrue
slapd shared/organization\tstring\t{slapd_organization}
slapd slapd/no_configuration\tboolean\tfalse
slapd slapd/move_old_database\tboolean\ttrue
slapd slapd/backend\tselect\tHDB
""".format(slapd_password=SLAPD_PASSWORD, slapd_domain=SLAPD_DOMAIN, slapd_organization=SLAPD_ORGANIZATION))

def create_base_ldif():
  with open(os.path.join(BUILD_DIR, 'base.ldif'), 'w') as f:
    f.write("""#Subtree for users
# Subtree for users
		dn: ou=Users,dc=openforce,dc=org
		ou: Users
		description: Openforce.org Users
		objectClass: organizationalUnit

# Subtree for groups
		dn: ou=Groups,dc=openforce,dc=org
		ou: Groups
		description: Openforce.org Groups
		objectClass: organizationalUnit

# Subtree for groups
		dn: ou=SUDOers,dc=openforce,dc=org
		ou: SUDOers 
		description: SUDO Policy
		objectClass: organizationalUnit

# Subtree for system accounts
		dn: ou=System,dc=openforce,dc=org
	ou: System
	description: Special accounts used by software applications.
	objectClass: organizationalUnit

##
## USERS
##

# Niklas Andersson
	dn: uid=nandersson,ou=Users,dc=openforce,dc=org
	ou: Users
# Name info
	uid: nandersson
	cn: Niklas Andersson
	sn: Andersson
	givenName: Niklas
	displayName: Niklas Andersson
# Work info
	title: Consultant
	description: Consultant Open Source Software
	mail: nandersson@openforce.se
	mail: nandersson@openforce.org
	telephoneNumber: +34 651 757 188
	userPassword: secret
# Object Classes:
	objectClass: person
	objectClass: organizationalPerson
	objectClass: inetOrgPerson
""")

  
def create_ldap_conf():
  with open(os.path.join(BUILD_DIR, 'ldap.conf'), 'w') as f:
    f.write("""BASE\tdc=openforce,dc=org
BINDDN\tcn=admin,dc=openforce,dc=org
URI\tldap://127.0.0.1
""")

def create_sudo_schema_ldif():
  with open(os.path.join(BUILD_DIR, 'cn={0}sudo.ldif'), 'w') as f:
    f.write("""# AUTO-GENERATED FILE - DO NOT EDIT!! Use ldapmodify.
# CRC32 a96f36e6
#dn: cn={0}sudo
dn: cn=sudo,cn=schema,cn=config
objectClass: olcSchemaConfig
#cn: {0}sudo
cn: sudo
olcAttributeTypes: {0}( 1.3.6.1.4.1.15953.9.1.1 NAME 'sudoUser' DESC 'User(s) 
 who may  run sudo' EQUALITY caseExactIA5Match SUBSTR caseExactIA5SubstringsMa
 tch SYNTAX 1.3.6.1.4.1.1466.115.121.1.26 )
olcAttributeTypes: {1}( 1.3.6.1.4.1.15953.9.1.2 NAME 'sudoHost' DESC 'Host(s) 
 who may run sudo' EQUALITY caseExactIA5Match SUBSTR caseExactIA5SubstringsMat
 ch SYNTAX 1.3.6.1.4.1.1466.115.121.1.26 )
olcAttributeTypes: {2}( 1.3.6.1.4.1.15953.9.1.3 NAME 'sudoCommand' DESC 'Comma
 nd(s) to be executed by sudo' EQUALITY caseExactIA5Match SYNTAX 1.3.6.1.4.1.1
 466.115.121.1.26 )
olcAttributeTypes: {3}( 1.3.6.1.4.1.15953.9.1.4 NAME 'sudoRunAs' DESC 'User(s)
 impersonated by sudo (deprecated)' EQUALITY caseExactIA5Match SYNTAX 1.3.6.1
 .4.1.1466.115.121.1.26 )
olcAttributeTypes: {4}( 1.3.6.1.4.1.15953.9.1.5 NAME 'sudoOption' DESC 'Option
 s(s) followed by sudo' EQUALITY caseExactIA5Match SYNTAX 1.3.6.1.4.1.1466.115
 .121.1.26 )
olcAttributeTypes: {5}( 1.3.6.1.4.1.15953.9.1.6 NAME 'sudoRunAsUser' DESC 'Use
 r(s) impersonated by sudo' EQUALITY caseExactIA5Match SYNTAX 1.3.6.1.4.1.1466
 .115.121.1.26 )
olcAttributeTypes: {6}( 1.3.6.1.4.1.15953.9.1.7 NAME 'sudoRunAsGroup' DESC 'Gr
 oup(s) impersonated by sudo' EQUALITY caseExactIA5Match SYNTAX 1.3.6.1.4.1.14
 66.115.121.1.26 )
olcAttributeTypes: {7}( 1.3.6.1.4.1.15953.9.1.8 NAME 'sudoNotBefore' DESC 'Sta
 rt of time interval for which the entry is valid' EQUALITY generalizedTimeMat
 ch ORDERING generalizedTimeOrderingMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.24
 )
olcAttributeTypes: {8}( 1.3.6.1.4.1.15953.9.1.9 NAME 'sudoNotAfter' DESC 'End 
 of time interval for which the entry is valid' EQUALITY generalizedTimeMatch 
 ORDERING generalizedTimeOrderingMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.24 )
olcAttributeTypes: {9}( 1.3.6.1.4.1.15953.9.1.10 NAME 'sudoOrder' DESC 'an int
 eger to order the sudoRole entries' EQUALITY integerMatch ORDERING integerOrd
 eringMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.27 )
olcObjectClasses: {0}( 1.3.6.1.4.1.15953.9.2.1 NAME 'sudoRole' DESC 'Sudoer En
 tries' SUP top STRUCTURAL MUST cn MAY ( sudoUser $ sudoHost $ sudoCommand $ s
 udoRunAs $ sudoRunAsUser $ sudoRunAsGroup $ sudoOption $ sudoOrder $ sudoNotB
 efore $ sudoNotAfter $ description ) )
""")

def create_nandersson_ldif():
  with open(os.path.join(BUILD_DIR, 'nandersson.ldif'), 'w') as f:
    f.write("""dn: cn=defaults,ou=SUDOers,dc=openforce,dc=org
objectClass: top
objectClass: sudoRole
cn: defaults
description: Default sudoOption's go here

dn: cn=nandersson,ou=SUDOers,dc=openforce,dc=org
objectClass: top
objectClass: sudoRole
cn: nandersson
sudoUser: nandersson
sudoHost: ALL
sudoCommand: ALL
sudoOption: !authenticate
""")

def create_dockerfile():
  with open(os.path.join(BUILD_DIR, 'Dockerfile'), 'w') as f:
    f.write("""FROM ubuntu:latest
ENV REFRESHED_AT 2018-10-02
RUN apt-get update -yqq
ADD slapd.debconf /tmp/slapd.debconf
ADD base.ldif /tmp/base.ldif
ADD nandersson.ldif /tmp/nandersson.ldif
RUN debconf-set-selections /tmp/slapd.debconf
RUN apt-get install slapd ldap-utils -y
ADD cn={0}sudo.ldif /tmp/
RUN slapadd -v -F /etc/ldap/slapd.d/ -l /tmp/cn={0}sudo.ldif -b 'cn=config'
RUN slapadd -l /tmp/base.ldif
RUN slapadd -l /tmp/nandersson.ldif
RUN chown -R openldap:openldap /var/lib/ldap
RUN chmod 0600 /var/lib/ldap/*
RUN chown -R openldap:openldap /etc/ldap/slapd.d/*
ADD ldap.conf /etc/ldap/ldap.conf
CMD /usr/sbin/slapd -d 5 -h "ldap:/// ldapi:///" -g openldap -u openldap -F /etc/ldap/slapd.d
EXPOSE 389 636
""")

if __name__ == '__main__':
  mkdir_build_dir()
  create_slapd_debconf()
  create_base_ldif()
  create_nandersson_ldif()
  create_sudo_schema_ldif()
  create_ldap_conf()
  create_dockerfile()
  client = docker.DockerClient(base_url='unix://var/run/docker.sock')
  client.images.build(path=BUILD_DIR, tag='aurora/slapd', rm=True, pull=True)
