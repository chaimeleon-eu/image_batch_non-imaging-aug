# image_batch_non-imaging-aug

## Description
A data synthesizer for the data augmentation purpose of non-imaging tabular data. 

## Usage
Step 1. Git clone

Step 2. In the privacy folder, build the container using
```
sudo docker build --tag non-imaging-aug ./
```

Step 3. For a demo run (as presented in the report), copy the dataset.csv file and metadata.json file to a new working directory. And then test the synthesis performance with

```
#for synthesis
docker run --rm -v [working_directory]:/home/chaimeleon/datasets/ non-imaging-aug --target synthesis --data_dir /home/chaimeleon/datasets/data.csv

#for analysis
docker run --rm -v [working_directory]:/home/chaimeleon/datasets non-imaging-aug --target analysis -s /home/chaimeleon/datasets/tvae.csv
```

