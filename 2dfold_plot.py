
from matplotlib import pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import math

from matplotlib import rc
rc('font',**{'family':'sans-serif','sans-serif':['Arial']})



line_length = 10000
max_ofset=3000
source_spacing = 10
receiver_spacing = 5
bin_length = receiver_spacing/2
bin_length = 5

n_sources = int(line_length/source_spacing)
n_receivers = int((line_length-source_spacing/2)/receiver_spacing)
sources = np.linspace(0, n_sources*source_spacing, n_sources+1)
receivers = np.linspace(receiver_spacing/2, receiver_spacing/2 + n_receivers*receiver_spacing, n_receivers+1)
zeros_source = np.zeros(sources.shape)
zeros_receivers = np.zeros(receivers.shape)
nbins = int((line_length - bin_length)/bin_length)
bin_centers=np.linspace(bin_length, nbins*bin_length, nbins+1)
cmp = []
bin_counts = np.zeros(bin_centers.shape)
n = 0

for i in range(0, len(sources)):
    xsource = sources[i]
    
    for j in range(0, len(receivers)):
        xreceiver = receivers[j]
        dist = np.abs(xreceiver-xsource)
        if dist < max_ofset:
            this_cmp = xsource + 0.5*(xreceiver-xsource)
            cmp.append(this_cmp)
            n=n+1

            # find nearest bincenter
            # add a count to associated bin_count

            dist = np.min(np.abs(bin_centers-this_cmp))
            index = np.argmin(np.abs(bin_centers-this_cmp))
            bin_counts[index] = bin_counts[index] +1
                          
print(str(n)+' common mid-points')

ax1 = plt.subplot(2, 1, 2)
ax1.spines["left"].set_color('none')
ax1.spines["right"].set_color('none')
ax1.spines["bottom"].set_position('zero')
ax1.spines["top"].set_color('none')
ax1.scatter(receivers, zeros_receivers, s=25)
ax1.scatter(sources,zeros_source, marker="*", s=35)
ax1.set_xlim([-bin_length/2, 10.5* bin_length])
ax1.yaxis.set_major_locator(ticker.NullLocator())

ax2 = plt.subplot(2, 1, 1)
ax2.spines["left"].set_position('zero')
#ax2.spines["left"].set_smart_bounds(True)
ax2.spines["right"].set_color('none')
ax2.spines["bottom"].set_position('zero')
#ax2.spines["bottom"].set_smart_bounds(True)
ax2.set_xticks(np.linspace(0,line_length, 6), [int(a) if a else '' for a in np.linspace(0,line_length, 6)])

max_fold = np.max(bin_counts)
if max_fold > 100:
    new_top_lim = int(100*math.ceil(1.2*max_fold/100))
    inc = int(100*int((new_top_lim / 4)/100))
    
else:
    new_top_lim = int(10*math.ceil(max_fold/10))
    inc = int(10*int((new_top_lim / 4)/10))

vector = np.arange(0,new_top_lim, inc)
ax2.set_yticks(vector, [int(a) if a else '' for a in vector])

ax2.spines["top"].set_color('none')
ax2.plot(bin_centers, bin_counts)
ax2.set_ylabel("fold")
ax2.set_xlabel("distance (m)")


plt.show()