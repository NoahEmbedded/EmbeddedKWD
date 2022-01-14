import matplotlib.pyplot as plt 
import numpy as np
#Daten aus Messung
vorverarbeitungsdauer = np.array([317,317,318,318,317,318,319,321,317,320,319,321,321,319,320,321,319,319,320,321,318,321,319,321,321,321,321,321,320,319,320,319,319,318,318,318,320,321,321,320,321,321,320,320,321,320,321,321,321,321,321,319,317,321,318,321,319,318,320,319,319,318,319,318,319,320,321,319,318,319,320,317,319,318,319,319,319,318,318,318,319,318,318,319,319,321,319,318,318,320,320,318,318,318,318,318,320,319,318,319])
inferenzdauer = np.array([4659,4662,4662,4660,4659,4661,4663,4667,4659,4664,4662,4666,4667,4661,4666,4666,4662,4662,4665,4666,4660,4666,4663,4667,4667,4666,4666,4666,4666,4665,4666,4663,4664,4660,4662,4662,4664,4666,4666,4665,4667,4667,4663,4667,4667,4666,4666,4666,4667,4665,4667,4662,4660,4667,4661,4667,4662,4664,4665,4663,4663,4662,4662,4661,4662,4665,4666,4663,4663,4662,4664,4660,4662,4661,4660,4663,4662,4663,4661,4661,4661,4661,4661,4663,4664,4665,4663,4663,4663,4667,4665,4662,4662,4660,4662,4663,4665,4664,4660,4663])
#Diagramm
fig,axs = plt.subplots(3,1, gridspec_kw={'height_ratios':[1,0.01,1]})
fig.suptitle("Zeitmessungen der Microcontrollerimplementation",fontsize=22)

axs[2].plot(vorverarbeitungsdauer,'bx')
axs[2].plot([-1,1],[470,480],'k-',linewidth=2, markersize=12,clip_on=False)
axs[2].plot([99,101],[470,480],'k-',linewidth=2, markersize=12,clip_on=False)
axs[2].set_yticks(np.arange(0,455,50))
axs[2].set_xlim(0,100)
axs[2].set_ylim(0,475)
axs[2].yaxis.grid(True,linestyle = "--")

axs[0].plot(inferenzdauer,'rx')
axs[0].plot((),'bx')#stub für legende
axs[0].plot([-1,1],[4370,4380],'k-',linewidth=2, markersize=12,clip_on=False)
axs[0].plot([99,101],[4370,4380],'k-',linewidth=2, markersize=12,clip_on=False)
axs[0].set_yticks(np.arange(4400,4850,50))
axs[0].set_xticks([], [])
axs[0].set_xlim(0,100)
axs[0].set_ylim(4375,4850)
axs[0].yaxis.grid(True,linestyle = "--")
axs[0].legend(["Inferenzdauer","Vorverarbeitungsdauer"],fontsize="xx-large")

#Umrandungen der Subplots entfernen, damit es wie ein großer plot aussieht
axs[0].spines['bottom'].set_visible(False)
axs[2].spines['top'].set_visible(False)
#Pseudoplot für gemeinsames y-label
axs[1].spines['bottom'].set_visible(False)
axs[1].spines['top'].set_visible(False)
axs[1].spines['right'].set_visible(False)
axs[1].spines['left'].set_visible(False)
axs[1].tick_params(axis='y', colors='white')#"unsichtbare" ticks als abstandshalter für label
axs[1].set_yticks(np.arange(1000,1010))
axs[1].set_xticks([],[])
#label


axs[2].set_xlabel("Messung",fontsize="xx-large")
axs[1].set_ylabel("Dauer in ms",fontsize="xx-large")
plt.show()

print("stabw inferenz in ms: ",np.std(inferenzdauer))
print("stabw vorverarbeitung in ms: ",np.std(vorverarbeitungsdauer))
print("mittelwert vorverarbeitung in ms: ",np.mean(vorverarbeitungsdauer))
print("mittelwert inferenz in ms: ",np.mean(inferenzdauer))

