# Legal stuff, credits, info

# Imports
import platform
import sqlite3

from Cookie import Cookie

# Functions
def grabJar(path):
  jar=sqlite3.connect(path)
  jar.execute('''CREATE TABLE IF NOT EXISTS CookieJar
                 (ID            INTEGER  PRIMARY KEY AUTOINCREMENT,
                  Domain        TEXT            NOT NULL,
                  Host          Text            Not Null,
                  Name          TEXT            NOT NULL,
                  Value         TEXT            NOT NULL,
                  LastUsed      INTEGER,
                  CreationTime  INTEGER,
                  TimeJarred    INTEGER         NOT NULL,
                  Notes         TEXT,
                  Browser       TEXT            NOT NULL,
                  User          TEXT);''')
  jar.close()

def addToJar(path, cookies):
  if type(cookies)!=list:
    cookies=[cookies]
  grabJar(path)
  jar=sqlite3.connect(path)
  cs=selectAllFrom(path, "CookieJar")
  added=0
  for c in cookies:
    if not any(d['domain']==c.domain and d['name']==c.name and d['value']==c.value and d['browser']==c.browser
                     and d['user']==c.user for d in cs):
      jar.execute('''INSERT INTO CookieJar
                    (Domain, Host,  Name, Value, LastUsed, CreationTime, TimeJarred, Notes, browser, user )
                     VALUES(:dom,:host,:name,:val, :lu, :ct, :tj, :notes, :browser, :user)''',
                     {'dom':c.domain,     'host': c.host,     'name': c.name,  'val':    c.value,   'lu':  c.lastUsed,
                      'ct':c.creationTime,'tj': c.timeJarred, 'notes':c.notes, 'browser':c.browser, 'user':c.user})
      added+=1
  jar.commit()
  jar.close()
  return added

def selectAllFrom(path, table, where=None):
  conn=sqlite3.connect(path)
  curs=conn.cursor()
  wh="where "+" and ".join(where) if where else ""
  data=list(curs.execute("SELECT * FROM %s %s"%(table,wh)))
  dataArray=[]
  names = list(map(lambda x: x[0], curs.description))
  for d in data:
    j={}
    for i in range(0,len(names)):
      j[names[i].lower()]=d[i]
    dataArray.append(j)
  conn.close()
  return dataArray

