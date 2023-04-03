#Trying to split the patient directories into training, validation and testing datasets. (70,15,15 split)

###Tasks
   #Given a list of files, randomly generate a subset of given proportion.
    #Shuffle the actual files around into train, val and test dirs based on the subsets generated, using OS lib.
    #Note if the .DS_Store file exists in Split_Datasets or in the datasets directory, I'd need to remove it:

import os
from random import sample,seed
from shutil import move, copytree

def remove_DS_Store(path):

    try:
        os.remove(path)
        print(f".DS_Store file found at {path}")
        print(".DS_Store file removed")
    except OSError:
        print(f".DS_Store file doesn't exist at {path}")



def split_patients():
    
    split_proportions={"train": 0.7,
    "val": 0.15,
    "test": 0.15
    }

    dataset_dir_path="/Users/srinivas/Desktop/Uni/Fourth_Year/FYP/Environments/practiceInitial/datasets"
    split_dest_path="/Users/srinivas/Desktop/Uni/Fourth_Year/FYP/Environments/practiceInitial/Split_Patients"
    path_to_DS_Store_file="/Users/srinivas/Desktop/Uni/Fourth_Year/FYP/Environments/practiceInitial/datasets/.DS_Store"

    # dataset_dir_path="/content/drive/MyDrive/FYP-Aortic_Dissection_Segmentation/datasets"
    # split_dest_path="/content/drive/MyDrive/FYP-Aortic_Dissection_Segmentation/Split_Patients"
    # path_to_DS_Store_file="/content/drive/MyDrive/FYP-Aortic_Dissection_Segmentation/datasets/.DS_Store"
    
    print("Accessing the directory at %s",dataset_dir_path)

    #The existence of the .DS_Store file due to file copy and move operations poses a problem to keeping datasets cleanly structured.
    #Thus it is removed, if it exists.
    remove_DS_Store(path_to_DS_Store_file)
   
    #getting the list of patient dirs
    patients=os.listdir(dataset_dir_path) 

    #printing out the patients and the number of patients in the dataset
    #print(patients)
    num_patients=len(patients)
    print(f"There are {num_patients} patients in the dataset")

    #need to get 70% of len(patients) and move them into a directory called train, 15% into val and 15% into test
    

    for proportion in split_proportions:
        print(f"\n----------------------------------Splitting into {proportion} directory------------------------------------------------------------\n")
        print(proportion,split_proportions[proportion])
        
        #get proportion of random patients and send them into appropriate directory
        split_percentage=round(num_patients*split_proportions[proportion])
        print(f"{split_percentage} files are selected for {proportion} ")

        #randomly sample patient files that are still in datasets (sampling without replacement)
        #NOTE: To make the sample reproducable, set random.seed(number)  here
        seedNum=7
        seed(seedNum)
        selected_files= sample(patients,split_percentage)
        print("Seed used for sampling the files to be split: ",seedNum)
        print(f"Files selected for {proportion} are {selected_files}")

        #move selected_files into appropriate directory. directory would be like "..../Split_datasets/train""
        dest_path=os.path.join(split_dest_path,proportion)
        #removing the .DS_Store file if it exists within train, test or val directories.
        remove_DS_Store(os.path.join(dest_path,".DS_Store"))
        
        #print(f"Moving {selected_files} to {dest_path}")

        for file in selected_files:
            source_path=os.path.join(dataset_dir_path,file)
            #print(source_path)
            dest_dir=os.path.join(dest_path,file)
            #print(dest_dir)
            move(source_path,dest_dir)
    
        #reevaluating the files that have not been split
        patients=os.listdir(dataset_dir_path) 
        print("Files left: ",patients)
        


