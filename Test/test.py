import scipy.io as sio
import sqlite3
sample = sio.loadmat('totalAve.mat')
conn = sqlite3.connect('rssi_map.db')
cursor = conn.cursor()
rssi = sample['rssiAve']
x = sample['locAve'][:, 0]
y = sample['locAve'][:, 1]
n = len(x)
cursor.execute("""create table rssi_ave
(
  x   tinyint unsigned                not null,
  y   tinyint unsigned                not null,
  ap1 double default '-100.0000' not null,
  ap2 double default '-100.0000' not null,
  ap3 double default '-100.0000' not null,
  ap4 double default '-100.0000' not null,
  primary key (x, y)
);""")
for i in range(n):
    sql = 'insert into rssi_ave (x, y, ap1, ap2, ap3, ap4) values (%f, %f, %f, %f, %f, %f)'\
          % (x[i], y[i], rssi[i, 0], rssi[i, 1], rssi[i, 2], rssi[i, 3])
    cursor.execute(sql)
conn.commit()
conn.close()

