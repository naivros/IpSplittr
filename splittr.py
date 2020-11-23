import ipaddress
import sys


axiomCount = int(sys.argv[2])
path = str(sys.argv[1])

file = open(path, 'r')
line = file.readlines()

isPrivate = 0
totalIP = 0
class Storage():
    def __init__(self):
        self.map = {}
        self.isPrivate = 0;
        self.totalIP = 0;
        self.axiomCount = int(axiomCount)
    def incPrivateIP(self):
        self.isPrivate = self.isPrivate + 1
    def incTotalIP(self):
        self.totalIP = self.totalIP + 1
    def processSubnets(self, iprange, subnet):
        ipCount = len(list(subnet))
        if(ipCount in self.map):
          self.map[ipCount].append(iprange)
        else:
          self.map[ipCount] = [iprange]
        for ip in subnet:
          self.totalIP += 1
          if(ip.is_private):
            self.isPrivate += 1
    def getMap(self):
        return self.map;
    def getIPCount(self):
        return self.totalIP;
    def getPrivateCount(self):
        return self.isPrivate
    def getAxiom(self):
        return self.axiomCount

Storage = Storage()

def processData(Storage):
  map = Storage.getMap()
  lists = {}

  for i in range(1, Storage.getAxiom()+1):
    goal = Storage.getIPCount() // Storage.getAxiom() + 1
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
  return lists


for iprange in line:
  #Clean Input
  iprange = iprange .replace("\n", "")
  iprange = iprange.replace(" ", "")

  if (iprange != ""):
    if int(iprange[(iprange.find("/", 0))+1:]) < 29:
        networks=list(ipaddress.ip_network(iprange, False).subnets(new_prefix=29))
        for smallerNet in networks:
            snet=list(ipaddress.ip_network(str(smallerNet)))
            Storage.processSubnets(str(smallerNet),snet)
    else:
        subnet=list(ipaddress.ip_network(iprange, False).hosts())
        Storage.processSubnets(iprange,"32")

map = Storage.getMap()

print("*"*72)
print("**** Total IPs: ", Storage.getIPCount())
print("**** Private IPs: ", Storage.getPrivateCount())
print("*"*72)

for a in sorted(map.keys(), reverse=True):
  print("* ::", len(map[a]), "Subnets ::", a,"IPs Per Subnet ::", a*len(map[a]), "Total IPs", "::")
print("*"*72)

map = Storage.getMap()

lists = processData(Storage)

def test(lists):
  print("\n")
  print("#" * 72)
  print("Count IP List Sizes / Run Tests")
  print("#" * 72)
  for key in sorted(lists.keys()):
    count = 0
    for iprange in (lists[key]):
      x=list(ipaddress.ip_network(iprange, False).hosts())
      if x == []:
          x=list(ipaddress.ip_network(iprange, False))
      count = count + len(x) + 2
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
