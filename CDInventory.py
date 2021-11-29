#------------------------------------------#
# Title: Assignment06.py
# Desc: Working with classes and functions.
# Change Log: (Who, When, What)
# DBiesinger, 2030-Jan-01, Created File
# ALarson, 2021-Nov-20, Moved code blocks into functions and created doctext
# ALarson, 2021-Nov-21, Troubleshooted new code errors after moving into functions
# ALarson, 2021-Nov-27, Modified file processing to pickling/unpickling data instead 
#                       of writing to textfile, added error handling functionality,
#                       updated docstrings to reflect changes in processsing.
#------------------------------------------#

import sys
import pickle



# -- DATA -- #
strChoice = '' # User input
lstTbl = []  # list of lists to hold data
dicRow = {}  # list of data row
strFileName = 'CDInventory.dat'  # pickled data storage file
objFile = None  # file object
strTitle = ''
stArtist = ''
lstValues = []

# -- PROCESSING -- #
class DataProcessor:
    """The DataProcessor class processes the user data."""
    
    @staticmethod
    def add_CD(strID, strTitle, stArtist):
        """Function to add a new user-defined CD to the table in-memory.
        
        Args: 
            intID: the CD ID number as provided by the user
            strTitle: the CD title as provided by the user
            stArtist: the CD artist as provided by the user
            
        Returns: 
            None.
        """
        
        intID = int(strID)
        dicRow = {'ID': intID, 'Title': strTitle, 'Artist': stArtist}
        lstTbl.append(dicRow)
        
        
    @staticmethod    
    def delete_Row(intIDDel): 
        """ Function to delete row in table.
        
        Args:
            intIDDel: the ID of the CD to delete
        
        Returns: 
            None.
                    
        """
        intRowNr = -1
        blnCDRemoved = False
        for row in lstTbl:
            intRowNr += 1
            if row['ID'] == intIDDel:
                del lstTbl[intRowNr]
                blnCDRemoved = True
                break
        if blnCDRemoved:
            print('The CD was removed')
        else:
            print('Could not find this CD!')


class FileProcessor:
    """Processing (pickling/unpickling) the data to and from datfile"""

    @staticmethod
    def read_file(file_name, table):
        """Function to manage data ingestion from a pickled datfile to a list of dictionaries

        Reads the data from datfile identified by file_name into a 2D table
        (list of dicts) table one line in the file represents one dictionary row in table.

        Args:
            file_name (string): name of datfile used to read the data from
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None.
        """
        table.clear()  # this clears existing data and allows to load data from file
        
        try:
            objFile = open(file_name, 'rb')
            table = pickle.load(objFile)
            return table 
        except IOError:
            print('Unable to open the file', file_name,'.'.strip(), 'Ending program.\n')
            input('\n Press Enter to exit.')
            sys.exit()
        except:
            print('Unknown Error')
        finally:
            objFile.close()

    
    @staticmethod
    def write_file(file_name, table):
        """Function to manage the saving of pickled data to a datfile.
        
        Args: 
            file_name (string): name of file to be saved, presumably the same as has already been loaded in.
            table (list of dictionaries): 2D data structure (list of dicts) that holds the data during runtime
            
        Returns: 
            None.
            """
        try:
            objFile = open(strFileName, 'wb')
            pickle.dump(table, objFile)
        except IOError:
            print('Unable to open/write to file.')
        finally:
            objFile.close()
    
    
    
# -- PRESENTATION (Input/Output) -- #

