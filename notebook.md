# 6D Beam Matching In Helical FOFO Channels For Muon Cooling
## Lab notebook 

If you are reading this, I am still in the process of retroactively adding my previous work to this file! (I tried using Google Docs but it did not work for me so I am returning to markdown.)

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
- [ ] Plot orbit for reduced current HFOFO input
    - [x] ~Write script to print macros with reduced currents~
    - [x] ~Generate input file with reduced currents~
    - [x] ~Generate root file~
    - [ ] Make plots
- [ ] Computing/organization
    - [ ] Generalize 'place_currents.sh' into a function and add to .g4bl_bash
    - [ ] Figure out how to pass arguments from a function to subcomponents

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
- 


