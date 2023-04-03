#testing if med2image utility can be called within this python script

import os

#round 1-> downloaded patients range (2,16) patients 1 to 14
#round 2 -> downloaded patients (range (16,26)) patients 15 to 24
#round 3 -> downloaded patients (range (26,36)) patients 25 to 34
#round 4 -> downloaded patients  (range(36,51)) patients 35 to 49
#round 5 -> downloaded patients (range(51,52)) patient 50
#round 6 -> downloaded patients (range(52,68)) patient 51 to 66
#round 7 -> downloaded patients (range(68,81)) patient 67 to 79
#round 8 -> downloaded patients (range(81,94)) patient 80 to 92
#round 8 -> downloaded patients (range(94,102)) patient 93 to 100

for i in range(94,102): 
    patient_number=i-1
    print(f"{i}_image.nii")
    os.system(f"med2image -i /Users/srinivas/Desktop/Uni/Fourth_Year/FYP/Environments/practiceInitial/Unconverted/{i}_image.nii -d /Users/srinivas/Desktop/Uni/Fourth_Year/FYP/Environments/practiceInitial/datasets/patient{patient_number}/images -o patient{patient_number}.jpg")
    print(f"{i}_label.nii")
    os.system(f"med2image -i /Users/srinivas/Desktop/Uni/Fourth_Year/FYP/Environments/practiceInitial/Unconverted/{i}_label.nii -d /Users/srinivas/Desktop/Uni/Fourth_Year/FYP/Environments/practiceInitial/datasets/patient{patient_number}/masks -o patient{patient_number}-mask.jpg")
    
    
    
    
    #If directories of images and masks structured by patient are not feasible, the below code can be used. 
    #os.system(f"med2image -i /Users/srinivas/Desktop/Uni/Fourth_Year/FYP/Environments/practiceInitial/Unconverted/{i}_image.nii -d /Users/srinivas/Desktop/Uni/Fourth_Year/FYP/Environments/practiceInitial/datasets/images -o patient{patient_number}.jpg")
    print(f"{i}_mask.nii")
    #os.system(f"med2image -i /Users/srinivas/Desktop/Uni/Fourth_Year/FYP/Environments/practiceInitial/Unconverted/{i}_label.nii -d /Users/srinivas/Desktop/Uni/Fourth_Year/FYP/Environments/practiceInitial/datasets/masks -o patient{patient_number}-mask.jpg")
