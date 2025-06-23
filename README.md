# Muon collider accelerator studies

### Relevant links
Caroline's muon cooling [GitHub](https://github.com/criggall/muon-cooling?tab=readme-ov-file) <br>
Solenoid study [GitHub](https://github.com/criggall/solenoid-study)  
g4beamline [documentation](https://www.muonsinc.com/Website1/Muons/G4beamlineUsersGuide.pdf) <br>

### Relevant papers

[Muon collider design](https://arxiv.org/abs/acc-phys/9604001)   
[Helical FOFO Snake for Initial Six-Dimensional Cooling of Muons](https://inspirehep.net/literature/1678715)  
[A High-Performance Rectilinear FOFO Channel for Muon Cooling](http://accelconf.web.cern.ch/PAC2013/papers/thpho12.pdf)  
[Solenoidal ionization cooling lattices](https://journals.aps.org/prab/pdf/10.1103/PhysRevSTAB.10.064001)

### Resources



### Repo structure

<pre>
.g4bl_bash   
.README.md    
.    
|---src   
|   '----uproot_g4bl.py    
|   
|---input   
|   |----singlecoil.in   
|   |----HFOFO-matching-frozen.in  
|   |----matching.in  
|   '----solenoid-matching.in  
|  
|---output  
|   |----singlecoil  
|   |----matching  
|   '----solenoid-matching  
|  
'---other  
    |---slides  
    |---resources  
    |   '---notes  
    '---ascii  
</pre>

**Bash commands**

- Source: `source .g4bl_bash`
- Run `intg4bl` to launch Docker container interactive terminal
- Run `rung4bl path/to/inputfile.in` to run g4bl in the container.  


<!--- 

 **May 27, 2025**  Installed geant4, g4beamline, and ran g4beamline regression test check 

**May 27, 2025**  Created folder & repo, initialized git -->

