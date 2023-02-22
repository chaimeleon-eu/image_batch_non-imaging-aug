# image_batch_privacypreserver
Tabular data synthesis and analysis

## Usage
Step 1. Git clone

Step 2. In the privacy folder, build the container using
```
sudo docker build --tag privacypreserver ./
```

Step 3. For a demo run (as presented in the report), copy the dataset.csv file and metadata.json file to a new working directory. And then test the synthesis performance with

```
#for synthesis
docker run --rm -v [working_directory]:/home/chaimeleon/datasets/ wp75 --target synthesis --data_dir /home/chaimeleon/datasets/data.csv

#for analysis
docker run --rm -v [working_directory]:/home/chaimeleon/datasets privacypreserver --target analysis -s /home/chaimeleon/datasets/tvae.csv --metric ml_efficency --meta_dir /home/chaimeleon/datasets/metadata.json
```
