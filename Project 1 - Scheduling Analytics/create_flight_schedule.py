
# coding: utf-8

# In[744]:

# Function To Convert MidNight Time to Military Time #

def ConvertMidToMil(MidNightTime):
    MilitaryTime=str('{:02}'.format(MidNightTime//60))+('{:02}'.format(MidNightTime%60))
    return MilitaryTime;


# In[745]:

# Function To Convert Military Time to Midnight Time #

def ConvertMilToMid(MilitaryTime):
    ZeroPadTime=('{:04}'.format(MilitaryTime))
    MidNightTime=(int(str(ZeroPadTime)[:2])*60)+(int(str(ZeroPadTime)[2:]))
    return MidNightTime
    


# In[746]:

# Initialize the number of Flights/Tails #

Tail_Number=['T1','T2','T3','T4','T5','T6']

# Assign Source Destination Flight Time #

SourceDestination = {'DAL HOU':65,'HOU AUS':45,'AUS DAL':50,'DAL AUS':50,'AUS HOU':45,'HOU DAL':65}

# Assign Ground Time for each Airport #

GroundTime = {'DAL_G1':30,'DAL_G2':30,'HOU_G1':35,'HOU_G2':35,'HOU_G3':35,'AUS_G1':25}

# Assign the number of Cycle #

Cycle=1

# Gates to Airport Mapping #

GateMapping = {'DAL_G1':'DAL','DAL_G2':'DAL','HOU_1':'HOU','HOU_2':'HOU','HOU_3':'HOU','AUS_G1':'AUS'}

# Assign Initital Origin of  Each Flight to each Gate #

Ori_T1='HOU_G1'
Ori_T2='AUS_G1'
Ori_T3='HOU_G2'
Ori_T4='HOU_G3'
Ori_T5='DAL_G1'
Ori_T6='DAL_G2'


# Assign Initital Destination of Each Flight to each Gate #

Dest_T1='AUS_G1'
Dest_T2='HOU_G1'
Dest_T3='DAL_G1'
Dest_T4='DAL_G2'
Dest_T5='HOU_G2'
Dest_T6='HOU_G3'

# Assign Initial Flight Departure Time to all Flights #

DeptNow_T1=DeptNow_T2=DeptNow_T3=DeptNow_T4=DeptNow_T5=DeptNow_T6=600

# Calculate Arrival Time of each flight based on initial run #

ArrivalNow_T1=AUS_G1=int(ConvertMidToMil(ConvertMilToMid(DeptNow_T1)+SourceDestination[Ori_T1[:3]+' '+Dest_T1[:3]]))
ArrivalNow_T2=HOU_G1=int(ConvertMidToMil(ConvertMilToMid(DeptNow_T2)+SourceDestination[Ori_T2[:3]+' '+Dest_T2[:3]]))
ArrivalNow_T3=DAL_G1=int(ConvertMidToMil(ConvertMilToMid(DeptNow_T3)+SourceDestination[Ori_T3[:3]+' '+Dest_T3[:3]]))
ArrivalNow_T4=DAL_G2=int(ConvertMidToMil(ConvertMilToMid(DeptNow_T4)+SourceDestination[Ori_T4[:3]+' '+Dest_T4[:3]]))
ArrivalNow_T5=HOU_G2=int(ConvertMidToMil(ConvertMilToMid(DeptNow_T5)+SourceDestination[Ori_T5[:3]+' '+Dest_T5[:3]]))
ArrivalNow_T6=HOU_G3=int(ConvertMidToMil(ConvertMilToMid(DeptNow_T6)+SourceDestination[Ori_T6[:3]+' '+Dest_T6[:3]]))

# Print the 1st cycle of Flight Schedule #

Flight_Schedule=[['T1','HOU','AUS','0600','0645'],
                ['T2','AUS','HOU','0600','0645'],
                ['T3','HOU','DAL','0600','0705'],
                ['T4','HOU','DAL','0600','0705'],
                ['T5','DAL','HOU','0600','0705'],
                ['T6','DAL','HOU','0600','0705']]


# In[736]:

# Function to calculate Next Departure Time #

def NextDeptTime (T,Arrival,Dest):
    #GroundTime = {'DAL':30,'HOU':35,'AUS':25}
    GroundTime = {'DAL_G1':30,'DAL_G2':30,'HOU_G1':35,'HOU_G2':35,'HOU_G3':35,'AUS_G1':25}
    if T == 'T1':
        NextDepartureTime_T1=Arrival+GroundTime[Dest]
        return NextDepartureTime_T1;
    if T == 'T2':
        NextDepartureTime_T2=Arrival+GroundTime[Dest]
        return NextDepartureTime_T2;
    if T == 'T3':
        NextDepartureTime_T3=Arrival+GroundTime[Dest]
        return NextDepartureTime_T3;
    if T == 'T4':
        NextDepartureTime_T4=Arrival+GroundTime[Dest]
        return NextDepartureTime_T4;
    if T == 'T5':
        NextDepartureTime_T5=Arrival+GroundTime[Dest]
        return NextDepartureTime_T5;
    if T == 'T6':
        NextDepartureTime_T6=Arrival+GroundTime[Dest]
        return NextDepartureTime_T6;   


# In[739]:

# Function to calculate Next Arrival Time + Destination #

def NextArrivalTimeDest (T, AUS_G1, DAL_G1, DAL_G2, HOU_G1, HOU_G2, HOU_G3, NextDeparture, Origin):
    NextDeparture = int(NextDeparture)
    NextDeparture = ConvertMilToMid(NextDeparture)
    MaxGrndTime=36
    AUS_G1 = ConvertMilToMid(AUS_G1)
    DAL_G1 = ConvertMilToMid(DAL_G1)
    DAL_G2 = ConvertMilToMid(DAL_G2)
    HOU_G1 = ConvertMilToMid(HOU_G1)
    HOU_G2 = ConvertMilToMid(HOU_G2)
    HOU_G3 = ConvertMilToMid(HOU_G3)
    if T == 'T1':
        if Origin[:1] == 'A':
            GrdTimeIncr = 1
            while (GrdTimeIncr<MaxGrndTime):
                if NextDeparture+50 > DAL_G1+30:
                    NextArrivalTimeMid_T1 = NextDeparture + 50 
                    NextArrivalTimeMilitary_T1 = ConvertMidToMil(NextArrivalTimeMid_T1)
                    NextArrivalTimeMilitary_T1_Dest = NextArrivalTimeMilitary_T1 + 'DAL_G1'
                    return NextArrivalTimeMilitary_T1_Dest; 
                elif NextDeparture+45 > HOU_G3+35:
                    NextArrivalTimeMid_T1 = NextDeparture + 45 
                    NextArrivalTimeMilitary_T1 = ConvertMidToMil(NextArrivalTimeMid_T1)
                    NextArrivalTimeMilitary_T1_Dest = NextArrivalTimeMilitary_T1 + 'HOU_G3'
                    return NextArrivalTimeMilitary_T1_Dest; 
                elif NextDeparture+45 > HOU_G1+35:
                    NextArrivalTimeMid_T1 = NextDeparture + 45 
                    NextArrivalTimeMilitary_T1 = ConvertMidToMil(NextArrivalTimeMid_T1)
                    NextArrivalTimeMilitary_T1_Dest = NextArrivalTimeMilitary_T1 + 'HOU_G1'
                    return NextArrivalTimeMilitary_T1_Dest;
                elif NextDeparture+45 > HOU_G2+35:
                    NextArrivalTimeMid_T1 = NextDeparture + 45 
                    NextArrivalTimeMilitary_T1 = ConvertMidToMil(NextArrivalTimeMid_T1)
                    NextArrivalTimeMilitary_T1_Dest = NextArrivalTimeMilitary_T1 + 'HOU_G2'
                    return NextArrivalTimeMilitary_T1_Dest; 
                elif NextDeparture+50 > DAL_G2+30:
                    NextArrivalTimeMid_T1 = NextDeparture + 50 
                    NextArrivalTimeMilitary_T1 = ConvertMidToMil(NextArrivalTimeMid_T1)
                    NextArrivalTimeMilitary_T1_Dest = NextArrivalTimeMilitary_T1 + 'DAL_G2'
                    return NextArrivalTimeMilitary_T1_Dest;
                else:
                    NextDeparture = NextDeparture + 1
                    GrdTimeIncr = GrdTimeIncr + 1
        elif Origin[:1] == 'D':
            GrdTimeIncr = 1
            while (GrdTimeIncr<MaxGrndTime):
                if NextDeparture+50 > AUS_G1+25:
                    NextArrivalTimeMid_T1 = NextDeparture + 50 
                    NextArrivalTimeMilitary_T1 = ConvertMidToMil(NextArrivalTimeMid_T1)
                    NextArrivalTimeMilitary_T1_Dest = NextArrivalTimeMilitary_T1 + 'AUS_G1'
                    return NextArrivalTimeMilitary_T1_Dest;  
                elif NextDeparture+65 > HOU_G1+35:
                    NextArrivalTimeMid_T1 = NextDeparture + 65 
                    NextArrivalTimeMilitary_T1 = ConvertMidToMil(NextArrivalTimeMid_T1)
                    NextArrivalTimeMilitary_T1_Dest = NextArrivalTimeMilitary_T1 + 'HOU_G1'
                    return NextArrivalTimeMilitary_T1_Dest;  
                elif NextDeparture+65 > HOU_G2+35:
                    NextArrivalTimeMid_T1 = NextDeparture + 65 
                    NextArrivalTimeMilitary_T1 = ConvertMidToMil(NextArrivalTimeMid_T1)
                    NextArrivalTimeMilitary_T1_Dest = NextArrivalTimeMilitary_T1 + 'HOU_G2'
                    return NextArrivalTimeMilitary_T1_Dest;  
                elif NextDeparture+65 > HOU_G3+35:
                    NextArrivalTimeMid_T1 = NextDeparture + 65 
                    NextArrivalTimeMilitary_T1 = ConvertMidToMil(NextArrivalTimeMid_T1)
                    NextArrivalTimeMilitary_T1_Dest = NextArrivalTimeMilitary_T1 + 'HOU_G3'
                    return NextArrivalTimeMilitary_T1_Dest;
                else:
                    NextDeparture = NextDeparture + 1
                    GrdTimeIncr = GrdTimeIncr + 1
        else:
            GrdTimeIncr = 1
            while (GrdTimeIncr<31):
                if NextDeparture+45 > AUS_G1+25:
                    NextArrivalTimeMid_T1 = NextDeparture + 45 
                    NextArrivalTimeMilitary_T1 = ConvertMidToMil(NextArrivalTimeMid_T1)
                    NextArrivalTimeMilitary_T1_Dest = NextArrivalTimeMilitary_T1 + 'AUS_G1'
                    return NextArrivalTimeMilitary_T1_Dest;  
                elif NextDeparture+65 > DAL_G1+30:
                    NextArrivalTimeMid_T1 = NextDeparture + 65 
                    NextArrivalTimeMilitary_T1 = ConvertMidToMil(NextArrivalTimeMid_T1)
                    NextArrivalTimeMilitary_T1_Dest = NextArrivalTimeMilitary_T1 + 'DAL_G1'
                    return NextArrivalTimeMilitary_T1_Dest;  
                elif NextDeparture+65 > DAL_G2+30:
                    NextArrivalTimeMid_T1 = NextDeparture + 65 
                    NextArrivalTimeMilitary_T1 = ConvertMidToMil(NextArrivalTimeMid_T1)
                    NextArrivalTimeMilitary_T1_Dest = NextArrivalTimeMilitary_T1 + 'DAL_G2'
                    return NextArrivalTimeMilitary_T1_Dest;
                else:
                    NextDeparture = NextDeparture + 1
                    GrdTimeIncr = GrdTimeIncr + 1
    elif T == 'T2':
        if Origin[:1] == 'A':
            GrdTimeIncr = 1
            while (GrdTimeIncr<MaxGrndTime):
                if NextDeparture+45 > HOU_G3+35:
                    NextArrivalTimeMid_T2 = NextDeparture + 45 
                    NextArrivalTimeMilitary_T2 = ConvertMidToMil(NextArrivalTimeMid_T2)
                    NextArrivalTimeMilitary_T2_Dest = NextArrivalTimeMilitary_T2 + 'HOU_G3'
                    return NextArrivalTimeMilitary_T2_Dest;
                elif NextDeparture+45 > HOU_G1+35:
                    NextArrivalTimeMid_T2 = NextDeparture + 45 
                    NextArrivalTimeMilitary_T2 = ConvertMidToMil(NextArrivalTimeMid_T2)
                    NextArrivalTimeMilitary_T2_Dest = NextArrivalTimeMilitary_T2 + 'HOU_G1'
                    return NextArrivalTimeMilitary_T2_Dest;
                elif NextDeparture+45 > HOU_G2+35:
                    NextArrivalTimeMid_T2 = NextDeparture + 45 
                    NextArrivalTimeMilitary_T2 = ConvertMidToMil(NextArrivalTimeMid_T2)
                    NextArrivalTimeMilitary_T2_Dest = NextArrivalTimeMilitary_T2 + 'HOU_G2'
                    return NextArrivalTimeMilitary_T2_Dest; 
                elif NextDeparture+50 > DAL_G2+30:
                    NextArrivalTimeMid_T2 = NextDeparture + 50 
                    NextArrivalTimeMilitary_T2 = ConvertMidToMil(NextArrivalTimeMid_T2)
                    NextArrivalTimeMilitary_T2_Dest = NextArrivalTimeMilitary_T2 + 'DAL_G2'
                    return NextArrivalTimeMilitary_T2_Dest;
                elif NextDeparture+50 > DAL_G1+30:
                    NextArrivalTimeMid_T2 = NextDeparture + 50 
                    NextArrivalTimeMilitary_T2 = ConvertMidToMil(NextArrivalTimeMid_T2)
                    NextArrivalTimeMilitary_T2_Dest = NextArrivalTimeMilitary_T2 + 'DAL_G1'
                    return NextArrivalTimeMilitary_T2_Dest;
                else:
                    NextDeparture = NextDeparture + 1
                    GrdTimeIncr = GrdTimeIncr + 1
        elif Origin[:1] == 'D':
            GrdTimeIncr = 1
            while (GrdTimeIncr<MaxGrndTime):
                if NextDeparture+50 > AUS_G1+25:
                    NextArrivalTimeMid_T2 = NextDeparture + 50 
                    NextArrivalTimeMilitary_T2 = ConvertMidToMil(NextArrivalTimeMid_T2)
                    NextArrivalTimeMilitary_T2_Dest = NextArrivalTimeMilitary_T2 + 'AUS_G1'
                    return NextArrivalTimeMilitary_T2_Dest;  
                elif NextDeparture+65 > HOU_G1+35:
                    NextArrivalTimeMid_T2 = NextDeparture + 65 
                    NextArrivalTimeMilitary_T2 = ConvertMidToMil(NextArrivalTimeMid_T2)
                    NextArrivalTimeMilitary_T2_Dest = NextArrivalTimeMilitary_T2 + 'HOU_G1'
                    return NextArrivalTimeMilitary_T2_Dest;  
                elif NextDeparture+65 > HOU_G2+35:
                    NextArrivalTimeMid_T2 = NextDeparture + 65 
                    NextArrivalTimeMilitary_T2 = ConvertMidToMil(NextArrivalTimeMid_T2)
                    NextArrivalTimeMilitary_T2_Dest = NextArrivalTimeMilitary_T2 + 'HOU_G2'
                    return NextArrivalTimeMilitary_T2_Dest;  
                elif NextDeparture+65 > HOU_G3+35:
                    NextArrivalTimeMid_T2 = NextDeparture + 65 
                    NextArrivalTimeMilitary_T2 = ConvertMidToMil(NextArrivalTimeMid_T2)
                    NextArrivalTimeMilitary_T2_Dest = NextArrivalTimeMilitary_T2 + 'HOU_G3'
                    return NextArrivalTimeMilitary_T2_Dest;
                else:
                    NextDeparture = NextDeparture + 1
                    GrdTimeIncr = GrdTimeIncr + 1
        else:
            GrdTimeIncr = 1
            while (GrdTimeIncr<31):
                if NextDeparture+45 > AUS_G1+25:
                    NextArrivalTimeMid_T2 = NextDeparture + 45 
                    NextArrivalTimeMilitary_T2 = ConvertMidToMil(NextArrivalTimeMid_T2)
                    NextArrivalTimeMilitary_T2_Dest = NextArrivalTimeMilitary_T2 + 'AUS_G1'
                    return NextArrivalTimeMilitary_T2_Dest;  
                elif NextDeparture+65 > DAL_G1+30:
                    NextArrivalTimeMid_T2 = NextDeparture + 65 
                    NextArrivalTimeMilitary_T2 = ConvertMidToMil(NextArrivalTimeMid_T2)
                    NextArrivalTimeMilitary_T2_Dest = NextArrivalTimeMilitary_T2 + 'DAL_G1'
                    return NextArrivalTimeMilitary_T2_Dest;  
                elif NextDeparture+65 > DAL_G2+30:
                    NextArrivalTimeMid_T2 = NextDeparture + 65 
                    NextArrivalTimeMilitary_T2 = ConvertMidToMil(NextArrivalTimeMid_T2)
                    NextArrivalTimeMilitary_T2_Dest = NextArrivalTimeMilitary_T2 + 'DAL_G2'
                    return NextArrivalTimeMilitary_T2_Dest;
                else:
                    NextDeparture = NextDeparture + 1
                    GrdTimeIncr = GrdTimeIncr + 1
    elif T == 'T3':
        if Origin[:1] == 'A':
            GrdTimeIncr = 1
            while(GrdTimeIncr<MaxGrndTime):
                if NextDeparture+50 > DAL_G1+30:
                    NextArrivalTimeMid_T3 = NextDeparture + 50 
                    NextArrivalTimeMilitary_T3 = ConvertMidToMil(NextArrivalTimeMid_T3)
                    NextArrivalTimeMilitary_T3_Dest = NextArrivalTimeMilitary_T3 + 'DAL_G1'
                    return NextArrivalTimeMilitary_T3_Dest; 
                elif NextDeparture+45 > HOU_G3+35:
                    NextArrivalTimeMid_T3 = NextDeparture + 45 
                    NextArrivalTimeMilitary_T3 = ConvertMidToMil(NextArrivalTimeMid_T3)
                    NextArrivalTimeMilitary_T3_Dest = NextArrivalTimeMilitary_T3 + 'HOU_G3'
                    return NextArrivalTimeMilitary_T3_Dest;
                elif NextDeparture+45 > HOU_G1+35:
                    NextArrivalTimeMid_T3 = NextDeparture + 45 
                    NextArrivalTimeMilitary_T3 = ConvertMidToMil(NextArrivalTimeMid_T3)
                    NextArrivalTimeMilitary_T3_Dest = NextArrivalTimeMilitary_T3 + 'HOU_G1'
                    return NextArrivalTimeMilitary_T3_Dest;
                elif NextDeparture+45 > HOU_G2+35:
                    NextArrivalTimeMid_T3 = NextDeparture + 45 
                    NextArrivalTimeMilitary_T3 = ConvertMidToMil(NextArrivalTimeMid_T3)
                    NextArrivalTimeMilitary_T3_Dest = NextArrivalTimeMilitary_T3 + 'HOU_G2'
                    return NextArrivalTimeMilitary_T3_Dest; 
                elif NextDeparture+50 > DAL_G2+30:
                    NextArrivalTimeMid_T3 = NextDeparture + 50 
                    NextArrivalTimeMilitary_T3 = ConvertMidToMil(NextArrivalTimeMid_T3)
                    NextArrivalTimeMilitary_T3_Dest = NextArrivalTimeMilitary_T3 + 'DAL_G2'
                    return NextArrivalTimeMilitary_T3_Dest;
                else:
                    NextDeparture = NextDeparture + 1
                    GrdTimeIncr = GrdTimeIncr + 1
        elif Origin[:1] == 'D':
            GrdTimeIncr = 1
            while (GrdTimeIncr<MaxGrndTime):
                if NextDeparture+50 > AUS_G1+25:
                    NextArrivalTimeMid_T3 = NextDeparture + 50 
                    NextArrivalTimeMilitary_T3 = ConvertMidToMil(NextArrivalTimeMid_T3)
                    NextArrivalTimeMilitary_T3_Dest = NextArrivalTimeMilitary_T3 + 'AUS_G1'
                    return NextArrivalTimeMilitary_T3_Dest;  
                elif NextDeparture+65 > HOU_G1+35:
                    NextArrivalTimeMid_T3 = NextDeparture + 65 
                    NextArrivalTimeMilitary_T3 = ConvertMidToMil(NextArrivalTimeMid_T3)
                    NextArrivalTimeMilitary_T3_Dest = NextArrivalTimeMilitary_T3 + 'HOU_G1'
                    return NextArrivalTimeMilitary_T3_Dest;  
                elif NextDeparture+65 > HOU_G2+35:
                    NextArrivalTimeMid_T3 = NextDeparture + 65 
                    NextArrivalTimeMilitary_T3 = ConvertMidToMil(NextArrivalTimeMid_T3)
                    NextArrivalTimeMilitary_T3_Dest = NextArrivalTimeMilitary_T3 + 'HOU_G2'
                    return NextArrivalTimeMilitary_T3_Dest;  
                elif NextDeparture+65 > HOU_G3+35:
                    NextArrivalTimeMid_T3 = NextDeparture + 65 
                    NextArrivalTimeMilitary_T3 = ConvertMidToMil(NextArrivalTimeMid_T3)
                    NextArrivalTimeMilitary_T3_Dest = NextArrivalTimeMilitary_T3 + 'HOU_G3'
                    return NextArrivalTimeMilitary_T3_Dest;
                else:
                    NextDeparture = NextDeparture + 1
                    GrdTimeIncr = GrdTimeIncr + 1
        else:
            GrdTimeIncr = 1
            while(GrdTimeIncr<31):
                if NextDeparture+45 > AUS_G1+25:
                    NextArrivalTimeMid_T3 = NextDeparture + 45 
                    NextArrivalTimeMilitary_T3 = ConvertMidToMil(NextArrivalTimeMid_T3)
                    NextArrivalTimeMilitary_T3_Dest = NextArrivalTimeMilitary_T3 + 'AUS_G1'
                    return NextArrivalTimeMilitary_T3_Dest;  
                elif NextDeparture+65 > DAL_G1+30:
                    NextArrivalTimeMid_T3 = NextDeparture + 65 
                    NextArrivalTimeMilitary_T3 = ConvertMidToMil(NextArrivalTimeMid_T3)
                    NextArrivalTimeMilitary_T3_Dest = NextArrivalTimeMilitary_T3 + 'DAL_G1'
                    return NextArrivalTimeMilitary_T3_Dest;  
                elif NextDeparture+65 > DAL_G2+30:
                    NextArrivalTimeMid_T3 = NextDeparture + 65 
                    NextArrivalTimeMilitary_T3 = ConvertMidToMil(NextArrivalTimeMid_T3)
                    NextArrivalTimeMilitary_T3_Dest = NextArrivalTimeMilitary_T3 + 'DAL_G2'
                    return NextArrivalTimeMilitary_T3_Dest;
                else:
                    NextDeparture = NextDeparture + 1
                    GrdTimeIncr = GrdTimeIncr + 1
    elif T == 'T4':
        if Origin[:1] == 'A':
            GrdTimeIncr = 1
            while(GrdTimeIncr<MaxGrndTime):
                if NextDeparture+45 > HOU_G3+35:
                    NextArrivalTimeMid_T4 = NextDeparture + 45 
                    NextArrivalTimeMilitary_T4 = ConvertMidToMil(NextArrivalTimeMid_T4)
                    NextArrivalTimeMilitary_T4_Dest = NextArrivalTimeMilitary_T4 + 'HOU_G3'
                    return NextArrivalTimeMilitary_T4_Dest;
                elif NextDeparture+45 > HOU_G1+35:
                    NextArrivalTimeMid_T4 = NextDeparture + 45 
                    NextArrivalTimeMilitary_T4 = ConvertMidToMil(NextArrivalTimeMid_T4)
                    NextArrivalTimeMilitary_T4_Dest = NextArrivalTimeMilitary_T4 + 'HOU_G1'
                    return NextArrivalTimeMilitary_T4_Dest;
                elif NextDeparture+45 > HOU_G2+35:
                    NextArrivalTimeMid_T4 = NextDeparture + 45 
                    NextArrivalTimeMilitary_T4 = ConvertMidToMil(NextArrivalTimeMid_T4)
                    NextArrivalTimeMilitary_T4_Dest = NextArrivalTimeMilitary_T4 + 'HOU_G2'
                    return NextArrivalTimeMilitary_T4_Dest; 
                elif NextDeparture+50 > DAL_G2+30:
                    NextArrivalTimeMid_T4 = NextDeparture + 50 
                    NextArrivalTimeMilitary_T4 = ConvertMidToMil(NextArrivalTimeMid_T4)
                    NextArrivalTimeMilitary_T4_Dest = NextArrivalTimeMilitary_T4 + 'DAL_G2'
                    return NextArrivalTimeMilitary_T4_Dest;
                elif NextDeparture+50 > DAL_G1+30:
                    NextArrivalTimeMid_T4 = NextDeparture + 50 
                    NextArrivalTimeMilitary_T4 = ConvertMidToMil(NextArrivalTimeMid_T4)
                    NextArrivalTimeMilitary_T4_Dest = NextArrivalTimeMilitary_T4 + 'DAL_G1'
                    return NextArrivalTimeMilitary_T4_Dest;
                else:
                    NextDeparture = NextDeparture + 1
                    GrdTimeIncr = GrdTimeIncr + 1
        elif Origin[:1] == 'D':
            GrdTimeIncr = 1
            while(GrdTimeIncr<MaxGrndTime):
                if NextDeparture+50 > AUS_G1+25:
                    NextArrivalTimeMid_T4 = NextDeparture + 50 
                    NextArrivalTimeMilitary_T4 = ConvertMidToMil(NextArrivalTimeMid_T4)
                    NextArrivalTimeMilitary_T4_Dest = NextArrivalTimeMilitary_T4 + 'AUS_G1'
                    return NextArrivalTimeMilitary_T4_Dest;  
                elif NextDeparture+65 > HOU_G1+35:
                    NextArrivalTimeMid_T4 = NextDeparture + 65 
                    NextArrivalTimeMilitary_T4 = ConvertMidToMil(NextArrivalTimeMid_T4)
                    NextArrivalTimeMilitary_T4_Dest = NextArrivalTimeMilitary_T4 + 'HOU_G1'
                    return NextArrivalTimeMilitary_T4_Dest;  
                elif NextDeparture+65 > HOU_G2+35:
                    NextArrivalTimeMid_T4 = NextDeparture + 65 
                    NextArrivalTimeMilitary_T4 = ConvertMidToMil(NextArrivalTimeMid_T4)
                    NextArrivalTimeMilitary_T4_Dest = NextArrivalTimeMilitary_T4 + 'HOU_G2'
                    return NextArrivalTimeMilitary_T4_Dest;  
                elif NextDeparture+65 > HOU_G3+35:
                    NextArrivalTimeMid_T4 = NextDeparture + 65 
                    NextArrivalTimeMilitary_T4 = ConvertMidToMil(NextArrivalTimeMid_T4)
                    NextArrivalTimeMilitary_T4_Dest = NextArrivalTimeMilitary_T4 + 'HOU_G3'
                    return NextArrivalTimeMilitary_T4_Dest;  
        else:
            GrdTimeIncr = 1
            while (GrdTimeIncr<31):
                if NextDeparture+45 > AUS_G1+25:
                    NextArrivalTimeMid_T4 = NextDeparture + 45 
                    NextArrivalTimeMilitary_T4 = ConvertMidToMil(NextArrivalTimeMid_T4)
                    NextArrivalTimeMilitary_T4_Dest = NextArrivalTimeMilitary_T4 + 'AUS_G1'
                    return NextArrivalTimeMilitary_T4_Dest;  
                elif NextDeparture+65 > DAL_G1+30:
                    NextArrivalTimeMid_T4 = NextDeparture + 65 
                    NextArrivalTimeMilitary_T4 = ConvertMidToMil(NextArrivalTimeMid_T4)
                    NextArrivalTimeMilitary_T4_Dest = NextArrivalTimeMilitary_T4 + 'DAL_G1'
                    return NextArrivalTimeMilitary_T4_Dest;  
                elif NextDeparture+65 > DAL_G2+30:
                    NextArrivalTimeMid_T4 = NextDeparture + 65 
                    NextArrivalTimeMilitary_T4 = ConvertMidToMil(NextArrivalTimeMid_T4)
                    NextArrivalTimeMilitary_T4_Dest = NextArrivalTimeMilitary_T4 + 'DAL_G2'
                    return NextArrivalTimeMilitary_T4_Dest;
                else:
                    NextDeparture = NextDeparture + 1
                    GrdTimeIncr = GrdTimeIncr + 1
    elif T == 'T5':
        if Origin[:1] == 'A':
            GrdTimeIncr = 1
            while(GrdTimeIncr<MaxGrndTime):
                if NextDeparture+50 > DAL_G1+30:
                    NextArrivalTimeMid_T5 = NextDeparture + 50 
                    NextArrivalTimeMilitary_T5 = ConvertMidToMil(NextArrivalTimeMid_T5)
                    NextArrivalTimeMilitary_T5_Dest = NextArrivalTimeMilitary_T5 + 'DAL_G1'
                    return NextArrivalTimeMilitary_T5_Dest; 
                elif NextDeparture+45 > HOU_G3+35:
                    NextArrivalTimeMid_T5 = NextDeparture + 45 
                    NextArrivalTimeMilitary_T5 = ConvertMidToMil(NextArrivalTimeMid_T5)
                    NextArrivalTimeMilitary_T5_Dest = NextArrivalTimeMilitary_T5 + 'HOU_G3'
                    return NextArrivalTimeMilitary_T5_Dest;
                elif NextDeparture+45 > HOU_G1+35:
                    NextArrivalTimeMid_T5 = NextDeparture + 45 
                    NextArrivalTimeMilitary_T5 = ConvertMidToMil(NextArrivalTimeMid_T5)
                    NextArrivalTimeMilitary_T5_Dest = NextArrivalTimeMilitary_T5 + 'HOU_G1'
                    return NextArrivalTimeMilitary_T5_Dest;
                elif NextDeparture+45 > HOU_G2+35:
                    NextArrivalTimeMid_T5 = NextDeparture + 45 
                    NextArrivalTimeMilitary_T5 = ConvertMidToMil(NextArrivalTimeMid_T5)
                    NextArrivalTimeMilitary_T5_Dest = NextArrivalTimeMilitary_T5 + 'HOU_G2'
                    return NextArrivalTimeMilitary_T5_Dest; 
                elif NextDeparture+50 > DAL_G2+30:
                    NextArrivalTimeMid_T5 = NextDeparture + 50 
                    NextArrivalTimeMilitary_T5 = ConvertMidToMil(NextArrivalTimeMid_T5)
                    NextArrivalTimeMilitary_T5_Dest = NextArrivalTimeMilitary_T5 + 'DAL_G2'
                    return NextArrivalTimeMilitary_T5_Dest;
                else:
                    NextDeparture = NextDeparture + 1
                    GrdTimeIncr = GrdTimeIncr + 1
        elif Origin[:1] == 'D':
            GrdTimeIncr = 1
            while(GrdTimeIncr<MaxGrndTime):
                if NextDeparture+50 > AUS_G1+25:
                    NextArrivalTimeMid_T5 = NextDeparture + 50 
                    NextArrivalTimeMilitary_T5 = ConvertMidToMil(NextArrivalTimeMid_T5)
                    NextArrivalTimeMilitary_T5_Dest = NextArrivalTimeMilitary_T5 + 'AUS_G1'
                    return NextArrivalTimeMilitary_T5_Dest;  
                elif NextDeparture+65 > HOU_G1+35:
                    NextArrivalTimeMid_T5 = NextDeparture + 65 
                    NextArrivalTimeMilitary_T5 = ConvertMidToMil(NextArrivalTimeMid_T5)
                    NextArrivalTimeMilitary_T5_Dest = NextArrivalTimeMilitary_T5 + 'HOU_G1'
                    return NextArrivalTimeMilitary_T5_Dest;  
                elif NextDeparture+65 > HOU_G2+35:
                    NextArrivalTimeMid_T5 = NextDeparture + 65 
                    NextArrivalTimeMilitary_T5 = ConvertMidToMil(NextArrivalTimeMid_T5)
                    NextArrivalTimeMilitary_T5_Dest = NextArrivalTimeMilitary_T5 + 'HOU_G2'
                    return NextArrivalTimeMilitary_T5_Dest;  
                elif NextDeparture+65 > HOU_G3+35:
                    NextArrivalTimeMid_T5 = NextDeparture + 65 
                    NextArrivalTimeMilitary_T5 = ConvertMidToMil(NextArrivalTimeMid_T5)
                    NextArrivalTimeMilitary_T5_Dest = NextArrivalTimeMilitary_T5 + 'HOU_G3'
                    return NextArrivalTimeMilitary_T5_Dest;
                else:
                    NextDeparture = NextDeparture + 1
                    GrdTimeIncr = GrdTimeIncr + 1
        else:
            GrdTimeIncr = 1
            while(GrdTimeIncr<31):
                if NextDeparture+45 > AUS_G1+25:
                    NextArrivalTimeMid_T5 = NextDeparture + 45 
                    NextArrivalTimeMilitary_T5 = ConvertMidToMil(NextArrivalTimeMid_T5)
                    NextArrivalTimeMilitary_T5_Dest = NextArrivalTimeMilitary_T5 + 'AUS_G1'
                    return NextArrivalTimeMilitary_T5_Dest;  
                elif NextDeparture+65 > DAL_G1+30:
                    NextArrivalTimeMid_T5 = NextDeparture + 65 
                    NextArrivalTimeMilitary_T5 = ConvertMidToMil(NextArrivalTimeMid_T5)
                    NextArrivalTimeMilitary_T5_Dest = NextArrivalTimeMilitary_T5 + 'DAL_G1'
                    return NextArrivalTimeMilitary_T5_Dest;  
                elif NextDeparture+65 > DAL_G2+30:
                    NextArrivalTimeMid_T5 = NextDeparture + 65 
                    NextArrivalTimeMilitary_T5 = ConvertMidToMil(NextArrivalTimeMid_T5)
                    NextArrivalTimeMilitary_T5_Dest = NextArrivalTimeMilitary_T5 + 'DAL_G2'
                    return NextArrivalTimeMilitary_T5_Dest;
                else:
                    NextDeparture = NextDeparture + 1
                    GrdTimeIncr = GrdTimeIncr + 1
    else:
        if Origin[:1] == 'A':
            GrdTimeIncr = 1
            while(GrdTimeIncr<MaxGrndTime):
                if NextDeparture+45 > HOU_G3+35:
                    NextArrivalTimeMid_T6 = NextDeparture + 45 
                    NextArrivalTimeMilitary_T6 = ConvertMidToMil(NextArrivalTimeMid_T6)
                    NextArrivalTimeMilitary_T6_Dest = NextArrivalTimeMilitary_T6 + 'HOU_G3'
                    return NextArrivalTimeMilitary_T6_Dest;
                elif NextDeparture+45 > HOU_G1+35:
                    NextArrivalTimeMid_T6 = NextDeparture + 45 
                    NextArrivalTimeMilitary_T6 = ConvertMidToMil(NextArrivalTimeMid_T6)
                    NextArrivalTimeMilitary_T6_Dest = NextArrivalTimeMilitary_T6 + 'HOU_G1'
                    return NextArrivalTimeMilitary_T6_Dest;
                elif NextDeparture+45 > HOU_G2+35:
                    NextArrivalTimeMid_T6 = NextDeparture + 45 
                    NextArrivalTimeMilitary_T6 = ConvertMidToMil(NextArrivalTimeMid_T6)
                    NextArrivalTimeMilitary_T6_Dest = NextArrivalTimeMilitary_T6 + 'HOU_G2'
                    return NextArrivalTimeMilitary_T6_Dest; 
                elif NextDeparture+50 > DAL_G2+30:
                    NextArrivalTimeMid_T6 = NextDeparture + 50 
                    NextArrivalTimeMilitary_T6 = ConvertMidToMil(NextArrivalTimeMid_T6)
                    NextArrivalTimeMilitary_T6_Dest = NextArrivalTimeMilitary_T6 + 'DAL_G2'
                    return NextArrivalTimeMilitary_T6_Dest;
                elif NextDeparture+50 > DAL_G1+30:
                    NextArrivalTimeMid_T6 = NextDeparture + 50 
                    NextArrivalTimeMilitary_T6 = ConvertMidToMil(NextArrivalTimeMid_T6)
                    NextArrivalTimeMilitary_T6_Dest = NextArrivalTimeMilitary_T6 + 'DAL_G1'
                    return NextArrivalTimeMilitary_T6_Dest;
                else:
                    NextDeparture = NextDeparture + 1
                    GrdTimeIncr = GrdTimeIncr + 1
        elif Origin[:1] == 'D':
            GrdTimeIncr = 1
            while(GrdTimeIncr<MaxGrndTime):
                if NextDeparture+50 > AUS_G1+25:
                    NextArrivalTimeMid_T6 = NextDeparture + 50 
                    NextArrivalTimeMilitary_T6 = ConvertMidToMil(NextArrivalTimeMid_T6)
                    NextArrivalTimeMilitary_T6_Dest = NextArrivalTimeMilitary_T6 + 'AUS_G1'
                    return NextArrivalTimeMilitary_T6_Dest;  
                elif NextDeparture+65 > HOU_G1+35:
                    NextArrivalTimeMid_T6 = NextDeparture + 65 
                    NextArrivalTimeMilitary_T6 = ConvertMidToMil(NextArrivalTimeMid_T6)
                    NextArrivalTimeMilitary_T6_Dest = NextArrivalTimeMilitary_T6 + 'HOU_G1'
                    return NextArrivalTimeMilitary_T6_Dest;  
                elif NextDeparture+65 > HOU_G2+35:
                    NextArrivalTimeMid_T6 = NextDeparture + 65 
                    NextArrivalTimeMilitary_T6 = ConvertMidToMil(NextArrivalTimeMid_T6)
                    NextArrivalTimeMilitary_T6_Dest = NextArrivalTimeMilitary_T6 + 'HOU_G2'
                    return NextArrivalTimeMilitary_T6_Dest;  
                elif NextDeparture+65 > HOU_G3+35:
                    NextArrivalTimeMid_T6 = NextDeparture + 65 
                    NextArrivalTimeMilitary_T6 = ConvertMidToMil(NextArrivalTimeMid_T6)
                    NextArrivalTimeMilitary_T6_Dest = NextArrivalTimeMilitary_T6 + 'HOU_G3'
                    return NextArrivalTimeMilitary_T6_Dest;
                else:
                    NextDeparture = NextDeparture + 1
                    GrdTimeIncr = GrdTimeIncr + 1
        else:
            GrdTimeIncr = 1
            while(GrdTimeIncr<31):
                if NextDeparture+45 > AUS_G1+25:
                    NextArrivalTimeMid_T6 = NextDeparture + 45 
                    NextArrivalTimeMilitary_T6 = ConvertMidToMil(NextArrivalTimeMid_T6)
                    NextArrivalTimeMilitary_T6_Dest = NextArrivalTimeMilitary_T6 + 'AUS_G1'
                    return NextArrivalTimeMilitary_T6_Dest;  
                elif NextDeparture+65 > DAL_G1+30:
                    NextArrivalTimeMid_T6 = NextDeparture + 65 
                    NextArrivalTimeMilitary_T6 = ConvertMidToMil(NextArrivalTimeMid_T6)
                    NextArrivalTimeMilitary_T6_Dest = NextArrivalTimeMilitary_T6 + 'DAL_G1'
                    return NextArrivalTimeMilitary_T6_Dest;  
                elif NextDeparture+65 > DAL_G2+30:
                    NextArrivalTimeMid_T6 = NextDeparture + 65 
                    NextArrivalTimeMilitary_T6 = ConvertMidToMil(NextArrivalTimeMid_T6)
                    NextArrivalTimeMilitary_T6_Dest = NextArrivalTimeMilitary_T6 + 'DAL_G2'
                    return NextArrivalTimeMilitary_T6_Dest;
                else:
                    NextDeparture = NextDeparture + 1
                    GrdTimeIncr = GrdTimeIncr + 1


# In[740]:

# Function to find the Aiport using Gate-Aiport Mapping #

def Airport(Gate):
    GateMapping = {'DAL_G1':'DAL','DAL_G2':'DAL','HOU_G1':'HOU','HOU_G2':'HOU','HOU_G3':'HOU','AUS_G1':'AUS'}
    if Gate[:3]=='AUS':
        Airport=GateMapping[Gate]
        return Airport;
    if Gate[:3]=='HOU':
        Airport=GateMapping[Gate]
        return Airport;
    if Gate[:3]=='DAL':
        Airport=GateMapping[Gate]
        return Airport;


# In[741]:

# Function to increment the Departure Time #

def IncrementDeparture(Origin, Destination, NextArrival):
    NextArrival = int(NextArrival)
    NextArrival = ConvertMilToMid (NextArrival)
    if((Origin=='HOU' and Destination=='AUS')or(Origin=='AUS' and Destination=='HOU')):
        NextDeparture = NextArrival - SourceDestination[Origin[:3]+' '+Destination]
        NextDeparture = ConvertMidToMil(NextDeparture)
        return NextDeparture;
    elif((Origin=='DAL' and Destination=='AUS')or(Origin=='AUS' and Destination=='DAL')):
        NextDeparture = NextArrival - SourceDestination[Origin[:3]+' '+Destination]
        NextDeparture = ConvertMidToMil(NextDeparture)
        return NextDeparture;
    elif((Origin=='DAL' and Destination=='HOU')or(Origin=='HOU' and Destination=='DAL')):
        NextDeparture = NextArrival - SourceDestination[Origin[:3]+' '+Destination]
        NextDeparture = ConvertMidToMil(NextDeparture)
        return NextDeparture;


# In[742]:

# Function to create the flight_schedule.csv #

def PrintFlightSchedule(fn, csv_hdr, flt_sched): 
    with open(fn,'wt') as f:
        print(csv_hdr, file=f) 
        for s in flt_sched:
            print(','.join(s), file=f)


# In[743]:

# Main program to print the Schedule #

while (Cycle<11):
    for T in Tail_Number:
        if T == 'T1':
            ArrivvalNowMid_T1 = ConvertMilToMid (ArrivalNow_T1)
            NextDepartureTimeMid_T1 = NextDeptTime(T, ArrivvalNowMid_T1, Dest_T1)
            NextDepartureTime_T1 = ConvertMidToMil(NextDepartureTimeMid_T1)
            Ori_T1 = Dest_T1
            NextArrivalTimeMilitary_T1_Dest = NextArrivalTimeDest (T, AUS_G1, DAL_G1, DAL_G2, HOU_G1, HOU_G2, HOU_G3, NextDepartureTime_T1, Ori_T1)
            NextArrivalTimeMilitary_T1 = NextArrivalTimeMilitary_T1_Dest[0:4]
            UpdatedDestination_T1 = NextArrivalTimeMilitary_T1_Dest[4:]
            Dest_T1 = UpdatedDestination_T1
            ArrivalNow_T1 = int(NextArrivalTimeMilitary_T1)
            if UpdatedDestination_T1 == 'AUS_G1':
                AUS_G1 = int(NextArrivalTimeMilitary_T1)
            elif UpdatedDestination_T1 == 'DAL_G1':
                DAL_G1 = int(NextArrivalTimeMilitary_T1)
            elif UpdatedDestination_T1 == 'DAL_G2':
                DAL_G2 = int(NextArrivalTimeMilitary_T1)
            elif UpdatedDestination_T1 == 'HOU_G1':
                HOU_G1 = int(NextArrivalTimeMilitary_T1)
            elif UpdatedDestination_T1 == 'HOU_G2':
                HOU_G2 = int(NextArrivalTimeMilitary_T1)
            else:
                HOU_G3 = int(NextArrivalTimeMilitary_T1)
            Origin_T1 = Airport(Ori_T1)
            Destination_T1 = Airport(Dest_T1)
            NextDepartureTime_T1 = IncrementDeparture(Origin_T1, Destination_T1, NextArrivalTimeMilitary_T1)
            Schedule_T1 = [T, Origin_T1, Destination_T1, NextDepartureTime_T1, NextArrivalTimeMilitary_T1]
        elif T == 'T2':
            ArrivvalNowMid_T2 = ConvertMilToMid (ArrivalNow_T2)
            NextDepartureTimeMid_T2 = NextDeptTime(T, ArrivvalNowMid_T2, Dest_T2)
            NextDepartureTime_T2 = ConvertMidToMil(NextDepartureTimeMid_T2)
            Ori_T2 = Dest_T2
            NextArrivalTimeMilitary_T2_Dest = NextArrivalTimeDest (T, AUS_G1, DAL_G1, DAL_G2, HOU_G1, HOU_G2, HOU_G3, NextDepartureTime_T2, Ori_T2)
            NextArrivalTimeMilitary_T2 = NextArrivalTimeMilitary_T2_Dest[0:4]
            UpdatedDestination_T2 = NextArrivalTimeMilitary_T2_Dest[4:]
            Dest_T2 = UpdatedDestination_T2
            ArrivalNow_T2 = int(NextArrivalTimeMilitary_T2)
            if UpdatedDestination_T2 == 'AUS_G1':
                AUS_G1 = int(NextArrivalTimeMilitary_T2)
            elif UpdatedDestination_T2 == 'DAL_G1':
                DAL_G1 = int(NextArrivalTimeMilitary_T2)
            elif UpdatedDestination_T2 == 'DAL_G2':
                DAL_G2 = int(NextArrivalTimeMilitary_T2)
            elif UpdatedDestination_T2 == 'HOU_G1':
                HOU_G1 = int(NextArrivalTimeMilitary_T2)
            elif UpdatedDestination_T2 == 'HOU_G2':
                HOU_G2 = int(NextArrivalTimeMilitary_T2)
            else:
                HOU_G3 = int(NextArrivalTimeMilitary_T2)
            Origin_T2 = Airport(Ori_T2)
            Destination_T2 = Airport(Dest_T2)
            NextDepartureTime_T2 = IncrementDeparture(Origin_T2, Destination_T2, NextArrivalTimeMilitary_T2)
            Schedule_T2 = [T, Origin_T2, Destination_T2, NextDepartureTime_T2, NextArrivalTimeMilitary_T2]
        elif T == 'T3':
            ArrivvalNowMid_T3 = ConvertMilToMid (ArrivalNow_T3)
            NextDepartureTimeMid_T3 = NextDeptTime(T, ArrivvalNowMid_T3, Dest_T3)
            NextDepartureTime_T3 = ConvertMidToMil(NextDepartureTimeMid_T3)
            Ori_T3 = Dest_T3
            NextArrivalTimeMilitary_T3_Dest = NextArrivalTimeDest (T, AUS_G1, DAL_G1, DAL_G2, HOU_G1, HOU_G2, HOU_G3, NextDepartureTime_T3, Ori_T3)
            NextArrivalTimeMilitary_T3 = NextArrivalTimeMilitary_T3_Dest[0:4]
            UpdatedDestination_T3 = NextArrivalTimeMilitary_T3_Dest[4:]
            Dest_T3 = UpdatedDestination_T3
            ArrivalNow_T3 = int(NextArrivalTimeMilitary_T3)
            if UpdatedDestination_T3 == 'AUS_G1':
                AUS_G1 = int(NextArrivalTimeMilitary_T3)
            elif UpdatedDestination_T3 == 'DAL_G1':
                DAL_G1 = int(NextArrivalTimeMilitary_T3)
            elif UpdatedDestination_T3 == 'DAL_G2':
                DAL_G2 = int(NextArrivalTimeMilitary_T3)
            elif UpdatedDestination_T3 == 'HOU_G1':
                HOU_G1 = int(NextArrivalTimeMilitary_T3)
            elif UpdatedDestination_T3 == 'HOU_G2':
                HOU_G2 = int(NextArrivalTimeMilitary_T3)
            else:
                HOU_G3 = int(NextArrivalTimeMilitary_T3)
            Origin_T3 = Airport(Ori_T3)
            Destination_T3 = Airport(Dest_T3)
            NextDepartureTime_T3 = IncrementDeparture(Origin_T3, Destination_T3, NextArrivalTimeMilitary_T3)
            Schedule_T3 = [T, Origin_T3, Destination_T3, NextDepartureTime_T3, NextArrivalTimeMilitary_T3]
        elif T == 'T4':
            ArrivvalNowMid_T4 = ConvertMilToMid (ArrivalNow_T4)
            NextDepartureTimeMid_T4 = NextDeptTime(T, ArrivvalNowMid_T4, Dest_T4)
            NextDepartureTime_T4 = ConvertMidToMil(NextDepartureTimeMid_T4)
            Ori_T4 = Dest_T4
            NextArrivalTimeMilitary_T4_Dest = NextArrivalTimeDest (T, AUS_G1, DAL_G1, DAL_G2, HOU_G1, HOU_G2, HOU_G3, NextDepartureTime_T4, Ori_T4)
            NextArrivalTimeMilitary_T4 = NextArrivalTimeMilitary_T4_Dest[0:4]
            UpdatedDestination_T4 = NextArrivalTimeMilitary_T4_Dest[4:]
            Dest_T4 = UpdatedDestination_T4
            ArrivalNow_T4 = int(NextArrivalTimeMilitary_T4)
            if UpdatedDestination_T4 == 'AUS_G1':
                AUS_G1 = int(NextArrivalTimeMilitary_T4)
            elif UpdatedDestination_T4 == 'DAL_G1':
                DAL_G1 = int(NextArrivalTimeMilitary_T4)
            elif UpdatedDestination_T4 == 'DAL_G2':
                DAL_G2 = int(NextArrivalTimeMilitary_T4)
            elif UpdatedDestination_T4 == 'HOU_G1':
                HOU_G1 = int(NextArrivalTimeMilitary_T4)
            elif UpdatedDestination_T4 == 'HOU_G2':
                HOU_G2 = int(NextArrivalTimeMilitary_T4)
            else:
                HOU_G3 = int(NextArrivalTimeMilitary_T4)
            Origin_T4 = Airport(Ori_T4)
            Destination_T4 = Airport(Dest_T4)
            NextDepartureTime_T4 = IncrementDeparture(Origin_T4, Destination_T4, NextArrivalTimeMilitary_T4)
            Schedule_T4 = [T, Origin_T4, Destination_T4, NextDepartureTime_T4, NextArrivalTimeMilitary_T4]
        elif T == 'T5':
            ArrivvalNowMid_T5 = ConvertMilToMid (ArrivalNow_T5)
            NextDepartureTimeMid_T5 = NextDeptTime(T, ArrivvalNowMid_T5, Dest_T5)
            NextDepartureTime_T5 = ConvertMidToMil(NextDepartureTimeMid_T5)
            Ori_T5 = Dest_T5
            NextArrivalTimeMilitary_T5_Dest = NextArrivalTimeDest (T, AUS_G1, DAL_G1, DAL_G2, HOU_G1, HOU_G2, HOU_G3, NextDepartureTime_T5, Ori_T5)
            NextArrivalTimeMilitary_T5 = NextArrivalTimeMilitary_T5_Dest[0:4]
            UpdatedDestination_T5 = NextArrivalTimeMilitary_T5_Dest[4:]
            Dest_T5 = UpdatedDestination_T5
            ArrivalNow_T5 = int(NextArrivalTimeMilitary_T5)
            if UpdatedDestination_T5 == 'AUS_G1':
                AUS_G1 = int(NextArrivalTimeMilitary_T5)
            elif UpdatedDestination_T5 == 'DAL_G1':
                DAL_G1 = int(NextArrivalTimeMilitary_T5)
            elif UpdatedDestination_T5 == 'DAL_G2':
                DAL_G2 = int(NextArrivalTimeMilitary_T5)
            elif UpdatedDestination_T5 == 'HOU_G1':
                HOU_G1 = int(NextArrivalTimeMilitary_T5)
            elif UpdatedDestination_T5 == 'HOU_G2':
                HOU_G2 = int(NextArrivalTimeMilitary_T5)
            else:
                HOU_G3 = int(NextArrivalTimeMilitary_T5)
            Origin_T5 = Airport(Ori_T5)
            Destination_T5 = Airport(Dest_T5)
            NextDepartureTime_T5 = IncrementDeparture(Origin_T5, Destination_T5, NextArrivalTimeMilitary_T5)
            Schedule_T5 = [T, Origin_T5, Destination_T5, NextDepartureTime_T5, NextArrivalTimeMilitary_T5]
        else:
            ArrivvalNowMid_T6 = ConvertMilToMid (ArrivalNow_T6)
            NextDepartureTimeMid_T6 = NextDeptTime(T, ArrivvalNowMid_T6, Dest_T6)
            NextDepartureTime_T6 = ConvertMidToMil(NextDepartureTimeMid_T6)
            Ori_T6 = Dest_T6
            NextArrivalTimeMilitary_T6_Dest = NextArrivalTimeDest (T, AUS_G1, DAL_G1, DAL_G2, HOU_G1, HOU_G2, HOU_G3, NextDepartureTime_T6, Ori_T6)
            NextArrivalTimeMilitary_T6 = NextArrivalTimeMilitary_T6_Dest[0:4]
            UpdatedDestination_T6 = NextArrivalTimeMilitary_T6_Dest[4:]
            Dest_T6 = UpdatedDestination_T6
            ArrivalNow_T6 = int(NextArrivalTimeMilitary_T6)
            if UpdatedDestination_T6 == 'AUS_G1':
                AUS_G1 = int(NextArrivalTimeMilitary_T6)
            elif UpdatedDestination_T6 == 'DAL_G1':
                DAL_G1 = int(NextArrivalTimeMilitary_T6)
            elif UpdatedDestination_T6 == 'DAL_G2':
                DAL_G2 = int(NextArrivalTimeMilitary_T6)
            elif UpdatedDestination_T6 == 'HOU_G1':
                HOU_G1 = int(NextArrivalTimeMilitary_T6)
            elif UpdatedDestination_T6 == 'HOU_G2':
                HOU_G2 = int(NextArrivalTimeMilitary_T6)
            else:
                HOU_G3 = int(NextArrivalTimeMilitary_T6)
            Origin_T6 = Airport(Ori_T6)
            Destination_T6 = Airport(Dest_T6)
            NextDepartureTime_T6 = IncrementDeparture(Origin_T6, Destination_T6, NextArrivalTimeMilitary_T6)
            Schedule_T6 = [T, Origin_T6, Destination_T6, NextDepartureTime_T6, NextArrivalTimeMilitary_T6]
    Cycle = Cycle + 1
    Schedule = [Schedule_T1, Schedule_T2, Schedule_T3, Schedule_T4, Schedule_T5, Schedule_T6]
    Flight_Schedule = Flight_Schedule + Schedule
    print(Flight_Schedule)
    csv_header = 'tail_number,origin,destination,departure_time,arrival_time'
    file_name = 'flight_schedule.csv'
    Flight_Schedule = sorted(Flight_Schedule, key = lambda x: x[0] + x[3])
    PrintFlightSchedule(file_name, csv_header, Flight_Schedule)

