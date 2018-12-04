import ldap
import ldap.modlist as modlist
import pytest
import time

def test_slapd(slapd):
  con = ldap.initialize('ldap://127.0.0.1')
  con.simple_bind_s('cn=admin,dc=openforce,dc=org', 'Secret007!')
  ldap_base = 'dc=openforce,dc=org'
  query = "(uid=nandersson)"
  result = con.search_s(ldap_base, ldap.SCOPE_SUBTREE, query)
  assert result[0][1]["displayName"][0] == b"Niklas Andersson"

def test_ldap_can_fetch_user_by_uid(ldap_conn):
  ldap_base = 'dc=openforce,dc=org'
  query = "(uid=nandersson)"
  result = ldap_conn.search_s(ldap_base, ldap.SCOPE_SUBTREE, query)
  assert result[0][1]["displayName"][0] == b"Niklas Andersson"

def test_ldap_can_create_user(ldap_conn):
  dn='uid=jdoe,ou=Users,dc=openforce,dc=org'
  attrs = {
	"objectClass": [b"inetOrgPerson", b"organizationalPerson", b"person"],
	"uid": [b"jdoe"],
	"cn": ['John Doe'.encode('utf-8')],
	"sn": [b"Doe"],
	"givenName": [b"John"],
	"displayName": [b"John Doe"],
	"title": [b"Test User"],
	"description": [b"Helping to try out the new test framework."],
	"mail": [b"jdoe@openforce.org", b"jdoe@openforce.se"],
	"userPassword": [b"alsosecret"],
  }
  result = ldap_conn.add_s(dn, modlist.addModlist(attrs))
  ldap_base = 'dc=openforce,dc=org'
  query = "(uid=jdoe)"
  result = ldap_conn.search_s(ldap_base, ldap.SCOPE_SUBTREE, query)
  assert result[0][1]["displayName"][0] == b"John Doe"

def test_ldap_can_delete_user(ldap_conn):
  ldap_base = 'dc=openforce,dc=org'
  dn = 'uid=nandersson,ou=Users,dc=openforce,dc=org'
  ldap_conn.delete_s(dn)
  query = "(uid=nandersson)"
  result = ldap_conn.search_s(ldap_base, ldap.SCOPE_SUBTREE, query)
  assert result == [] 

def test_ldap_can_modify_user(ldap_conn):
  ldap_base = 'dc=openforce,dc=org'
  query = "(uid=nandersson)"
  dn = 'uid=nandersson,ou=Users,dc=openforce,dc=org'

  result = ldap_conn.search_s(ldap_base, ldap.SCOPE_SUBTREE, query)
  assert result[0][1]["telephoneNumber"][0] == b"+34 651 757 188"

  old = { 'telephoneNumber': [b'+34 651 757 188']}
  new = { 'telephoneNumber': [b'+34 651 555 555']}
  ldif = modlist.modifyModlist(old, new)
  ldap_conn.modify_s(dn, ldif)

  result = ldap_conn.search_s(ldap_base, ldap.SCOPE_SUBTREE, query)
  assert result[0][1]["telephoneNumber"][0] == b"+34 651 555 555"

@pytest.mark.skip
def test_ldap_can_fetch_and_modify_element(ldap_conn):
  assert False

@pytest.mark.skip
def test_ldap_can_create_user_with_password_and_bind(ldap_conn):
  assert False
