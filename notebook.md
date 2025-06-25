## Week 4 (June 23, 2025 - June 27, 2025)

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
- [ ] Fix code from yesterday
- [ ] Plot xy orbit for current HFOFO input
- [ ]
- [ ]

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
    ```


    - 