# Attention !

Before you go any further, please read the guidlines to keep your files *safe* and 
to make sure this *program works* as it supposed to.

## Structure

The project contains two folders **[SOURCE, DESTINATION]**. They are part of this program.
The **SOURCE** folder contains 21 fake files: *5 documents, 5 images, 5 audio, 5 video, 1 unsorted*
These files are placed to keep your personal files away from being touched in this project.
The **DESTINATION** folder is where files are to be moved to. 

## WorkFlow

**IMPORTANT** - Make sure your *current working directory* is where this project is, 
as the program is using *os.getcwd()* as part of its workflow.

When you start the program it:
1. Reads files in the **SOURCE** directory
2. Counts the files and outputs the count
3. Creates folders for different types of files in the **DESTINATION** folder
4. Creates a temporary file with a list of files to be moved
5. Moves all files to their corresponding folders within the **DESTINATION** folder
6. Prints a success message to notify user the files are moved
7. Reads files in the **DESTINATION** folder recursively
8. Creates a log file in the **DESTINATION** folder that shows where each file was taken from and where it was moved to
9. Removes all temporary files
10. Counts the number of files in the **DESTINATION** folder
11. Outputs the number of files and path to the log file
12. Asks user if she wants to move all files back to the **SOURCE** directory
*NOTE* This is totaly optional. It is done to prevent tester from manualy cutting/pasting files back and forth.
13. If users answers *no*, farewell message is printed. **END**. If user answers *yes*:
14. Files are moved back to **SOURCE** directory
15. All supplemental folders, files, including the log are removed. All is back to the initial state.
16. Prints a farewell message

## What else

- I've been working on making a GUI, but decided to keep things simple for now
- I've worked on letting the user to decide where files are taken from and where to place them, but for this project 
I really want to keep things simple, but working. Working with files is dangerous.
- I've worked on making a global dictionary where file types' folders are presented as keys and file types' extensions
are presented as values. User could add her own specifications there. But again, things went quite tedious and to make it simple, but yet working, I decided to keep away from this idea at this time

## Thanks for reading this. Have fun!





