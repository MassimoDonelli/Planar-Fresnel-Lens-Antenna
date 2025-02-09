# -*- coding: utf-8 -*-
# .. Massimo Donelli, January 2025, V1.0 ..
# .. Import Library ..
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.patches import Rectangle 
# .. Define functions .. 
def InsertData():
#
    print("Do you need a reflector or a lens (R/L):")
    ReflectorLens=str(input("R or L:"))
    print(ReflectorLens)
    if(ReflectorLens == "R"):
        print("Insert the kind of geometry you need (M,MB,DC,DV,G):")
        print("M - Reflector - annular metallic reflector ")
        print("MB - Reflector - annular metallic reflector plus metallic background")
        print("DC - Lens dielectric of constant thickness variable eps")
        print("DG - Lens dielectric of constant eps value conical teeth")
        print("DGr - Lens dielectric of constant eps value grooved structure teeth")
    elif(ReflectorLens == "L"):  
        print("M - Reflector - annular metallic lens ")
        print("DC - Lens dielectric of constant thickness variable eps")
        print("DG - Lens dielectric of constant eps value conical theet")
        print("DGr - Lens dielectric of constant eps value grooved structure teeth")
    else:
        print("Error Wrong choice!")
        exit(0)    
    Geometry=str(input("Which Geometry?:"))
    print(Geometry)
    Frequency=input('Frequency of the Electromagnetic Wave [Hz]:')
    print(Frequency)
    Focal=input('Focal lenght [m]:')
    print(Focal)
    CorrectionPhase=int(input('Correction Phase [even number]:'))
    print(CorrectionPhase)
    W=int(input("Number of full-waves circular zones:"))
    print(W)
    return [Geometry,ReflectorLens,float(Frequency),float(Focal),int(CorrectionPhase),int(W)]
# .. Input ..
# .. Lambda = wavelenght of the EM waves ..
# .. P = PhaseCorrectionFactor always even P=2 half-wavelenght correcting, 
# ..     P=4 quarte-wavelenght correcting
# .. F = Focal lenght of the lens ..
# .. W = Number of full-waves circular zones ..
def FresnelZone(Lambda, P, F, W, FlagVisualization):
    OuterRadius = []
    for I_X_FOR in range(0,(P*W)+1,1):
        Rw = pow((((2*I_X_FOR*F*Lambda)/P) + pow(((I_X_FOR*Lambda)/P),2)),0.5)
        OuterRadius.append(Rw)
    if(FlagVisualization == 1):
        # .. Create a figure panel ..
        fig, ax = plt.subplots()
        # .. Add annular Fresnel zone ..  
        for I_X_FOR in range(P*W,0,-1): 
            if I_X_FOR % 2 ==0: 
                CircleColor = 'white'
            else:
                CircleColor = 'black'
            circle = plt.Circle((0,0),OuterRadius[I_X_FOR],fill=True,color=CircleColor)
            # .. Add Circle .. 
            ax.add_patch(circle)
        # .. Add Last Circle ..
        CircleColor = 'black'    
        circle = plt.Circle((0,0),OuterRadius[P*W],fill=False,color=CircleColor)
        ax.add_patch(circle)    
        # .. Set the figure axis ..
        ax.set_xlim(-max(OuterRadius),max(OuterRadius))
        ax.set_ylim(-max(OuterRadius),max(OuterRadius))
        plt.title('Fresnel Zone')
        plt.axis('equal')
        plt.show()
    return(OuterRadius)    
# .. Estimates the EPS of each fresnel zone ..
def EpsFresnelZone(Lambda, EpsMax, LensThickness,P, W):
    EpsFresnel = []
    EpsPrev = 1.0
    EpsFresnel.append(EpsPrev)
    EpsFresnel.append(EpsMax)
    EpsPrev = EpsMax
    for I_X_FOR in range(2,W*P,1):
        DummyEps = (Lambda/(LensThickness*P))+pow(EpsPrev,0.5)
        EpsFresnel.append(round(DummyEps,2))
        EpsPrev = DummyEps
    print(EpsFresnel)   
    print("Thickness:",Lambda/(P*(pow(EpsMax,0.5)-1.0)) ) 
    return(EpsFresnel)    
