# DISFA+ Dataset

Follow this guide in order to train the VideoSwinTransformer using the
DISFA+ dataset.

## Download the dataset

The following script will download and unzip the DISFA+ dataset

```bash
cd tools/data/disfa+
./download_dataset.sh
```

## Format the Dataset

The following script will format the downloaded dataset into a
MMAction frienly layout.

```bash
cd tools/data/disfa+
./disfa+_to_frames.sh
```

or equivalently (if you need to specify alternative routes):

```bash
cd tools/data/disfa+
./disfa+_to_frames.py --disfa ../../../data/disfa+/raw/disfa+/ --output ../../../data/disfa+/
```

## Trim the Samples

The dataloader requires that the action starts at the very
beggining. Run the following script to trim the existing videos and
remove unneeded video frames from the start.

```bash
./trim_videos.sh
```

## Train VST

In order to train the project, run the following *in the root of the project*

```bash
python3 tools/train.py --validate configs/recognition/swin/swin_base_patch244_window877_disfa+_22k.py
```

