import torch 
import os
from PIL import Image
from torchvision.transforms import functional,Grayscale
import cv2
import numpy as np
import copy

class CTADataset(torch.utils.data.Dataset):

        def __init__(self,imageDir,maskDir,transform=None): 
            # transforms=> list of transforms to be done on the data
            # imageDir => the path to the images
            # maskDir => the path to the masks
            
            self.imageDir=imageDir
            self.maskDir= maskDir
            self.transform=transform
            self.imageContrast=1
            self.maskContrast=1
            #generating semantically labelled segmentation maps here
            self.target_maps=[]

            #need to make sure they are listed in order
            self.images=os.listdir(self.imageDir)
            self.masks=os.listdir(self.maskDir)

            self.images.sort()
            self.masks.sort()

            print("Creating semantically labelled segmentation maps")
            for mask in self.masks:
                maskSlice= Image.open(os.path.join(self.maskDir,mask))
            
                #making a copy of the image object and converting it to greyscale and resizing it.
                maskSlice_copy=copy.deepcopy(maskSlice)
                maskSlice_copy=functional.to_grayscale(maskSlice_copy, num_output_channels=1)
                
                maskSlice_copy=functional.resize(img=maskSlice_copy,size=[128,128])

                #returns a semantically labelled mask
                target_map=self.get_target_map_from_mask(maskSlice_copy)

                #adding a channel [1] to the start of the dimensions
                target_map =np.reshape(target_map,(1,target_map.shape[0],target_map.shape[1]))

                self.target_maps.append(target_map)



        def __len__(self):
            return len(self.images)

        def setImageContrast(self,contrast_multiplier):
            self.imageContrast=contrast_multiplier

        def settMaskContrast(self,contrast_multiplier):
            self.maskContrast=contrast_multiplier

        def get_target_map_from_mask(self,maskSlice):
            '''
            read in image using opencv's imread
            convert image to np array
            '''
            #mask=cv2.imread(maskPath)
            #mask=maskSlice
            
            mask_copy_array=np.asarray(maskSlice)
            mask_copy=copy.deepcopy(mask_copy_array)

            mask_pixels=mask_copy

            #print("Dimensions of passed in mask is : ", mask_pixels.shape)

            #setting pixels that aren't black (background) or white (TL) to be grey (FL)
            mask_pixels[(mask_pixels>=250)]=255
            mask_pixels[(mask_pixels>=70) & (mask_pixels<250) ]=128
            mask_pixels[(mask_pixels<70)]=0
            
            #print("After editing, the unique values are: ", np.unique(mask_pixels))
            '''
            #rgb values for background pixel-> (0,0,0) usually if greyscale=> 0
            #rgb values for tl -> (255,255,255), if greyscale -> 255
            #rgb values for fl -> grey (might need to threshold for this to work)
            '''
            colour_map=[0,255,128]

            #for single channel image, dimension would be [height,width]
            #print(mask_pixels.shape[0]) #height
            #print(mask_pixels.shape[1]) # width
            #print(mask_pixels[0][0][2])

            #iterate over every pixel and assign it a value based on the class it belongs to     
            for i in range(mask_pixels.shape[0]):
                 for j in range(mask_pixels.shape[1]):
                    mask_pixels[i][j]= colour_map.index(mask_pixels[i][j])

            
            return mask_pixels #pixel array, where each pixel value is equal to a class.
            

        def __getitem__(self,index):
            imagePath=os.path.join(self.imageDir,self.images[index])
            maskPath= os.path.join(self.maskDir,self.masks[index])

            #print("ImagePath",imagePath)
            #print("MaskPath",maskPath)
            imageSlice=Image.open(imagePath)
            maskSlice= Image.open(maskPath)
            
            
            #enhancing contrast of the images can be done using torchvision.transforms.functional.adjust_contrast(image,factor)
            imageSlice=functional.adjust_contrast(imageSlice,self.imageContrast)
            maskSlice=functional.adjust_contrast(maskSlice,self.maskContrast)


            if(self.transform):
                return self.transform(imageSlice),self.transform(maskSlice),imagePath,maskPath,self.target_maps[index]
        
            return imageSlice,maskSlice,imagePath,maskPath,self.target_maps[index] #would need to return the mask slice and image slice for the given patient.





#ONE-HOT ENCODING HERE
'''
read in image using opencv's imread
convert image to np array
'''
'''
            #rgb values for background pixel-> (0,0,0) usually
            #rgb values for tl -> (255,255,255)
            #rgb values for fl -> grey (might need to threshold for this to work)
            
            colour_map=[ [rgb value for background pixel], [rgb value for TL],  [rgb value for FL] ]

            binary_mask=[]
            for index,colour in enumerate(colour_map):
                channel_map=np.all(np.equal(mask,colour), axis=-1)

                binary_mask.append(channel_map)
            
            binary_mask=np.stack(binary_mask,axis=-1)
            #binary mask should contain 3 channels (3 classes), with 1 channel only showing background, another channel only showing TL and another channel only showing FL. 
'''
