import fitz
import os
import shutil
import random
# converts from-
"""
data
    - obj_train_data
        {label .txt files}
    - obj.data
    - obj.names
    - train.txt
pdf_path
"""
# to-
"""
Images
    - train
    - test
    - val
Labels
    - train
    - test
    - val
"""

class Annotations():
    def __init__(self, pdf_and_data_tuple_list, three_part_ratio) -> None:
        self.pdf_and_data_tuple_list = pdf_and_data_tuple_list
        self.pdf_path_list = [t[0] for t in pdf_and_data_tuple_list]
        self.data_path_list = [t[1] for t in pdf_and_data_tuple_list]
        self.three_part_ratio = three_part_ratio
    
    def get_annotation_folder(self):
        self.pdf_to_img()
        train_list, test_list, val_list = self.split_traintxt()
        self.send_splits_to_dirs(train_list, test_list, val_list)

    def pdf_to_img(self):
        for pdf_path,data_path in self.pdf_and_data_tuple_list:
            file_name = pdf_path.split("/")[-1]
            file_name = file_name.split(".pdf")[0]
            doc = fitz.open(pdf_path)

            # directory = file_name+"/"
            # path = os.path.join(parent_dir+directory)
            # os.mkdir(path)
            # Count variable is to get the number of pages in the pdf

            zoom = 4
            mat = fitz.Matrix(zoom, zoom)
            count = 0
            for p in doc:
                count += 1
            num_digits = len(str(count))
            for i in range(count):
                # page number
                # i = page_number
                a = i+1
                page_number = f"{a:0{num_digits}}"
                pdf_path = pdf_path.split(".")[0]
                
                val = f"{data_path}/obj_train_data/{pdf_path}000000000.jpeg-{page_number}.jpg"
                page = doc.load_page(i)
                pix = page.get_pixmap(matrix=mat)
                pix.save(val)
                # break
                
            doc.close()   
         
           
    def _divide_number_into_ratio(self,number, ratio):
        total_parts = sum(ratio)
        divided_parts = [number * part // total_parts for part in ratio]
        return divided_parts

    def  _copy_images_to_directory(self,file_list, target_directory):
        for file_path in file_list:
            # images
            target_ = target_directory
            if os.path.exists(target_):
                pass
            else:
                os.mkdir(target_)
            shutil.copy2(file_path, target_)

    def  _copy_labels_to_directory(self,file_list, target_directory):
        for file_path in file_list:
            # labels
            file_path = self._imgpth_to_labelpth(file_path)
            target_ = target_directory
            if os.path.exists(target_):
                pass
            else:
                os.mkdir(target_)
            shutil.copy2(file_path, target_)

    def _imgpth_to_labelpth(self,imgpth):
        labelpth = imgpth.replace(".jpg",".txt")
        # labelpth = imgpth.split(".")[:-1]
        # labelpth.append(".txt")
        # labelpth = "".join(labelpth)
        return labelpth

    def send_splits_to_dirs(self,train_list, test_list, val_list,):
        if os.path.exists("annotations7files"):
                pass
        else:
            os.mkdir("annotations7files")
            print("creating dir = annotations7files")

        if os.path.exists("annotations7files/Images"):
                pass
        else:
            os.mkdir("annotations7files/Images")
        if os.path.exists("annotations7files/Images/train"):
                pass
        else:
            os.mkdir("annotations7files/Images/train")
        self._copy_images_to_directory(train_list, "annotations7files/Images/train")
        if os.path.exists("annotations7files/Images/test"):
                pass
        else:
            os.mkdir("annotations7files/Images/test")
        self._copy_images_to_directory(test_list, "annotations7files/Images/test")
        if os.path.exists("annotations7files/Images/val"):
                pass
        else:
            os.mkdir("annotations7files/Images/val")
        self._copy_images_to_directory(val_list, "annotations7files/Images/val")




        if os.path.exists("annotations7files/Labels"):
                pass
        else:
            os.mkdir("annotations7files/Labels")
        if os.path.exists("annotations7files/Labels/train"):
                pass
        else:
            os.mkdir("annotations7files/Labels/train")
        self._copy_labels_to_directory(train_list, "annotations7files/Labels/train")
        if os.path.exists("annotations7files/Labels/test"):
                pass
        else:
            os.mkdir("annotations7files/Labels/test")
        self._copy_labels_to_directory(test_list, "annotations7files/Labels/test")
        if os.path.exists("annotations7files/Labels/val"):
                pass
        else:
            os.mkdir("annotations7files/Labels/val")
        self._copy_labels_to_directory(val_list, "annotations7files/Labels/val")


    def split_traintxt(self):
        """
        ratio: x:y:z
        """
        lines = []
        for data_path in self.data_path_list:
            file_name = data_path+'/train.txt'
            with open(file_name) as f:
                lines_ = f.readlines()
            for line in lines_:
                line = line.rstrip("\n")    
                line_list = line.split("/")
                line_list[0] = data_path
                line = "/".join(line_list)
                lines.append(line)
        random.shuffle(lines)
        # print(lines)
        # Remove newline characters from lines
            
        
        number = len(lines)
        ratio = self.three_part_ratio
        parts = self._divide_number_into_ratio(number, ratio)
        part_x = parts[0]
        part_y = part_x+parts[1]
        part_z = part_y+parts[2]
        # split
        train_set = lines[:part_x]
        test_set = lines[part_x:part_y]
        val_set = lines[part_y:part_z]
        return train_set,test_set,val_set
    


from time import time
if __name__ == "__main__":
    pdf_and_data_path_list = [("Wolters-Kluwer-2022-Annual Report.pdf","data7")]
    """ ("caterpillar-ar-2017.pdf","data3"),
                              ("en_Enhanced Sales Report_Quick_Reference_Guide.pdf","data4"),
                              ("LSE_MGNT_2020 (1).pdf","data5"),
                              ("salesforce-state-of-sales-4th-ed.pdf","data6"),
                              ("Wolters-Kluwer-2022-Annual Report.pdf","data7")]"""
    
    start_time = time()
    ann_class  = Annotations(pdf_and_data_path_list,[50,30,20])
    ann_class.get_annotation_folder()
    end_time = time()
    time_taken = round(((end_time-start_time)/60),2)
    print(f"time taken = {time_taken} minutes")
    
