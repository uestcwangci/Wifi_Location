a=[['1','2','3'],['4','5','6']]


Network = open('test.txt', 'w')
for i in a:
    xx = ' | '.join(i)
    Network.write(xx)
    Network.write('\n')
# Network.write('\n')
Network.close()
