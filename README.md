# Linux Book
#### A Utilitiy designed on CLI for Linux users who get stuck in complex commands or want an interactive and helpful documentation of the linux commands.

[View Developer Docs](./developer.md)

### With this CLI Utility
- Interactively power-search commands by their subsets or by the work you want to be done
- Maintain your own database copy that comes with a preloaded set of commands but can be customized by you completely
- Enjoy all CRUD operations on ur personal command book
- Hence this is the linux book where you read as well as write
- LEARNS from your errors! Yes it detects your wrong inputs and learns with your consent to suggest you potential enhancements in the future.

## How to install and run
1. #### Firstly download the compiled binaries for your OS
2. If you are linux user : run `./main` <br>
  Else if you are windows user : double click on `main.exe`

## Troubleshooting
1. Restore database to its original form.
- download [[Raw_Database.db]]
- copy the file to `installaition_location/resources/database.db`

2. Fix : Library not found
- Option 1 : `pip install -r requirements.txt`
- Option 2 : switch to python3.9 and repeat option 1
