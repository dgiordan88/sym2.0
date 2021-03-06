import sys
import os
p = os.path.abspath('..')
sys.path.append(p+"/")

from Simulator.RunSim import *
from Simulator.Globals.GlobalVar import * 
import datetime as datetime
import pickle

from multiprocessing import Process
import multiprocessing

def main():


    walkingTreshold = 1000000#int(sys.argv[4]) # in [m]

    zoneEnjoy = 220

    # countNoRech = {}

    #BookingID_Car = load()
    a = datetime.datetime.now()
    Stamps_Events = pickle.load( open( "../events/"+provider+"_sorted_dict_events_obj.pkl", "rb" ) )
    b = datetime.datetime.now()    
    c = (b - a).total_seconds()
    print("End Load Events: "+str(int(c)))


    a = datetime.datetime.now()    
    global DistancesFrom_Zone_Ordered 
    DistancesFrom_Zone_Ordered = pickle.load( open( "../input/"+provider+"_ZoneDistances.p", "rb" ) )
    b = datetime.datetime.now()    
    c = (b - a).total_seconds()
    print("End Load Zones: "+str(int(c)))
    i=0
    
    ZoneCars = pickle.load( open( "../input/"+provider+"_ZoneCars.p", "rb" ) )


    
    a = datetime.datetime.now()    
    global RechargingStation_Zones
    #RechargingStation_Zones = loadRecharing(algorithm, provider, numberOfStations)
    b = datetime.datetime.now()    
    c = (b - a).total_seconds()
    print("End Load Recharging: "+str(int(c)))


    simulations_parameters = [1]
    
    
    #simulation 1
    
    numberOfStations =20#len(RechargingStation_Zones)#int(sys.argv[1])
    algorithm = "custom"#str(sys.argv[2])
    tankThreshold = 20#int(sys.argv[3]) # in [%]

    jobs = []

    manager = multiprocessing.Manager()
    return_dict = manager.dict()

    RechargingStation_Zones = []
    
    while len(RechargingStation_Zones)<numberOfStations:
        rn = np.random.randint(NColumns*Nrows, size = 1)[0]
        if(rn not in RechargingStation_Zones): RechargingStation_Zones.append(rn)
    
    '''
    for k in range(0,1):    
        
        RechargingStation_Zones = [i for i in range(0,40)]
        
        p = Process(target=RunSim,args = (algorithm,numberOfStations,tankThreshold,walkingTreshold,ZoneCars,Stamps_Events,\
                                           RechargingStation_Zones,DistancesFrom_Zone_Ordered,return_dict,k))
    
        jobs.append(p)
        p.start()
        
    for proc in jobs:
        proc.join()'''
    
    
    results = ""
    k=0
    while 1:
        index=np.random.randint(len(RechargingStation_Zones), size = 1)[0]
        ID=RechargingStation_Zones[index]
        retv = zoneIDtoMatrixCoordinates(ID) 
        xy= [retv[1],retv[2]]
        RechargingStation_Zones_new=RechargingStation_Zones.copy()
        IDn=-1
        while IDn < 0:
            pos=np.random.randint(2, size = 1)[0]
            PiuMeno=np.random.randint(2, size = 1)[0]
            xynew=xy
            xynew[pos]=xynew[pos]+(PiuMeno-1.5)*2
            IDn=MatrixCoordinatesToID(xynew[0],xynew[1])
        
        RechargingStation_Zones_new[index]=IDn
        
        p = Process(target=RunSim,args = (algorithm,numberOfStations,tankThreshold,walkingTreshold,ZoneCars,Stamps_Events,\
                                           RechargingStation_Zones_new,DistancesFrom_Zone_Ordered,return_dict,k))
    
        jobs.append(p)
        p.start()
        for proc in jobs:
            proc.join()


        new_results=""
        for val in return_dict.values():
            if(val["ProcessID"]==k): new_results = val
            
        print()
        print("NEW STEP")
        print(RechargingStation_Zones_new)
        print(new_results)
        if k==0 or (new_results["PercDeath"] <=results["PercDeath"] and new_results["MeanMeterEnd"]< results["MeanMeterEnd"]):
            RechargingStation_Zones=RechargingStation_Zones_new.copy()
            results=new_results.copy()
            print()
            print("NEW BEST SOLUTION FOUND")
            print(RechargingStation_Zones)
            print(results)

        k+=1


    print("\n\n\n")
    for val in return_dict.values():
        print(val)
        print("\n\n\n")

    #PercRerouteEnd, PercRerouteStart, PercRecharge,PercDeath, MedianMeterEnd, MeanMeterEnd, MedianMeterStart, MeanMeterStart, NEnd, NStart = \
    #        RunSim(algorithm,numberOfStations,tankThreshold,walkingTreshold,ZoneCars,Stamps_Events,RechargingStation_Zones,DistancesFrom_Zone_Ordered)

    #print("PercRerouteEnd, PercRerouteStart, PercRecharge, PercDeath, MedianMeterEnd, MeanMeterEnd, MedianMeterStart, MeanMeterStart, NEnd, NStart")
    #print(PercRerouteEnd, PercRerouteStart, PercRecharge,PercDeath, MedianMeterEnd, MeanMeterEnd, MedianMeterStart, MeanMeterStart, NEnd, NStart)
    
    #PercRerouteEnd, PercRerouteStart, PercRecharge,PercDeath, MedianMeterEnd, MeanMeterEnd, MedianMeterStart, MeanMeterStart, NEnd, NStart = \
    #        RunSim(algorithm,numberOfStations,tankThreshold,walkingTreshold,ZoneCars,Stamps_Events,RechargingStation_Zones,DistancesFrom_Zone_Ordered)

    #print("PercRerouteEnd, PercRerouteStart, PercRecharge, PercDeath, MedianMeterEnd, MeanMeterEnd, MedianMeterStart, MeanMeterStart, NEnd, NStart")
    #print(PercRerouteEnd, PercRerouteStart, PercRecharge,PercDeath, MedianMeterEnd, MeanMeterEnd, MedianMeterStart, MeanMeterStart, NEnd, NStart)

main()

