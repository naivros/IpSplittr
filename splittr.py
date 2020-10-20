import ipaddress
import sys

axiomCount = int(sys.argv[1])

map = {} # int --> array

file = open('tmp', 'r')
line = file.readlines()

isPrivate = 0
totalIP = 0

for iprange in line:
  #Clean
  iprange = iprange.replace("\n", "")
  iprange = iprange.replace(" ", "")

  if (iprange != ""):

    subnet=list(ipaddress.ip_network(iprange, False).hosts())
    ipCount = len(subnet)
    if ipCount == 0:
        ipCount = 1
    if(ipCount in map):
      map[ipCount].append(iprange)
    else:
      map[ipCount] = [iprange]

    for ip in subnet:
      totalIP += 1
      if(ip.is_private):
        isPrivate += 1

print("*"*72)
print("**** Total IPs: ", totalIP)
print("**** Private IPs: ", isPrivate)
print("*"*72)

for a in sorted(map.keys(), reverse=True):
  print("* ::", len(map[a]), "Subnet ::", a,"IPs Per Subnet ::", a*len(map[a]), "Total IPs", "::")
print("*"*72)

lists = {} # map(integer) => array of IPRanges
for i in range(1, axiomCount+1):
  goal = totalIP // axiomCount + 1
  current = 0
  #print("Target", goal)
  for key in sorted(map.keys(),reverse=True):
    while key + current < goal and len(map[key]) > 0:
      cache = map[key]
      if not i in lists:
        lists[i] = [cache[0]]
      else:
        lists[i].append(cache[0])
      cache.pop(0)
      map[key] = cache
      current += key
      #print(current)

## ROUND ROBIN DISTRIBUTION
for key in sorted(map.keys(), reverse=True):
  while len(map[key]) > 0:
    if(i>axiomCount):
      i=1
    cache = map[key]
    lists[i].append(cache[0])
    cache.pop(0)

    map[key] = cache
    current += key
    i = i + 1
#At the end of this every map[key] == []

## // TESTCASE- TEST COUNTING DIVIDED IPS TO ENSURE THAT THEY'RE EQUALLY DISTRIBUTED
def test(lists):
  for key in sorted(lists.keys()):
    count = 0
    for iprange in (lists[key]):
      x=list(ipaddress.ip_network(iprange, False).hosts())
      count = count + len(x) + 1
    print("* ::", key, "::",count, "ips ::")
  print("*"*72)
## DoTest
test(lists)

def saveToFiles(lists):
    for key in lists.keys():
        file = open("./output/output-" + str(key), "w");
        for range in lists[key]:
            file.write(range + "\n")
saveToFiles(lists)
