# image_batch_non-imaging-aug

## Description
This repository presents a data synthesizer designed for augmenting non-imaging tabular data. The synthesizer incorporates four data synthesis algorithms, including a conventional approach known as the Gaussian copula model, as well as three deep learning-based algorithms: CTGAN, copulaGAN, and TVAE.

To assess the effectiveness of data augmentation using synthetic data, we developed an SVM classifier specifically for classification tasks. We compared the classification performance of SVM models trained with and without synthetic data, and conducted a Wilcoxon signed-rank test to determine the significance of any observed improvements.

![图片](https://user-images.githubusercontent.com/30890745/236931994-370ee336-a8f9-419d-853b-b5229bae1fc7.png)



## Usage
#### Step 1. Data preparation

The objective of this repository is to provide a solution for synthesizing tabular data. The input data should be organized as follows: each row of the table represents a patient/subject, and each column represents a feature that describes the patients. An example data is shown in ![data.csv](./data.csv).

This dataset is the Breast Cancer Wisconsin (BCW) dataset with 683 breast cancer patients. Features are computed from a digitized image of a fine needle aspirate (FNA) of a breast mass. They describe characteristics of the cell nuclei present in the image. All these features were valued on a scale of 1 to 10, with 1 being the closest to benign and 10 the most anaplastic. The classification target is to classify whether the tumor is benign or malignant.

![图片](https://user-images.githubusercontent.com/30890745/236933499-38cd6e5a-aa4b-4c16-8f09-d5e9ae998c77.png)



#### Step 2. Build the docker using below command:
```
sudo docker build --tag non-imaging-aug ./
```

#### Step 3. For a demo run on the BCW dataset, copy the dataset.csv file to a new working directory. And then test the synthesis performance with

```
#for synthesis
docker run --rm -v [working_directory]:/home/chaimeleon/datasets/ non-imaging-aug --target synthesis --data_dir /home/chaimeleon/datasets/data.csv

#for analysis
docker run --rm -v [working_directory]:/home/chaimeleon/datasets non-imaging-aug --target analysis -s /home/chaimeleon/datasets/tvae.csv
```

