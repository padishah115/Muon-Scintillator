NOTE: MAIN.PY IS THE PROJECT FILE

Project created to model the motion of a charged muon through a scintillating array. The quantum efficiency of the array, the stopping probability of the muon, and the muon lifetime are all tunable parameters of the problem. The program then generates plots to show the 
passage of the muon through the array, as well as the "pulse" output for an observer checking the output signal from the array.

Extensive project whose purpose is to use the Bethe equation to calculate energy loss of a muon travelling through a material of known stopping power (via atomic number, mass number, etc.)

The simulation operates by generating muons, first randomly generating their zenith angle in line with the literature cos^2(theta) distribution which describes muons created in the atmosphere (velocity_distribution.py), assuming that the muons effectively travel at the speed of light. The muons are then generated just outside the array, depending on their angle of incidence, and their passage though a fictitious scintillating array is simulated, producing a scintillation output (a bar graph), which is a schematic diagram showing where scintillation events have been triggered in the array. In addition to this, every scintillating bar has a simple electronic "readout", producing binary signals indicating when the muon has passed through each scintillator. Whether or not events are detected is determined by the efficiency of the SiPMs (which can be changed at will in the main.py file.)

This project is a work in progress and is written/maintained by Hayden Ramm as per a Part III physics project undertaken at the University of Cambridge, in collaboration with a group of students and academics in the High Energy Physics Department at the Cavendish Laboratory.