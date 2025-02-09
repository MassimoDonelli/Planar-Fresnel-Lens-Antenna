# About the project
FresnelLenses.py is a tool that permits the design of a Planar Fresnel Lenses Antenna. The code is written in python3.


The tool permits the design of the following lenses/reflectors antennas:
 -------------------------------------------------------------
Antenna Lens Reflectors geometries:
M   - Annular metallic reflector antenna
MB  - Annular metallic reflector antenna plus metallic background
DC  - Reflector Lens dielectric of constant thickness variable eps"
DG  - Reflector Lens dielectric of constant eps value conical teeth"
DGr - Reflector Lens dielectric of constant eps value grooved structure teeth

Antenna Lens geometries:
M   - Annular metallic lens antenna
DC  - Lens dielectric of constant thickness variable eps
DG  - Lens dielectric of constant eps value conical teeth
DGr - Lens dielectric of constant eps value grooved structure teeth

Usage: python3 Source/FresnelLenses.py < Examples/InputReflectorAnnular.txt

Output example:
__________________________________
Phase 1 Insert Data
Do you need a reflector or a lens (R/L):
R or L:R
Insert the kind of geometry you need (M,MB,DC,DV,G):
M - Reflector - annular metallic reflector 
MB - Reflector - annular metallic reflector plus metallic background
DC - Lens dielectric of constant thickness variable eps
DG - Lens dielectric of constant eps value conical teeth
DGr - Lens dielectric of constant eps value grooved structure teeth
Which Geometry?:M
Frequency of the Electromagnetic Wave [Hz]:10e9
Focal length [m]:0.05
Correction Phase [even number]:8
Number of full-waves circular zones:2
End ...
__________________________________
Phase 2 Estimates the lens geometry
Lambda [m]: 0.0299792458
You Choosed Annular metallic reflector strucure
Two foci at: +/- 0.05  [m]
Low efficient <40%
Radius: [0.0, 0.019717596764508672, 0.028384033252359525, 0.03536395289712202, 0.041516877106596115, 0.047167564111305016, 0.05247850248472664, 0.057543839298576316, 0.06242339111852878, 0.0671576665436552, 0.07177541843678989, 0.07629780670045042, 0.08074085720475006, 0.08511699499131715, 0.08943604278970253, 0.09370589502665573, 0.09793298665387097]
Diameter of Lens [m]: 0.19586597330774194
F/D: 0.2552766014209149
End ...

Some input file examples show how to use the class and all the functions implemented. From a terminal, use the following command to launch the tool:

Example of lens antenna input files with conical teeth (InputLensConicalCostantEPS.t.xt):
L		<--- Specify that you want to design a lens 
DG		<--- Specify the geometry (DG mean constant EPS conical teeth)
10e9		<--- Working Frequency
0.05		<--- Focal point 
8		<--- Number of correction phase areas 2,4,6,8... 10 etc.. P
2		<--- Number of Fresnel Constant Zones W
3.0		<--- Specify the Dielectric permeability of the considered lens material

Example of reflector lens antenna input files with conical teeth ()InputLensConicalCostantEPS.t.xt):
R		<--- Specify that you want to design a lens 
DC		<--- Specify the geometry (DC mean lens of constant thickness and variable eps)
10e9		<--- Working Frequency
0.05		<--- Focal point 
8		<--- Number of correction phase areas 2,4,6,8... 10 etc.. P
2		<--- Number of Fresnel Constant Area W
3.0		<--- Specify the 


License:
See LICENSE.txt for more information.

Contact: Massimo Donelli - massimo.donelli@unitn.it 

Project link: 