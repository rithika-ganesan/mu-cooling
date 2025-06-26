# 6D Beam Matching In Helical FOFO Channels For Muon Cooling
## Lab notebook 

Hello! If you are reading this, I am still in the process of retroactively adding my previous work to this file. (I tried using Google Docs but it did not work as well for me so I am returning to markdown!)

## Week 0 (May 27, 2025 - May 30, 2025)

## Week 1 (Jun 02, 2025 - Jun 06, 2025)

## Week 2 (Jun 09, 2025 - Jun 13, 2025)

## Week 3 (Jun 16, 2025 - Jun 20, 2025)

## Week 4 (Jun 23, 2025 - Jun 27, 2025)

Overdue tasks:

- [ ] Add description of world material to Overleaf (M Jun 23)
- [ ] Add MICE discussion to overleaf (M Jun 23)

### Monday | June 23, 2025

**To-do:**
- [x] ~Clean up HFOFO input~
- [x] ~Write scripts to get the following and store in a file:~
    - [x] ~Wedge absorber widths~
    - [x] ~RF timing offsets~
    - [x] ~Solenoid currents~
- [x] ~Store wedge absorber widths in an external file to use loops~
- [x] ~Store sol currents in an external file to use loops~
- [x] ~Add description of physics list to overleaf~
- [ ] **Add description of world material to Overleaf**
- [x] ~Figure out how to run all commands inside same docker container instead of launching new each time~
- [x] ~Clean up matching section input~
- [x] ~Add more HFOFO periods to the matching section input~
- [x] Run a scan of currents for solenoid dimensions 
- [ ] **Add MICE discussion to overleaf**

**Log:**
- Started cleaning up the original HFOFO input file into a format that is easier to understand
- Began writing a description of the channel in the overleaf file
- Katsuya’s lecture on MICE
- Made a few plots looking at solenoid dimensions
- Modified docker run command with `--rm` flag

### Tuesday | June 24, 2025

**To-do:**
- [x] ~Clean up HFOFO input~
- [x] ~Get RF timing information  ~
- [x] ~Rewrite scripts~

