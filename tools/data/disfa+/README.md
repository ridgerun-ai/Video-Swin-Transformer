# DISFA+ Dataset

Follow this guide in order to train the VideoSwinTransformer using the
DISFA+ dataset.

## Download the dataset

The following script will download and unzip the DISFA+ dataset

```bash
cd tools/data/disfa+
./download_dataset.sh
```

## Format the dataset

The following script will format the downloaded dataset into a
MMAction frienly layout.

```bash
cd tools/data/disfa+
./disfa+_to_frames.sh
```

or equivalently:

```bash
cd tools/data/disfa+
./disfa+_to_frames.py --disfa ../../../data/disfa+/raw/disfa+/ --output ../../../data/disfa+/
```

## Train VST

In order to train the project, run the following *in the root of the project*

```bash
python3 tools/train.py --validate configs/recognition/swin/swin_base_patch244_window877_disfa+_22k.py
```
