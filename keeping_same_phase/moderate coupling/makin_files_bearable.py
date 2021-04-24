import os, csv

if not os.path.exists('from_1.1_to_1.4_beta_0.2_short.dat'):
    os.mknod('from_1.1_to_1.4_beta_0.2_short.dat')

f_out = open('from_1.1_to_1.4_beta_0.2_short.dat', 'w')

with open('from_1.1_to_1.4_beta_0.2.dat', 'r') as f_in:
    for line in f_in :
        time = float(line.rstrip().split(' ')[0])
        print(time)
        if (time >= 14 and time <= 31) or (time >= 154 and time <= 171) :
            f_out.write(line)

f_in.close()
f_out.close()