**Log:**
- Added macros to HFOFO input file
- Stored all custom parameters [here](https://docs.google.com/spreadsheets/d/1kLRYvZeHiFVt271Rl15znbeaFh1iBoN3rxb7HgmF3jo/edit?gid=0#gid=0) 

### Wednesday | June 25, 2025

**To-do:**
- [x] ~Fix code from yesterday~
- [x] ~Plot xy orbit for original HFOFO input~
- [x] ~Plot orbit for reduced current HFOFO input~
    - [x] ~Write script to print macros with reduced currents~
    - [x] ~Generate input file with reduced currents~
    - [x] ~Generate root file~
    - [x] ~Make plots~
- [x] ~Make plots for alt reduced currents~
- [x] Look at timing offsets

**Log:**
- Git:
    - Renaming git branch from `main` to `working`:

    ```
    git branch -m main working
    git push --set-upstream origin working
    git push origin --delete main
    ```

    - Creating a new branch `main` for storing 'permanent' code:
    ```
    git checkout --orphan main
    git commit -m "test main"
    git push origin main
    ```
    - Command to check ls for branch: `git ls-tree -r main --name-only`
    - Deleted everything from branch main 
    - Will return to this later
- Checking orbit for original file:
    - Running docker in a test branch produces some kind of segmentation error -> root file still produced and is seemingly fine
    - output: `hfofotest.root`
    - Added issue for `read.read_trace` not producing full dataframe as well
    - Ran original file and plotted a few things. 
- Checking orbit for reduced currents:
    - Writing a script that takes a text file (?) of currents and generates commands we can add to input files -> place_currents.sh
    - Text file with currents: `input/hfofo-reduced-currents.txt` (Generated in Google Sheets)
    - output: `hfofo-reducedcurrents.root`
    - From plots: There seems to be a small section (z=4200 to z=6300) that seems to be roughly matched, but the matching section is not -- which means this will change as well. The output file has far fewer entries than the original version -- I am unsure why. The momenta do not go to zero, and the particle doesn't leave the channel either. 
    - What I think I should do next:
        - See if the original file is matched.
        - Drop the matching section, find conditions for the whole channel to form a steady orbit, then return to the matching section.
    - I think Caroline attempted both of these, so her older presentations might have something?
        - From [2/28 update](https://github.com/rithika-ganesan/mu-cooling/blob/working/other/resources/Muon%20Cooling%20Project%202-28-2025.pdf), it looks like the correct value was 230 and not 240 as was mentioned in the meeting. 
    - Running file + scripts again with currents reduced according to original p = 230 MeV/c:
        - Text file: `input/hfofo-reduced-currents-v2.txt`, plots: `plots/hfofo-reduced-currents-v2`
        - Clipped reduced current values to 3 decimal points
        - I think I should probably change the time offset values as well now. Before I do that, will test run the file.
- Timing offsets:
    - Katsuya's slides are [here](https://github.com/rithika-ganesan/mu-cooling/blob/working/other/resources/HFOFO02212025.pdf)
    - Code for time offset 0 `toffs0` from the file:
    ```
    param beamstart=-700       

    param beamtime=-0.671 # average time of mu+ in initial.dat modulo RF period TRF
    # if there is no mu+ take mu- and add TRF/2

    param toffs0=$beamtime-$beamstart/275.89-.07 # time needed to travel from beamZ to 0
    ```
    - The velocity $275.89$ comes from $v = \frac{pc}{\sqrt{p^2 + m^2}}$ where $p \approx 248$ MeV/c and $m = 105.7$ MeV/c^2. 
        - For the original value, 
        $$ v = \frac{248 \cdot c}{\sqrt{248^2 + 105.7^2}} = \frac{248 \cdot c}{269.58} = 0.91 \cdot c = 275.97 \text{ Mm/s}$$
        - For p=230 MeV/c, v = 272.592 Mm/s using the same calculation. 
        - v = 274.55 for p=240 MeV/c
    - I do not recall if we know what the .07 is for.
    - Maybe I should figure out what the p value is from the `initial.dat` file
- Original beam input file:
    - Copied `input/initial.dat` from Caroline's repo. Maybe rename this. It is now `input/initial_beam.dat`.

### Thursday | June 26, 2025

#### To-do 
- **Main**
    - [x] ~Make plot of histogram for original file beam~
    - [ ] Look at Caroline's code that she sent yesterday
- **Computing/organization**
    - [ ] Generalize 'place_currents.sh' into a function and add to .g4bl_bash
    - [ ] Figure out how to pass arguments from a function to subcomponents
    - [ ] Fix links in this doc to slides on github (all links go to things in branch `main`)
- **Reading**
    - [ ] Understand RF cavities better
- **Ideas for later**
    - [ ] Try using the original dat file to run the true HFOFO file.
    - [ ] Try moving the first two RF cavities in the matching section and seeing what happens


#### Log
- Meeting with Katsuya:
    - Run whole beam with some offset instead of reference particles
- Holmes group meeting:
    - Talk to Trent and read through his comp doc
    - Emailed him 
- Initial beam file
    - plotted histograms in `src/plot_beam.py` and added `make_histograms` function to `plot.py`
    - Got carried away studying pz distribution -- not as uniform as I had thought it would be, more langaus than purely gaussian 
    - perhaps later: fit beam profile to curve and see what the mean is.
    - For now: median is 289.960000
    - Which is quite high compared to what I expected
- Caroline's old code
    - Copied to `src/cr-pscans`
    - Just taking this line `reference referenceMomentum=221.7999999999999 particle=mu+ beamZ=0.0` and appending to copy of cleaned HFOFO `input/HFOFO-refptest.in`
    - unrelated: installed VS Code `code` shell command
    - When running this -> only first two periods have entries in trace
    - Ran Caroline's code unchanged -> everything looked as expected
    - Checking for differences between the two files:
        - I did not stochastics turned off
            - Turned it off and ran -- no changes
        - This line was missing from mine: `param TRF=1/325*1000 # RF period (ns)`
            - Added this
        - The only other thing that is immediately different is the beam itself 
            - Changed this
            - Still no change
        - root/ascii and docker are different -- could run locally
            - Ran a local file with ascii -- still the same
        - Modifying Caroline's file to not include detectors and seeing what happens
            - No change 
        - Ran the base file I had that just contains all input in a single file -- still very few entries even with stochastics turned off. 
        











