### Jun 02, 2025 | Monday | Meeting with Katsuya and Caroline

- look at relation between dispersion
 - also look at x and y individually when a tilt is added
 - for a second coil, flip polatity to see if you can cancel out angular momentum
 - see if dispersion exists even when angular momentum is cancelled out
 - ideally dispersion and angular momentum should be decoupled
 - look at pz from B_r -> lorentz force along z
 - dp_r / dt = dp_r / dz times dz / dt = v_z tmes 

### May 30, 2025 | Friday | Meeting with HFOFO folks

- change both parameters to see periodicity for B and p and see if L changes as predicted by analytical model
- changing the amplitude(?) which depends on L --> so change px, py to see if there are meaningful changes
- focussing changes greatly depending on B, p values even for a single solenoid
- thin lens analysis depends on linearity -> mathieu equations instead
- validate analytical model:
    - perhaps using the above methods, might not work
    - paper for solving equations numerically/analytically
- for a single coil you can check the phase rotation?
- stopband models?
- when things are designed from scratch they start with a hamiltonian? 
- intermediate between continuum helical channel and more discretized rectilinear channel

- start with a single coil and look at the angular momentum and see how different tilts etc. change it. 
- maybe describe the rest?

### May 29, 2025 | Thursday | Meeting with Katsuya and Caroline

- Do the plot for the reference particle
- Fernow fig 1 -> type A easier for dispersion than type B
- Make your own bethe-bloch curve??? (muons in LiH)
- How do I get the trace for the reference particle?
- Change plot rc params
- Look at angular momentum (xpy - ypx) again

### May 28, 2025 | Wednesday | Meeting with Katsuya and Caroline

- orthogonal fofo
- matching section in front end
- hfofo can cool both m and mbar 
- change field strengths etc in yui's matching channel to have the final momentum at caroline's design input
- `sol_place7_31.txt` --> just 7 coils make up the matching section
    - starting at RotSol at z=-3000
- go over twiss parameters
- transfer matrix
- angular momentum induced in beam due to edge effects in solenoid
    - phase space rotates
    - this rotation can be used as part of matching
    - angular momentum can be used to separate charges
- don't rely too much on input files, use visualizations as sanity checks
- use `trace` to check the magnetic fields and the tuples at locations instead of placing detectors to avoid interactions with the 
- last meeting: fernow's paper
- ~join github, slack~
- estimating twiss parameters -> from phase space evolution, get covariance matrix, 
- pi resonance -> sudden loss in phase space
- mechanical orbital momentum (xpy - ypx) 
- what about canonical orbital momentum ?
- Br couples to pz creating orbital momentum
- from maxwell equation, from Bz as a fucntion of z, we can derive / estimate B_r from Masxwell's equation for free  (crul B = 0, div B = 0)
- make Bz vs z plot from solenoid, we can get \partial Bz / \partial z by looking at the slopes on the plots instead of estimating the function. 

To-do:

- [x] ~Join Slack~
- [x] ~Find GitHub~
- [x] Look at Fernow's paper
