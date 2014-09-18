import datetime

net = '255.255.255.128'
ip = '172.10.80.64'


def cmask(num):
    if num >= 8:
        return(255);
    bitpat=0xff00; 
    while num > 0:
        bitpat=bitpat >> 1
        num -= 1
    return(bitpat & 0xff);
def check_mask(tmpvar):
    asd = []
    if tmpvar >= 8:
        asd.append(255)
        tmpvar-=8;
    else:
        asd.append(cmask(tmpvar))
        tmpvar = 0
    if tmpvar >= 8:
        asd.append(255)
        tmpvar-=8;
    else:
        asd.append(cmask(tmpvar))
        tmpvar = 0
    if tmpvar >= 8:
        asd.append(255)
        tmpvar-=8;
    else:
        asd.append(cmask(tmpvar))
        tmpvar = 0
    asd.append(cmask(tmpvar))
    return asd

print check_mask(9)

ip_list = []
n = net.split('.')
ii = ip.split('.')
cs = []
ce = []
if int(n[3]) == 254:
    cs.append(int(ii[0]) & int(n[0]))
    cs.append(int(ii[1]) & int(n[1]))
    cs.append(int(ii[2]) & int(n[2]))
    cs.append(int(ii[3]) & int(n[3]))
    ce.append(int(ii[0]) | (~ int(n[0]) & 0xff))
    ce.append(int(ii[1]) | (~ int(n[1]) & 0xff))
    ce.append(int(ii[2]) | (~ int(n[2]) & 0xff))
    ce.append(int(ii[3]) | (~ int(n[3]) & 0xff))
else:
    cs.append(int(ii[0]) & int(n[0]))
    cs.append(int(ii[1]) & int(n[1]))
    cs.append(int(ii[2]) & int(n[2]))
    cs.append((int(ii[3]) & int(n[3])) + 1)
    ce.append(int(ii[0]) | (~ int(n[0]) & 0xff))
    ce.append(int(ii[1]) | (~ int(n[1]) & 0xff))
    ce.append(int(ii[2]) | (~ int(n[2]) & 0xff))
    ce.append((int(ii[3]) | (~ int(n[3]) & 0xff)) - 1)
    


        
print cs
print ce

#print x
#print x  + 256 - int(n[3]) - 3
