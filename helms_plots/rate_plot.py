import numpy as np
import  matplotlib.pyplot as plt 

plt.xkcd()

X = np.genfromtxt('bgRt')

d0 = min(X[:,0])

X[:,0] = X[:,0] - d0


rates = X[:,1]


rates = np.log10(rates*4) + 4

plt.plot(abs(X[:,0]/365.25 - 2005), rates, color='#5fbdce', linewidth=2.5, label='$R(r_0, t)$')

plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))

plt.axhline(np.median(rates), color='k', linestyle='dashed', alpha=0.5, label='$Median(R)$')
# plt.gca().get_yaxis().get_ticker().set_scientific(True)

plt.title('stationary modeled seismicity sate in one cell')
plt.xlabel('Time')
plt.ylabel('Seismic Rate [m > 0]')
plt.legend(fontsize='small')

plt.show()
