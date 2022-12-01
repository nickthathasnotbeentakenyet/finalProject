import os
import time
from colorama import Fore
from tqdm import tqdm

#################################
# read the README.md file first #
#################################
CURRENT_DIR = os.getcwd()


def main():
    '''
    Purpose: Refer to README.md file
    Author: Arkadii Lantukh
    Parameters: None
    Return: None
    '''
    try: 
        # declaring some vars
        SOURCE_TXT =  "source.txt"
        SOURCE_DIR = CURRENT_DIR + "\SOURCE"
        DESTINATION_DIR = CURRENT_DIR + "\DESTINATION"

        # Find all files in the source directory, count and output the result
        print(f"{Fore.YELLOW}Searching for files in source directory...")
        source_file_list = read_filenames(SOURCE_DIR)
        count_f_source = count_files(source_file_list)
        print(f"{Fore.CYAN}Source dir: {count_f_source} files")

        # create supplemental folder to separate files by types
        make_filetype_folder(DESTINATION_DIR)

        # create temp file with file names
        make_storage_file(DESTINATION_DIR, SOURCE_TXT, source_file_list)

        # move files from source to destination
        move_files(source_file_list)

        # display a progress bar
        for i in tqdm(range(count_f_source), colour='cyan', desc='Moving'):
            time.sleep(.001)
        print(f"{Fore.GREEN}Success! Files moved to their destionation folders")

        # find all files in the destination folder
        moved_files = read_filenames(DESTINATION_DIR)

        # create temp file with files names of moved files
        make_storage_file(DESTINATION_DIR, 'destination.txt', moved_files)

        # create a log file and remove all temp files
        print(f"{Fore.YELLOW}Removing temp files...")
        time.sleep(.5)
        remove_temp_files(DESTINATION_DIR)

        # read filenames after clean up and count them up, output 
        files_after_cleanup = read_filenames(DESTINATION_DIR)
        count_f_destination = count_files(files_after_cleanup)
        print(f"{Fore.CYAN}Destion dir: {count_f_destination - 1} files + log")
        print(f"{Fore.CYAN}To view the log refer to {DESTINATION_DIR}\\log.txt")

        # OPTIONAL PART
        # Ask user if she wants to move files back. If no - say 'bye', if 'yes' - proceed
        user_answer = input(f"{Fore.MAGENTA}Move all files back to source directory? [y/n]: ")
        if get_user_answer(user_answer) == True:
            
            # create a list of files to move back to source and move them 
            move_back_files = read_filenames(DESTINATION_DIR)
            move_back(move_back_files)
            
            # count mpved back files in the source directory 
            moved_back_list = read_filenames(SOURCE_DIR)
            count_moved_back = count_files(moved_back_list)

            # display a progress bar
            for i in tqdm(range(count_moved_back), colour='cyan', desc='Moving'):
                time.sleep(.001)
            
            # notify user 
            print(f"{Fore.GREEN}Success! {Fore.CYAN}{count_moved_back} files moved back")

            # clear all temporary files, including the folders we created for different types of files
            clear_destination(DESTINATION_DIR)
            print(f"{Fore.GREEN}All temporary folders removed")
            print(f"{Fore.GREEN}Log file removed")

        # say goodbye 
        print(f"{Fore.MAGENTA}Thank you for using 'File Mover'{Fore.RESET}")

    
    except FileNotFoundError as not_found_err:
        print(type(not_found_err).__name__, not_found_err, sep=": ")

    except PermissionError as perm_err:
        print(type(perm_err).__name__, perm_err, sep=": ")

    except Exception as excep:
        print('Please contact Arkadii Lantukh and tell him he needs to fix this. Lol')
        print(type(excep).__name__, excep, sep=": ")


def make_filetype_folder(DESTINATION_DIR):
    '''
    Creates supplemental folders for different file extensions.
    In case if folder already exists, creation will be skipped 
    and user will be notified
    Parameters: DESTINATION_DIR - where the folders will be created
    Return: None
    '''
    folders = ['audio','video','images','docs','unsorted']
    for _ in folders:
        folder = DESTINATION_DIR + '\\' + _
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"{Fore.YELLOW}Creating folder '{_}'")
            time.sleep(1)
        else: print(f'{Fore.LIGHTRED_EX}Required folder already exist. Skipping..')


