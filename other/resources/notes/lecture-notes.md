
# Accelerator design

## Lecture 3

### Recap of prev. lectures:

- beam dynamics + SHM analog 
- "transfer matrix" -> canonical coordinate transform?
    - is there mixing classically?
- beta function and evolution of the beta function can fully represent all three twiss parameters
- **q: how is $\epsilon_rms$ defined for multiple axes?**
- $\mu$ in eigenvalue solution of hill's equation describes phase advance
- with focusing length, transfer matrix, and initial conditions, we can get the angular spread 
- 'lens' -> operations to the right
- in thin lens approximation: transfer matrix is just regular matrix constructed from lens equation
- larry asked: what would the unitarity of the transfer matrix mean?
- phase advance (as fraction of the full 360) describes how much a particle transforms 

### g4beamline

- we use a geant4 based simulation software because we want to have material in the beam line at some point and i guess other softwares don't allow for that?
- you can define a quadrupole! try!
- "focusing" and "defocusing" refer to horizontal beam motion -> is this just in this specific g4bl input file or is that convention?
- **q: when you use trace how do you change how many data points it gives out in the output file?**
- maybe i should learn mathematica -> ask if i can have the mathematica file that h showed with all the calculations or try to do it in mathematica
- he demonstrated in the first part that the thin lens approximation holds for a simple FODO cell:
    - solve transfer matrix and thin lens analysis to get twiss paramaters
    - show that twiss parameter ellipse contains all data points from simulation in phase space
- stability condition for thin lens from |tr(M)| < 2 (approximate equation)
- interesting: he says FOFO is focusing focusing instead of FODO which is focusing defocusing. previously i had thought FOFO = FODO FODO.
- fig 1 in fernow paper caption -> operators are and and or? actually maybe not.
- look at different lengths for the solenoid and see if Bz field changes
- make fig 1 from fernow with different colors for solenoids of different polarities
- try to replicate things from these slides
- get focal length from x vs z plot
- no known explanation (to people in the room) for why _very_ thin lens approximation does not work 
- larmor motion and larmor rotation frame?
- **read the Dugan paper**
- larmor motion couples x and y
- do not understand transverse emittance formula that has 1/4th power
- in the fernow fig 1 channels, how exactly are the rf cavities and the solenoids arranged? are the rf cavities inside the solenoids?
- fernow fig 1 a and b differ in where the beam starts -- how do you actually control where the beam starts in g4bl?
- **we place absorbers at minimum beta function -- why?**  
- stop band structure of beta function?
- angular momentum induced by larmor motion must have specific values wrt to the position --> otherwise causes filamentation in phase space
- acceptance becomes smaller for smaller particles

- stopband structure -> you can design a channel with the goal of trying to move the beta function lower to reduce the band gap

- **look at dikty's rectilinear channel**

- helical channel uses continuous solenoid as opposed to discrete solenoids in rectilinear channels etc.
- 

two main questions at this point:

- how are rms emittance, transverse emittance, emittance in 3d dimensions, etc. defined?
- how do i get an intuition for canonical angular momentum?

- hfofo -> use dispersion for the resonance condition instead
  
- dave says that hfofo is between rectilinear and helical. 

- high gradient RF?
 
- very interesting plot on last slide -> this could be something we try to make at the end of the summer: projected vs reached?

- adding beam instrumentation?