# .. This Function create a dielectric lens of fixed Thickness and different dielectric permottivity EPS .. 
# .. It is based on the following work: "3D Printed Dielectric Fresnel Lens" by Shiyu Zhang 
def FresnelLensCostantThickness(Lambda, P, F, W, EpsMax, LensThickness, FlagVisualization):
    #ColorNames = list(mcolors.TABLEAU_COLORS)
    ColorNames = list(mcolors.CSS4_COLORS)
    IndexColour = 0
    OuterRadius = FresnelZone(Lambda, P, F, W, 0)
    Eps = EpsFresnelZone(Lambda, EpsMax, LensThickness,P,W)
    print("Radius:",OuterRadius)
    print("Eps:",Eps)
    if(FlagVisualization == 1):
        # .. Create a figure panel ..
        fig, ax = plt.subplots()
        # .. Add annular Fresnel zone .. 
        for I_X_FOR in range(W*P,0,-1):
            circle = plt.Circle((0,0),OuterRadius[I_X_FOR],fill=True,color=ColorNames[IndexColour])
            # .. Add Text ..
            ax.text(-max(OuterRadius)*1.5,max(OuterRadius)+0.0015-(I_X_FOR*0.008),'Eps= '+ str(Eps[I_X_FOR-1]) ,fontsize = 10, horizontalalignment='left',verticalalignment='center')
            # .. Add Rectangle ..
            ax.add_patch(
                Rectangle(xy=(-max(OuterRadius)*1.7,max(OuterRadius)-(I_X_FOR*0.008)), width=0.01,height=0.005,color=ColorNames[IndexColour])
            ) 
            # .. Add Circle .. 
            ax.add_patch(circle)
            IndexColour += 1
        # .. Set the figure axis ..
        ax.set_xlim(-max(OuterRadius),max(OuterRadius))
        ax.set_ylim(-max(OuterRadius),max(OuterRadius))
        plt.title('Fresnel Zone')
        plt.axis('equal')
        plt.show()
    return(OuterRadius)  
# .. This Function create a dielectric lens of fixed dielectric permottivity EPS e conical profiles .. 
# .. It is based on the following work: " A 3D printed all dielectric Fresnel zone plate lens with high gain characteristic at the X-band," by Chen Wang, Wei-sheng Yu, Yan-fang Liu, Lin Peng
def FresnelLensCostantEpsConical(Lambda, P, F, W, EpsMax, FlagVisualization, FlagReflector):  
    # .. Support thickness lambda/4 ..
    SupportThickness = Lambda/4
    # .. Conical theet height ..
    TheetHeigh = Lambda/(2*pow(EpsMax,0.5)-1)
    # .. Estimates the Freasnel Zone .. 
    OuterRadius = FresnelZone(Lambda, P, F, W, 0)
    if(FlagVisualization == 1):
        TheetColor = 'blue'
        GroundColor = 'red'
        # .. Create a figure panel ..
        fig, ax = plt.subplots()
        # .. Add annular Fresnel zone ..  
        for I_X_FOR in range(W*P,0,-1): 
            if I_X_FOR % 2 ==0: 
                CircleColor = 'white'
            else:
                CircleColor = 'blue'
            circle = plt.Circle((0,0),OuterRadius[I_X_FOR],fill=True,color=CircleColor)
             # .. Add Circle .. 
            ax.add_patch(circle)  
        # .. Add Last Circle ..
        CircleColor = 'black'   
        OffsetY = -max(OuterRadius)-2*SupportThickness - TheetHeigh
        OffsetYT = -max(OuterRadius)-SupportThickness - TheetHeigh
        circle = plt.Circle((0,0),OuterRadius[W*P],fill=False,color=CircleColor)
        ax.add_patch(circle)    
        # .. Add Lens Substrate ..
        ax.add_patch(
                Rectangle(xy=(-max(OuterRadius),OffsetY), width= max(OuterRadius)*2,height=SupportThickness,color=TheetColor)
           )
        # .. Add Theet to lens ..
        if (W*P) % 2 ==0: 
            IndexFresnel = len(OuterRadius)-2
        else:
            IndexFresnel = len(OuterRadius)
        for I_X_FOR in range(IndexFresnel): 
            if I_X_FOR % 2 == 0: 
                FresnelRadius = OuterRadius[I_X_FOR]
                if(FresnelRadius == 0.0):
                    FresnelRadius=OuterRadius[I_X_FOR+1]
                    plt.fill((-FresnelRadius,FresnelRadius,0,-FresnelRadius),(OffsetYT,OffsetYT,TheetHeigh+OffsetYT,OffsetYT),color=TheetColor)
                else:            
                    FresnelRadius=OuterRadius[I_X_FOR]
                    plt.plot((FresnelRadius,FresnelRadius,OuterRadius[I_X_FOR+1],FresnelRadius),(OffsetYT,TheetHeigh+OffsetYT,OffsetYT,OffsetYT),color=TheetColor)
                    plt.fill((FresnelRadius,FresnelRadius,OuterRadius[I_X_FOR+1],FresnelRadius),(OffsetYT,TheetHeigh+OffsetYT,OffsetYT,OffsetYT),color=TheetColor)
                    # .. Simmetric lens side ..
                    plt.plot((-FresnelRadius,-FresnelRadius,-OuterRadius[I_X_FOR+1],-FresnelRadius),(OffsetYT,TheetHeigh+OffsetYT,OffsetYT,OffsetYT),color=TheetColor)
                    plt.fill((-FresnelRadius,-FresnelRadius,-OuterRadius[I_X_FOR+1],-FresnelRadius),(OffsetYT,TheetHeigh+OffsetYT,OffsetYT,OffsetYT),color=TheetColor)
                    # 
        # .. Add Text ..
        ax.text(-max(OuterRadius)*1.5,max(OuterRadius),'Dielectric' ,fontsize = 10, horizontalalignment='left',verticalalignment='center')
        # .. Add Rectangle ..
        ax.add_patch(
                Rectangle(xy=(-max(OuterRadius)*1.7,max(OuterRadius)), width=0.01,height=0.005,color=TheetColor)
            )            
        if(FlagReflector == 1):  
            # .. Add Metallic Groundplane ..
            ax.add_patch(
                Rectangle(xy=(-max(OuterRadius),OffsetY-SupportThickness/3), width= max(OuterRadius)*2,height=SupportThickness/3,color=GroundColor)
            )
            # .. Add Text ..
            ax.text(-max(OuterRadius)*1.5,max(OuterRadius)-0.01,'Metallic Ground' ,fontsize = 10, horizontalalignment='left',verticalalignment='center')
            # .. Add Rectangle ..
            ax.add_patch(
                Rectangle(xy=(-max(OuterRadius)*1.7,max(OuterRadius)-0.01), width=0.01,height=0.005,color=GroundColor)
            ) 
        # .. Set the figure axis ..
        ax.set_xlim(-max(OuterRadius),max(OuterRadius))
        ax.set_ylim(-max(OuterRadius),max(OuterRadius))
        plt.title('Fresnel Zone')
        plt.axis('equal')
        plt.show()
    return(OuterRadius,TheetHeigh)