def read_filenames(location):
    '''
    Read filenames recursively in a specified directory
    Parameters: location
    Return: name_list. Each line is the path to a file 
    '''
    name_list = []
    for root, dirs, files in os.walk(location): 
        for file in files: 
                name_list.append(os.path.join(root,file))
    return name_list


def make_storage_file(path, source_txt, source_file_list):
    '''
    Creates a file that has a list of files from source directory
    Parameters: 
            path = where this file will be kept (destination folder)
            source_txt = name of the file
            source_file_list = list of files in source directory
    Return: none
    '''
    time.sleep(2)
    store = path + '/' + source_txt
    with open(store, 'w', encoding='utf-8') as f:
        for _ in source_file_list:
            f.write(_ + "\n")
    f.close()


def move_files(files):
    '''
    Moves files according to their extensions to appropriate folders
    Parameters: 
            files = files in the source directory
    Return: none
    '''
    docF = ['.txt','.csv','.doc','.rtf','.xls']
    audioF = ['.wma','.mp3','.wav','m4a','.cda']
    videoF = ['.avi','.mkv','.mp4','.webm','.wmv']
    imageF = ['.gif','.jpeg','.pdf','.png','.svg']
    log_file = CURRENT_DIR + "\DESTINATION" + "\\log.txt"
    with open(log_file, 'w', encoding='utf-8') as log:
        for f in files:
            if any(f.endswith(_) for _ in docF):
                f_path = str(f).replace('SOURCE', 'DESTINATION\\docs')
            elif any(f.endswith(_) for _ in audioF):
                f_path = str(f).replace('SOURCE', 'DESTINATION\\audio')
            elif any(f.endswith(_) for _ in videoF):
                f_path = str(f).replace('SOURCE', 'DESTINATION\\video')
            elif any(f.endswith(_) for _ in imageF):
                f_path = str(f).replace('SOURCE', 'DESTINATION\\images')
            else:
                f_path = str(f).replace('SOURCE', 'DESTINATION\\unsorted')
            log.write(f + " -> " + f_path + "\n")
            os.replace(f, f_path)
    log.close()


def move_back(files):
    '''
    Moves files back from the Destination folder to the Source folder
    It's a feature for testers
    It also removes the log file from the Destination directory
    Parameters:
            files = all files in subfolders within the Destination folder
    Return: none
    '''
    for f in files:
        old_loc = f
        f = str(f).split('\\') 
        f.pop(-2)
        f = '\\'.join(f)
        new_loc = str(f).replace('DESTINATION', 'SOURCE' )
        os.replace(old_loc, new_loc)
    os.remove(CURRENT_DIR + '\log.txt')


def remove_temp_files(destination_dir):
    '''
    Removes all temp files in the Destination folder
    Parameters: destination_dir
    Return: none
    '''
    sFile = destination_dir + "\\source.txt"
    dFile = destination_dir + "\\destination.txt"
    os.remove(sFile)
    os.remove(dFile)


def clear_destination(destination_dir):
    '''
    Removes subfolders where files were kept to revert the Destination folder 
    to its initial state
    Parameters: destination_dir
    Return: none
    '''
    folders = ['audio','video','images','docs','unsorted']
    for _ in folders:
        folder = destination_dir + '\\' + _
        if os.path.exists(folder):
            os.rmdir(folder)
            print(f"{Fore.YELLOW}Removing folder '{_}'")
            time.sleep(.5)


def get_user_answer(answer):
    '''
    Checks if user answered positively or not to
    either move all files back to the Source folder or
    keep them in the Destination folder
    Parameters: 
            answer = user input 
    Retrun: 
            boolean value
    '''
    if str(answer).lower() in ['y', 'yes', '+', ""]: return True
    else: return False


def count_files(file_list):
    '''
    Counts files in a given file list
    Parameters: 
            file_list = either in source or destination
    Return:
            count = number of files in a list
    '''
    count = 0
    for _ in file_list: count += 1
    return count


if __name__ == '__main__':
    main()







