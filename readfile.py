################################ left panel ################################
sourcepath = '/mnt/IBMShare/sysmon/'
#sourcepath = 'U:\\sysmon\\'
#sourcepath = '../'

import datetime
import os
alarm = False

# filesystem stats
def diskstats():
  global alarm
  f = open(sourcepath + 'df.txt')
  line = f.readline()
  import re
  lc = 1
  head = ["Filesystem", "MB blocks",  "Free",  "%Used",  "Iused",  "%Iused",  "Mounted on"]

  body = '<table>'
  oline = ''
  for i in range(0, 4):
    oline = oline + head[i] + '</td><td>'
  body += '<tr class="headrow"><td>' + oline + head[6] + '</td></tr>'

  while line:
    line = line.strip('\n')

    line = re.split(r'\s+', line)
    diskfree = (line[3]).replace('%','')

    try:
      dfree = int(diskfree)
    except:
      dfree = 0

    if dfree <= 85:
      ins = "normalrow"
    elif dfree > 85 and dfree <=89:
      ins = "attrow"
    elif dfree > 89:
      ins = "alarmrow"
      alarm = True
    if lc > 1:
      oline = ''
      for i in range(0, 4):
        if i >= 1:
          alins = 'align="right"'
        elif i == 0:
         alins = 'align="left" class="padd"'
        oline = oline + '<td ' + alins + '>' + line[i] + '</td>'
    body += '<tr class="' + ins + '">' + oline + '<td align="left" class="padd">' + line[6] + '</td></tr>'
    lc = lc + 1
    line = f.readline()
  f.close()
  mod_date = modification_date(sourcepath + "df.txt")
  body = body + '<tr><td colspan="5"><b>moment last checked: ' + str(mod_date) + '</b></td></tr>'
  body += '</table>'
  return body

################################ right panel ################################

# printer stats
def printstats():
  global alarm
  f = open(sourcepath + 'LPQ.TXT')
  line = f.readline()
  lines = line.split('\\')
  LPStr = lines[0] + '<br>' + lines[2]
  s = lines[2]
  if s[3:5].lower() <> 'no':
    LPDown = True
  else:
    LPDown = False
  SP = int(lines[1])
  SP = int(SP)
  oline = '<span>' + LPStr + '</span>'
  if SP >= 10:
    oline = '<span class="attrow">' + LPStr + '</span>'
  if SP >= 30 or LPDown:
    oline = '<span class="errline">' + LPStr + '</span>'
    alarm = True
  return oline
  f.close()

#Scheduler Stats
def schedstat():
  global alarm
  f = open(sourcepath + 'Scheduler.txt')
  bodya = f.read()
  f.close

  f = open(sourcepath + 'Sched_Stat.txt')
  bodyb = f.read()
  f.close()
  body = bodya + bodyb + '</span><br>'
  if  'alarm' in body:
    alarm = True
  return body

#UDT log
def udterr():
  f = open(sourcepath + 'udtsum.txt')
  body = f.read()
  body = body + '<br>'
  f.close
  thisline = body[0:17] + '<br>'
  thisline = thisline + body[18:]
  return thisline

#phantom jobs
def phantom():
  global alarm
  f = open(sourcepath + 'phantom.txt')
  body = f.read()
  f.close
  if not('OK' in body):
    alarm = True
    body = '<span class="errline">' + body + '</span>'
  return body

#backup stats
def backuplog():
  f = open(sourcepath + 'backup.log')
  body = f.read()
  f.close()
  dt = datetime.datetime(2008, 3, 12)
  thisbody = body.split('\n')
  ic = 0
  for line in thisbody:
    if line[0:8] == 'Command:':
      thisdate =  thisbody[ic+1][10:16] + ' ' + thisbody[ic+1][30:34]
      thisdate = datetime.datetime.strptime(thisdate, '%b %d %Y')
      if thisdate > dt:
        dt = thisdate
    ic=ic+1
  ic = 0
  obody = ''
  for line in thisbody:
    if line[0:8] == 'Command:':
      thisdate =  thisbody[ic+1][10:16] + ' ' + thisbody[ic+1][30:34]
      thisdate = datetime.datetime.strptime(thisdate, '%b %d %Y')
      jc = ic
      if dt == thisdate:
          while thisbody[jc+1][0:8] != 'Command:' and thisbody[jc].strip():
            obody = obody + thisbody[jc] + '<br>'
            jc=jc+1
          success = obody.find('SUCCESS:')
          failure = obody.find('FAILURE:')
          warning = obody.find('WARNING:')
          if success >= 0:
            fntins = '<font color="black" style="background-color:green;color:white">'
            obody = fntins + obody + '</font>'
          if failure >= 0:
            fntins = '<font color="red">'
            obody = fntins + obody + '</font>'
          if warning >= 0:
            fntins = '<font style="background-color:#ffff00">'
            obody = fntins + obody + '</font>'
    ic=ic+1
  return obody
  
#read rsync
def readrsync():
  f = open(sourcepath + 'rsync.log')
  body = f.read()
  f.close()
  thisbody = body.split('\n')
  ic = 0
  for line in thisbody:
    if line[0:5] == "rsync":
      if thisbody[ic-1] != "*** backup Exit Code: 0":
        thisline= '<font color="red">'
        thisline = thisline + thisbody[ic]
        thisline = thisline + '</font>'
      else:
        thisline = '<font style="background-color:green;color:white">'        
        thisline = thisline + thisbody[ic]
        thisline = thisline + '</font><br>'
    ic=ic+1
  f.close()
  return thisline

#read raid_array_check.txt
def raid():
  f = open(sourcepath + 'raid_array_check.txt')
  body = f.read()
  f.close()
  return body

#read network file stats
def networkfiles():
  f = open(sourcepath + 'sysmonPC.txt')
  body = f.read()
  f.close()
  return body

#*****************************************************************************************************************************
#Get file mod datetime
def modification_date(filename):
  t = os.path.getmtime(filename)
  return datetime.datetime.fromtimestamp(t)  
  
def main():
  global alarm
  alarm  = False
  opage = '<div>'
  opage = opage + (diskstats())
  opage = opage + '</div>'
  opage = opage + '<div>'
  opage = opage + (raid())
  opage = opage + (printstats()) + '<hr>'
  opage = opage + (schedstat()) + '<hr>'
  opage = opage + (udterr()) + '<hr>'
  opage = opage + (phantom()) + '<hr>'
  opage = opage + (networkfiles()) + '<hr>'
  opage = opage + (readrsync()) + '<hr>'
  opage = opage + '</div>'
  opage = opage + '<div>'
  opage = opage + (backuplog())
  opage = opage + '</div>'
  return opage + '0xdeadbeef' + str(alarm)