# .. This Function create a dielectric lens/reflector of fixed dielectric permottivity EPS and grooved profiles  .. 
# .. It is based on the following work: "Fresnel Zone Plate and Ordinary Lens Antennas: Comparative Study at Microwave and Terahertz Frequencies"
# .. by J.M. Rodríguez, Hristo D. Hristov and Walter Grote
def FresnelLensGrooved(Lambda, P, F, W, EpsMax, FlagVisualization, FlagReflector):
    TotalZones = P*W
    #
    OuterRadius = []
    StepHeigh = []
    for I_X_FOR in range(0,TotalZones+1,1):
        Rw = pow((((2*I_X_FOR*F*Lambda)/P) + pow(((I_X_FOR*Lambda)/P),2)),1/2)
        OuterRadius.append(Rw)
    # .. Estimates the heigh of single step ..
    QuarterWavelength = (Lambda*pow(EpsMax,0.5))/4
    SingleStepHeigh = (Lambda*pow(EpsMax,0.5))/(P*(pow(EpsMax,0.5)-1))
    MaxHeigh    =  SingleStepHeigh*(P-1)
    if(FlagVisualization == 1):
        # .. Create a figure panel ..
        fig, ax = plt.subplots()
        # .. Add annular Fresnel zone ..  
        for I_X_FOR in range(TotalZones,0,-1): 
            if I_X_FOR % 2 ==0: 
                CircleColor = 'white'
            else:
                CircleColor = 'blue'
            circle = plt.Circle((0,0),OuterRadius[I_X_FOR],fill=True,color=CircleColor)
            # .. Add Circle .. 
            ax.add_patch(circle)
        # .. Add Last Circle ..
        CircleColor = 'blue'    
        circle = plt.Circle((0,0),OuterRadius[TotalZones],fill=False,color=CircleColor)
        ax.add_patch(circle)    
        StepHeigh = MaxHeigh
        J_X_FOR = 0
        for I_X_FOR in range(TotalZones):
        # .. Add Rectangle ..
            ax.add_patch(
                    Rectangle(xy=(-OuterRadius[I_X_FOR],-max(OuterRadius)*2), width=OuterRadius[I_X_FOR]-OuterRadius[I_X_FOR+1],height=StepHeigh,color='blue')
                    )
            ax.add_patch(
                    Rectangle(xy=(OuterRadius[I_X_FOR],-max(OuterRadius)*2), width=-OuterRadius[I_X_FOR]+OuterRadius[I_X_FOR+1],height=StepHeigh,color='blue')
                    )
            J_X_FOR += 1  
            StepHeigh = MaxHeigh - SingleStepHeigh*J_X_FOR
            if(J_X_FOR > P-1): 
                StepHeigh = MaxHeigh
                J_X_FOR = 0
        if(FlagReflector == 1):
            # .. Add Quarterwavelenght Background Rectangle ..
            ax.add_patch(
                    Rectangle(xy=(-max(OuterRadius),-max(OuterRadius)*2), width=max(OuterRadius)*2,height=-QuarterWavelength,color='blue')
                    )
            ax.add_patch(
                    Rectangle(xy=(-max(OuterRadius),-max(OuterRadius)*2-QuarterWavelength*(1+1/10)), width=max(OuterRadius)*2,height=-QuarterWavelength*(1/10),color='red')
                    )
        # .. Set the figure axis ..
        ax.set_xlim(-max(OuterRadius),max(OuterRadius))
        ax.set_ylim(-max(OuterRadius),max(OuterRadius))
        plt.title('Plane Fresnel Zone Grooved Lens')
        plt.axis('equal')
        plt.show()
    return(OuterRadius,StepHeigh)