class IO:
    """Handling Input / Output"""

    @staticmethod
    def print_menu():
        """Displays a menu of choices to the user

        Args:
            None.

        Returns:
            None.
        """

        print('Menu\n\n[l] load Inventory from file\n[a] Add CD\n[i] Display Current Inventory')
        print('[d] delete CD from Inventory\n[s] Save Inventory to file\n[x] exit\n')

    @staticmethod
    def menu_choice():
        """Gets user input for menu selection

        Args:
            None.

        Returns:
            choice (string): a lower case sting of the users input out of the choices l, a, i, d, s or x

        """
        try:
            choice = ' '
            while choice not in ['l', 'a', 'i', 'd', 's', 'x']:
                choice = input('Which operation would you like to perform? [l, a, i, d, s or x]: ').lower().strip()
            print()  # Add extra space for layout
            return choice
        except TypeError:
            print('Numbers aren\'t allowed, please choose a letter from the menu choices above.')


    @staticmethod
    def show_inventory(table):
        """Displays current inventory table


        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.

        Returns:
            None.

        """
        print('======= The Current Inventory: =======')
        print('ID\tCD Title (by: Artist)\n')
        for eachDict in table:
            print('{}\t{} (by:{})'.format(*eachDict.values()))
        print('======================================')

    
    @staticmethod
    def get_CD():
        """Function to get user input/information for the CD ID number, the CD title, and the CD artist.
        
        Args: None
            
        Returns:
            a tuple of the user's input: strID, strTitle, stArtist
        
        """
        while True:
            try:
                strID = int(input('Enter ID: ').strip())
                strID = str(strID)
                break                
            except ValueError:
                print('The ID must be a number. Please enter a numeric ID.')
            
        strTitle = input('What is the CD\'s title? ').strip()
        stArtist = input('What is the Artist\'s name? ').strip()
        return strID, strTitle, stArtist #returns a tuple

# 1. When program starts, read in the currently saved Inventory
lstTbl = FileProcessor.read_file(strFileName, lstTbl)


# 2. start main loop
while True:
    # 2.1 Display Menu to user and get choice
    IO.print_menu()
    strChoice = IO.menu_choice()

    # 3. Process menu selection
    # 3.1 process exit first
    if strChoice == 'x':
        break
    # 3.2 process load inventory
    if strChoice == 'l':
        print('WARNING: If you continue, all unsaved data will be lost and the Inventory re-loaded from file.')
        strYesNo = input('type \'yes\' to continue and reload from file. otherwise reload will be canceled')
        if strYesNo.lower() == 'yes':
            print('reloading...')
            lstTbl = FileProcessor.read_file(strFileName, lstTbl)
            IO.show_inventory(lstTbl)
        else:
            input('canceling... Inventory data NOT reloaded. Press [ENTER] to continue to the menu.')
            IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.3 process add a CD
    elif strChoice == 'a':
        # 3.3.1 Ask user for new ID, CD Title and Artist
        strID, strTitle, stArtist = IO.get_CD() #unpack and call at the same time
        # 3.3.2 Add item to the table
        DataProcessor.add_CD(strID, strTitle, stArtist)
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.4 process display current inventory
    elif strChoice == 'i':
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.5 process delete a CD
    elif strChoice == 'd':
        # 3.5.1 get Userinput for which CD to delete
        # 3.5.1.1 display Inventory to user
        IO.show_inventory(lstTbl)
        # 3.5.1.2 ask user which ID to remove
        while True:
            try:
                intIDDel = int(input('Which ID would you like to delete? ').strip())
                break
            except ValueError:
                print('Please type an ID (number) to delete')
        # 3.5.2 search thru table and delete CD
        blnCDRemoved = False
        DataProcessor.delete_Row(intIDDel)
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.6 process save inventory to file
    elif strChoice == 's':
        # 3.6.1 Display current inventory and ask user for confirmation to save
        IO.show_inventory(lstTbl)
        strYesNo = input('Save this inventory to file? [y/n] ').strip().lower()
        # 3.6.2 Process choice
        if strYesNo == 'y':
            FileProcessor.write_file(strFileName, lstTbl)
        else:
            input('The inventory was NOT saved to file. Press [ENTER] to return to the menu.')
        continue  # start loop back at top.
    # 3.7 catch-all should not be possible, as user choice gets vetted in IO, but to be save:
    else:
        print('General Error')




