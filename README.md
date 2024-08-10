# Keyboard Dynamics Authentication

This project is to build a keyboard dynamic based authentication system


## Capture
Capture Keyboard dynamics: key, time, edge/trigger

### Capture Technique
Key stroke events are captured asynchronously.
The asynchronous capture will start for the password potion of the procedure.

__WARNING__: if the user switches out of the capture program while in the password
procedure. They will basically be keylogged, and that data will be collected.

### Procedure
1. Ask for user name
2. Ask for password
3. Ask for password to be repeated 5 times
4. exit & output file

### Output
type - file
    File name: `username-date-time`
    File payload: json

- [ ] Capture
- [x] Async Capture
- [x] Procedure
- [ ] Output: Data File

## Data Visualization
From the Capture file events will be displayed.
Each Key will be displayed like a signal on a logical analyzer.

- [ ] Data Visualization
- [ ] Command line args
- [ ] Data processed
- [ ] Graph output

## Training/Classification
will try different models and go from there.

Depending on the classifier used more visualization maybe required.

- [ ] Training/Classification
- [ ] pick classifier
- [ ] create verification program