#
# .. Main Program ..
if __name__ == '__main__':
    # .. Light velocity in vacuum ..
    C = 299792458
    FlagVisualization = 1
    print("__________________________________")
    print("Phase 1 Insert Data")
    Geometry,ReflectorLens,Frequency,Focal,CorrectionPhase,W = InsertData()
    print("End ...")
    print("__________________________________")
    print("Phase 2 Estimates the lens geometry")
    Lambda = C/Frequency
    print("Lambda [m]:",Lambda)
    #
    if (ReflectorLens == 'R'):
        if(Geometry == 'M'):
            print("You Choosed Annular metallic reflector strucure")
            print("Two foci at: +/-",Focal," [m]")
            print("Low efficient <40%")
            OuterRadius = FresnelZone(Lambda, CorrectionPhase, Focal, W, FlagVisualization)
            print("Radius:",OuterRadius)
            print("Diameter of Lens [m]:", OuterRadius[CorrectionPhase*W]*2)
            print("F/D:",Focal/(OuterRadius[CorrectionPhase*W]*2))
            print("End ...")
        elif(Geometry == 'MB'):
            print("You Choosed Annular metallic reflector strucure with background")
            print("The focus is at: +",Focal," [m]")
            print("Position of the metallic background P=",Lambda/4,"[m] ")
            print("Efficiency > 50%")
            OuterRadius = FresnelZone(Lambda, CorrectionPhase, Focal, W, FlagVisualization)
            print("Radius:",OuterRadius)
            print("Diameter of Lens [m]:", OuterRadius[CorrectionPhase*W]*2)
            print("F/D:",Focal/(OuterRadius[CorrectionPhase*W]*2))
            print("End ...")
        elif(Geometry == 'DC'):
            print("You Choosed Lens dielectric of constant thickness variable eps reflector strucure with background")
            LensThickness = input('Thickness of the lens [m]:')
            print(LensThickness)
            EpsMax = input('Eps max of the considered material:')
            print(EpsMax)
            OuterRadius = FresnelLensCostantThickness(Lambda, CorrectionPhase, Focal, W, float(EpsMax), float(LensThickness),FlagVisualization)
            print("The focus is at: +",Focal," [m]")
            print("Position of the metallic background P=",(Lambda*pow(EpsMax,0.5))/4,"[m] ")
            print("Efficiency > 50%")
            print("Radius:",OuterRadius)
            print("Diameter of Lens [m]:", OuterRadius[CorrectionPhase*W]*2)
            print("F/D:",Focal/(OuterRadius[CorrectionPhase*W]*2))
            print("End ...")
        elif(Geometry == 'DG'):
            print("You Choosed Lens dielectric of constant eps, conical theet, reflector strucure with background")
            FlagReflector = 1
            EpsMax = float(input('Eps max of the considered material:'))
            print(EpsMax)
            OuterRadius,TheetHeigh = FresnelLensCostantEpsConical(Lambda, CorrectionPhase,Focal, W, EpsMax, FlagVisualization, FlagReflector)
            print("The focus is at: +",Focal," [m]")
            print("The heigh of conical dielectric theet is: ",TheetHeigh," [m]")
            print("Lens substrate thickness = ",Lambda/4,"[m] ")
            print("Position of the metallic background P = ",(Lambda*pow(EpsMax,0.5))/4,"[m] ")
            print("Efficiency > 50%")
            print("Radius:",OuterRadius)
            print("Diameter of Lens [m]:", OuterRadius[CorrectionPhase*W]*2)
            print("F/D:",Focal/(OuterRadius[CorrectionPhase*W]*2))
            print("End ...")
        elif(Geometry == 'DGr'):
            print("You Choosed Lens dielectric of constant eps, grooved structure, reflector strucure with background")
            FlagReflector = 1
            EpsMax = float(input('Eps of the considered material:'))
            print(EpsMax)
            OuterRadius,TheetHeigh = FresnelLensGrooved(Lambda, CorrectionPhase, Focal, W, EpsMax, FlagVisualization, FlagReflector)
            print("The focus is at: +",Focal," [m]")
            print("The heigh of grooved dielectric theet is: ",TheetHeigh," [m]")
            print("Lens substrate thickness = ",(Lambda*pow(EpsMax,0.5))/4,"[m] ")
            print("Position of the metallic background P = ",(Lambda*pow(EpsMax,0.5))/4,"[m] ")
            print("Efficiency > 50%")
            print("Radius:",OuterRadius)
            print("Diameter of Lens [m]:", OuterRadius[CorrectionPhase*W]*2)
            print("F/D:",Focal/(OuterRadius[CorrectionPhase*W]*2))
            print("End ...")
    elif(ReflectorLens == 'L'):
        if(Geometry == 'M'):
            print("You Choosed Annular metallic lens strucure")
            print("Two foci at: +/-",Focal," [m]")
            print("Low efficient <40%")
            OuterRadius = FresnelZone(Lambda, CorrectionPhase, Focal, W, FlagVisualization)
            print("Radius:",OuterRadius)
            print("Diameter of Lens [m]:", OuterRadius[CorrectionPhase*W]*2)
            print("F/D: ",Focal/(OuterRadius[CorrectionPhase*W]*2))
            print("End ...")
        elif(Geometry == 'DC'):
            print("You Choosed Lens dielectric of constant thickness variable eps lens strucure")
            LensThickness = input('Thickness of the lens [m]:')
            EpsMax = input('Eps max of the considered material:')
            OuterRadius = FresnelLensCostantThickness(Lambda, CorrectionPhase, Focal, W, float(EpsMax), float(LensThickness),FlagVisualization)
            print("The focus is at: +",Focal," [m]")
            print("Efficiency > 50%")
            print("Fresnel Zone Radius:",OuterRadius)
            print("Diameter of Lens [m]:", OuterRadius[CorrectionPhase*W]*2)
            print("F/D:",Focal/(OuterRadius[CorrectionPhase*W]*2))
            print("End ...")
        elif(Geometry == 'DG'):
            print("You Choosed Lens dielectric of constant eps, conical theet")
            FlagReflector = 0
            EpsMax = float(input('Eps max of the considered material:'))
            OuterRadius,TheetHeigh = FresnelLensCostantEpsConical(Lambda, CorrectionPhase, Focal, W, EpsMax, FlagVisualization, FlagReflector)
            print("The focus is at: +",Focal," [m]")
            print("The heigh of conical dielectric theet is: ",TheetHeigh," [m]")
            print("Lens substrate thickness = ",Lambda/4,"[m] ")
            print("Efficiency < 50%")
            print("Radius:",OuterRadius)
            print("Diameter of Lens [m]:", OuterRadius[CorrectionPhase*W]*2)
            print("F/D:",Focal/(OuterRadius[CorrectionPhase*W]*2))
            print("End ...")
        elif(Geometry == 'DGr'):
            print("You Choosed Lens dielectric of constant eps, grooved structure")
            FlagReflector = 0
            EpsMax = float(input('Eps of the considered material:'))
            print(EpsMax)
            OuterRadius,TheetHeigh = FresnelLensGrooved(Lambda, CorrectionPhase, Focal, W, EpsMax, FlagVisualization, FlagReflector)
            print("The focus is at: +",Focal," [m]")
            print("The heigh of grooved dielectric theet is: ",TheetHeigh," [m]")
            print("Lens substrate thickness = ",Lambda/4,"[m] ")
            print("Position of the metallic background P = ",Lambda/4,"[m] ")
            print("Efficiency > 50%")
            print("Radius:",OuterRadius)
            print("Diameter of Lens [m]:", OuterRadius[CorrectionPhase*W]*2)
            print("F/D:",Focal/(OuterRadius[CorrectionPhase*W]*2))
            print("End ...")    

    