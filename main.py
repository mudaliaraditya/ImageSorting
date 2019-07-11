from __future__ import print_function
import exifread
import os
import shutil
# Open image file for reading (binary mode)
from datetime import datetime

class Picture:
   FileName = ""
   Date     = ""
   Path     = ""
   
try:
    path =raw_input("Enter Image Dir With / or \\ ");
except:
    try:
        path = input("Enter Image Dir With / or \\ ");
        #print ("error");
    except:
        exit (1)

path = os.path.join(path, '')
print(path)
files = []

for r, d, f in os.walk(path):
    for file in f:
            files.append(os.path.join(r, file))

for f in files:
    print(f)

entries = files
string = [];

#entries = os.listdir(DirToSearch)
for entry in entries:
    if os.path.isdir(entry):
        print("\nIt is a directory")
    elif os.path.isfile(entry):
        print("\nIt is a normal file")
        f = open(str(entry), 'rb')
        try:
            print(entry)
            tags = exifread.process_file(f)
            i = 0;
            File = Picture();
            for tag in tags.keys():
                if tag  in ('Image DateTime'):
                    File.FileName = os.path.basename(entry);
                    File.Date = str(tags[tag]);
                    head, tail = os.path.split(entry)
                    File.Path = head;
                    #string.append(tags[tag]);
                    string.append(File);
        finally:
            f.close()
    else:
        print("It is a special file (socket, FIFO, device file)" )

for Filelist in string:
#print(string.split(':, ', len(string)))
    datetime_object = datetime.strptime( Filelist.Date, '%Y:%m:%d %H:%M:%S');
    print (Filelist.FileName," ",datetime_object.second," ",datetime_object.hour," ",datetime_object.minute);

    FinalStringName = path + str(datetime_object.day) + str(datetime_object.month) + str(datetime_object.year)
    print ("folder name is ",FinalStringName)
    if not os.path.isdir(FinalStringName) :
        os.mkdir(FinalStringName)
    FinalFile = os.path.join(FinalStringName ,  Filelist.FileName)
    SourceFile = os.path.join(Filelist.Path , Filelist.FileName)
    print ("source file is ",SourceFile)
    print ("final file is ",FinalFile)
    try:
        shutil.copyfile(SourceFile, FinalFile);
    except:
        print ("error occured but still continuing")
        continue;
    os.remove(SourceFile)
try:
    path =raw_input("Press Enter to quit");
except:
    try:
        path = input("Press Enter to quit");
        #print ("error");
    except:
        exit (1)

