# yolo-annotations


Conversion from yolo format (from CVAT) to the format required by the yolo pipeline

Yolo format:
data
- obj_train_data
{label .txt files}
- obj.data
- obj.names
- train.txt


Required format:
Images
{page images .jpg files}
- train
- test
- val
Labels
{label .txt files}
- train
- test
- val


The annotations obtained in yolo format from CVAT only contain labels for files as listed in train.txt. The required format needs the images as well.
So the conversion pipeline requires 3 arguments- the path to the pdf(s), the path to the corresponding annotation file from CVAT and the train, test, val split ratio percentage.


We can provide a list containing tuples of pdf_path and the annotation data file.
pdf_and_data_path_list = [("Wolters-Kluwer-2022-Annual Report.pdf","data7"),
("caterpillar-ar-2017.pdf","data3"),
("en_Enhanced Sales Report_Quick_Reference_Guide.pdf","data4"),
("LSE_MGNT_2020 (1).pdf","data5"),
("salesforce-state-of-sales-4th-ed.pdf","data6"),
("Wolters-Kluwer-2022-Annual Report.pdf","data7")]
required_format_annotations = Annotations(pdf_and_data_path_list,[50,30,20]).get_annotation_folder()

This also performs random shuffling on the dataset before splitting it. 