#This function will reset the dataset structure after split and send all patients back to the source directory.
def reset_split_patients():

    print("Reverting dataset samples back to original directory")

    #traverse the Split_Datasets directory and move all the folders within its train, test and val directories back to the datasets directory,
    
    #Note if the .DS_Store file exists in Split_Datasets:
        # make sure to delete it using os.command(cd <path_to_Split_Datasets>) and os.command("rm .DS_Store")
        # UPDATE: Wrote a function to do the above
    
    #NOTE: UNCOMMENT IF USING LOCALLY
    source_path="/Users/srinivas/Desktop/Uni/Fourth_Year/FYP/Environments/practiceInitial/Split_Patients"
    dest_path="/Users/srinivas/Desktop/Uni/Fourth_Year/FYP/Environments/practiceInitial/datasets"
    path_to_DS_Store_file="/Users/srinivas/Desktop/Uni/Fourth_Year/FYP/Environments/practiceInitial/Split_Patients/.DS_Store"

    #NOTE: Comment if using locally
    # source_path="/content/drive/MyDrive/FYP-Aortic_Dissection_Segmentation/Split_Patients"
    # dest_path="/content/drive/MyDrive/FYP-Aortic_Dissection_Segmentation/datasets"
    # path_to_DS_Store_file="/content/drive/MyDrive/FYP-Aortic_Dissection_Segmentation/Split_Patients/.DS_Store"
    
    remove_DS_Store(path_to_DS_Store_file)
    remove_DS_Store(os.path.join(dest_path,".DS_Store"))


    dirs_to_move= os.listdir(source_path)
    print("Source directories that contain patients: ",dirs_to_move)  # should be a list of "train", "test"  and "val"

    for dir in dirs_to_move:
        print(f"Moving files back to source directory from {dir} directory")
        new_dir=os.path.join(source_path,dir) #indexing in to the individual directories

        #getting the patient samples to be moved back
        selected_to_move=os.listdir(new_dir) #getting a list of the patient folders within the split directories (train,test & val)
        #print("Files that are being moved back: ", selected_to_move)

        for selected in selected_to_move: #moving individual patient folders back into the datasets directory.
            #move(new_dir+"/"+selected,dest_path)
            move(os.path.join(new_dir,selected),dest_path)

    patients_restored=len(os.listdir(dest_path))
    print(f"\nOriginal dataset directory now has {patients_restored} patients")
        
  

#The below method is used to copy the patient's images and masks proportionally into train, test and val image and masks dirs
#Eg: the train dir would contain 2 folders-> images and masks. It would contain the images and masks of all patients that were
# split into  train, val and test dirs in the Split_Patients folders.

def copy_collate_datasets():

    source_dir="/Users/srinivas/Desktop/Uni/Fourth_Year/FYP/Environments/practiceInitial/Split_Patients"
    

    #source_dir="/content/drive/MyDrive/FYP-Aortic_Dissection_Segmentation/Split_Patients"
    split_patient_dirs= os.listdir(source_dir)
    print(split_patient_dirs)

    for dir in split_patient_dirs: #iterating through train, test and val
        dir_path=os.path.join(source_dir,dir)
        print(dir_path)
        patients=os.listdir(dir_path)
        print(f"checking for .DS_Store file at {dir_path}")
        remove_DS_Store(os.path.join(dir_path,".DS_Store"))

        dest_dir="/Users/srinivas/Desktop/Uni/Fourth_Year/FYP/Environments/practiceInitial/Prepared_Dataset"
        #dest_dir="/content/drive/MyDrive/FYP-Aortic_Dissection_Segmentation/Prepared_Dataset"
        
        print(patients)
        for patient in patients: #iterating through patients in the train, test and val dirs
            images_sourcepath=os.path.join(dir_path,patient,"images")
            masks_sourcepath=os.path.join(dir_path,patient,"masks")
            dest_path=os.path.join(dest_dir,dir)
            copytree(images_sourcepath,os.path.join(dest_path,"images"),dirs_exist_ok=True)
            copytree(masks_sourcepath,os.path.join(dest_path,"masks"),dirs_exist_ok=True)





#Uncomment when the patients have to be split into train, test and val.  
#split_patients()

#Uncomment to send all dataset files back to the datasets folder.
#reset_split_patients()

copy_collate_datasets()


