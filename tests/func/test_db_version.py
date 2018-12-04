def test_db_version(db_conn):
  cur = db_conn.cursor()
  cur.execute('select version()')
  db_version = cur.fetchone()
  assert db_version[0] == 'PostgreSQL 10.5 (Debian 10.5-1.pgdg90+1) on x86_64-pc-linux-gnu, compiled by gcc (Debian 6.3.0-18+deb9u1) 6.3.0 20170516, 64-bit'
