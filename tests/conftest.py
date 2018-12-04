import docker
import ldap
import psycopg2
import pytest
import time 

@pytest.fixture
def some_data():
  return 42

@pytest.fixture
def postgres():
  client = docker.from_env()
  container = client.containers.run('postgres', ports={'5432/tcp': 5432}, name='some-postgres', environment={ 'POSTGRES_PASSWORD': 'mysecretpassword'}, detach=True)
  time.sleep(2)
  yield
  container.kill()
  container.remove()

@pytest.fixture
def db_conn(postgres):
  conn = psycopg2.connect(host='127.0.0.1',database='postgres',user='postgres',password='mysecretpassword')
  return conn

@pytest.fixture
def slapd(scope='session'):
  ports = {
	'389': 389,
	'636': 636
  }
  client = docker.from_env()
  container = client.containers.run('aurora/slapd', name='slapd', ports=ports, detach=True)
  time.sleep(1)
  yield
  container.kill()
  container.remove()

@pytest.fixture
def ldap_conn(slapd):
  con = ldap.initialize('ldap://127.0.0.1')
  con.simple_bind_s("cn=admin,dc=openforce,dc=org", "Secret007!")
  yield con
  con.unbind_s()

@pytest.fixture
def active_directory(tmpdir):
  environment = {
	'SAMBA_DOMAIN': 'openforce',
	'SAMBA_HOST_NAME': 'dc',
	'SAMBA_ADMINPASS': 'Abc123!',
	'SAMBA_KRBTGTPASS': 'Abc123!',
	'SAMBA_REALM': 'OPENFORCE.ORG',
  }
  ports = {
	'22': 2222,
	'53': 5353,
	'88': 88,
	'135': 135,
	'139': 139,
	'389': 389,
	'445': 445,
	'464': 464,
	'636': 636,
	'1024': 1024,
	'3268': 3268,
	'3269': 3269
  }
  client = docker.from_env()
  container = client.containers.run('xnandersson/samba-ad-dc', command='dcpromo', privileged=True, ports=ports, name='dc', environment=environment, detach=True)
  time.sleep(5)
  yield
  container.kill()
  container.remove()
