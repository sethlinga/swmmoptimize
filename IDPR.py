from swmm5.swmm5tools import SWMM5Simulation 
import math

#Make a list of OUTFALL nodes
#no = st.entityList(within='NODE')
#outfall_node = [f for f in no if 'OF' in f]

def IrrigationDeficit(swmmfile, IWR):
    st=SWMM5Simulation(swmmfile)
    #Volume of water supplied to each offtake
    total_effective_volume=0.0
    total_required_volume=0.0
    for node, wreq in IWR.items():
        inflow = list(st.Results('NODE', node, 4)) #Inflow (per 1-hr time step) in CMS
        volume = [v * 3600 for v in inflow] #Volume (per 1-hr time step) in m3
        total_volume = math.fsum (volume) #Total volume

        effective_vol= wreq if total_volume > wreq else total_volume
        total_effective_volume = total_effective_volume + effective_vol
        total_required_volume = total_required_volume + wreq
        deficit = total_required_volume-total_effective_volume
        print ("Node", node ,"has VolSupplied of", total_volume, "and VolDelivered of", wreq, "and effective_volume of", effective_vol, '\n')
        print ("Total effective volume: ", total_effective_volume, "deficit ", deficit)
    return deficit

if __name__ == "__main__":
    inpfile='D:/IHE_Delft/Module 14_Thesis/SWMM/TalibonModel/SimplifiedTalibon.inp'
    IWR = {'OF-1':1200 , 'OF-2':1080, 'OF-3':1200, 'OF-A':35635}
    ird = IrrigationDeficit(inpfile, IWR)
    print(f"Irrigatino deficit is {ird}")