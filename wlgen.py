import time
start = time.clock()

import ConfigParser
import itertools

def all_perms(itemList):
  perms = []
  n = len(itemList)

  for i in range (1,n+1):
    for perm in itertools.permutations(itemList,i):
      for connector in connectors:
          str = ''
          str += connector.join(perm)
          perms.append(str)
  return perms

def leetify(l): # Medico -> M3d1c0
  leeted = []
  aux = l
  v = len(replacements)
  # TODO Permutations with replacements list: Medico -> M3dico, Med1co, Medic0 and M3d1c0 but never M3d1co, M3dic0, Med1c0
  for i in replacements:
    aux = [w.replace(i[0], i[1]) for w in aux]
    leeted.extend([w.replace(i[0], i[1]) for w in l])
  leeted.extend(aux)
  return leeted
  
def to_file(filename, wordlist):
  f = open ( filename, 'w' )
  wordlist = sorted(list(set(wordlist)))
  f.write ('\n'.join(wordlist))
  f = open ( filename, 'r' )
  lines = 0
  for line in f:
    lines += 1
  f.close()
  print "Saving wordlist ("+str(lines)+" words) to "+filename+"."

Config = ConfigParser.ConfigParser()
Config.read("config.cfg")

replacements = Config.items('Replacements');
items = list(Config.get('Params','keywords').split(','))
connectors = list(Config.get('Params','connectors').split(','))
num_tails = list(Config.get('Params','num_tails').split(','))
tails = list(Config.get('Params','tails').split(','))
min_lenght = Config.get('Options','min_length')
max_lenght = Config.get('Options','max_length')
output = Config.get('Files','output')

m = len(items)
result = []

# TODO Extend input items with similar words that they can be found in dictionaries or password dictionaries
# Language dictionaries -> ftp.funet.fi/pub/unix/security/passwd/crack/dictionaries/
# Comparing words -> http://stackoverflow.com/questions/18871706/check-if-two-words-are-related-to-each-other

result.extend(all_perms(items))

if (Config.getboolean('Options','abbreviation')):
  # Abbr by element T[ab,cd,ef] -> t[a,cd,ef],t[ab,c,ef],t[ab,cd,e]
  abbr_items = list(items)
  for i in range(0,m):
    abbr_items = list(items)
    abbr_items[i] = abbr_items[i][0]
    result.extend(all_perms(abbr_items))

  # Abbr acum forward T[ab,cd,ef] -> t[a,cd,ef],t[a,c,ef],t[a,c,e]
  abbr_items = list(items)
  for i in range(0,m):
    abbr_items[i] = abbr_items[i][0]
    result.extend(all_perms(abbr_items))

  # Abbr acum backward T[ab,cd,ef] -> t[ab,cd,e],t[ab,c,e],t[a,c,e]
  abbr_items = list(items)
  for i in range(0,m):
    k = m-i-1
    abbr_items[k] = abbr_items[k][0]
    result.extend(all_perms(abbr_items))

if (Config.getboolean('Options','reverse')):
  # Reverse by element T[ab,cd,ef] -> t[ba,cd,ef],t[ba,dc,ef],t[ba,dc,fe]
  inv_items = list(items)
  for i in range(0,m):
    inv_items = list(items)
    inv_items[i] = inv_items[i][::-1]
    result.extend(all_perms(inv_items))
    
  # Reverse acum forward T[ab,cd,ef] -> t[ba,cd,ef],t[ba,dc,ef],t[ba,dc,fe]
  inv_items = list(items)
  for i in range(0,m):
    inv_items[i] = inv_items[i][::-1]
    result.extend(all_perms(inv_items))
    
  # Reverse acum backward T[ab,cd,ef] -> t[ab,cd,fe],t[ab,dc,fe],t[ba,cd,ef]
  inv_items = list(items)
  for i in range(0,m):
    k = m-i-1
    inv_items[k] = inv_items[k][::-1]
    result.extend(all_perms(inv_items))
  
result = sorted(list(set(result)))

if (Config.getboolean('Options','string_replacements')):
  result.extend(leetify(result))

# Add pretails and tails
aux = []
for item in result:
  for tail in tails:
    for pretail in num_tails:
      if "-" in pretail:
        limits = pretail.split('-')
        for x in range(int(limits[0]),int(limits[1])+1):
          aux.append(item+str(x)+tail)
      else:
        aux.append(item+pretail+tail)
        
result.extend(aux)

# Filter by length
result = [elem for elem in result if (len(elem) > int(min_lenght) and len(elem) < int(max_lenght))]

to_file(output, result)

end = time.clock()
print 'Wordlist generated in ' + str(end-start) + ' seconds.'