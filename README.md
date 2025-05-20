

<div align="center">
  <a href="(https://github.com/panliangrui/ACM_MM_2025/blob/main/liver.jpg)">
    <img src="https://github.com/panliangrui/ACM_MM_2025/blob/main/liver.jpg" width="1200" height="200" />
  </a>

  <h1>DLiPath(Histopathology images)</h1>
  Six pathological indicators for liver donor assessment.

  <p>
  Liangrui Pan et al. is a developer helper.
  </p>

  <p>
    <a href="https://github.com/misitebao/yakia/blob/main/LICENSE">
      <img alt="GitHub" src="https://img.shields.io/github/license/misitebao/yakia"/>
    </a>
  </p>

  <!-- <p>
    <a href="#">Installation</a> | 
    <a href="#">Documentation</a> | 
    <a href="#">Twitter</a> | 
    <a href="https://discord.gg/zRC5BfDhEu">Discord</a>
  </p> -->

  <div>
  <strong>
  <samp>

[English](README.md)

  </samp>
  </strong>
  </div>
</div>

# DLiPath: A Benchmark for the Comprehensive Evaluation of Donor Liver Based on Histopathological Image Datasets

## Table of Contents

<details>
  <summary>Click me to Open/Close the directory listing</summary>

- [Table of Contents](#table-of-contents)
- [Feature Preprocessing](#Feature-Preprocessing)
- [Feature Extraction](#Feature-Extraction)
- [Models](#Train-models)
- [Train Models](#Train-models)
- [Datastes](#Datastes)
- [Installation](#Installation)
- [License](#license)

</details>

## Feature Preprocessing

Use the pre-trained model for feature preprocessing and build the spatial topology of WSI.

### Feature Extraction

The original WSI needs permission from the Third Xiangya Hospital to be used. If WSI is used for commercial purposes, the dataset will be protected by law. We support the following 21 pre-trained foundation models to extract the feature representation of WSI. Please contact us by email before using. (Highly recommended!!)

| Patch Encoder         | Embedding Dim | Args                                                             | Link |
|-----------------------|---------------:|------------------------------------------------------------------|------|
| **UNI**               | 1024           | `--patch_encoder uni_v1 --patch_size 256 --mag 20`               | [MahmoodLab/UNI](https://huggingface.co/MahmoodLab/UNI) |
| **UNI2-h**             | 1536           | `--patch_encoder uni_v2 --patch_size 256 --mag 20`               | [MahmoodLab/UNI2-h](https://huggingface.co/MahmoodLab/UNI2-h) |
| **CONCH**             | 512            | `--patch_encoder conch_v1 --patch_size 512 --mag 20`             | [MahmoodLab/CONCH](https://huggingface.co/MahmoodLab/CONCH) |
| **CONCHv1.5**         | 768            | `--patch_encoder conch_v15 --patch_size 512 --mag 20`            | [MahmoodLab/conchv1_5](https://huggingface.co/MahmoodLab/conchv1_5) |
| **Virchow**           | 2560           | `--patch_encoder virchow --patch_size 224 --mag 20`              | [paige-ai/Virchow](https://huggingface.co/paige-ai/Virchow) |
| **Virchow2**          | 2560           | `--patch_encoder virchow2 --patch_size 224 --mag 20`             | [paige-ai/Virchow2](https://huggingface.co/paige-ai/Virchow2) |
| **Phikon**            | 768            | `--patch_encoder phikon --patch_size 224 --mag 20`               | [owkin/phikon](https://huggingface.co/owkin/phikon) |
| **Phikon-v2**         | 1024           | `--patch_encoder phikon_v2 --patch_size 224 --mag 20`            | [owkin/phikon-v2](https://huggingface.co/owkin/phikon-v2/) |
| **Prov-Gigapath**     | 1536           | `--patch_encoder gigapath --patch_size 256 --mag 20`             | [prov-gigapath](https://huggingface.co/prov-gigapath/prov-gigapath) |
| **H-Optimus-0**       | 1536           | `--patch_encoder hoptimus0 --patch_size 224 --mag 20`            | [bioptimus/H-optimus-0](https://huggingface.co/bioptimus/H-optimus-0) |
| **H-Optimus-1**       | 1536           | `--patch_encoder hoptimus1 --patch_size 224 --mag 20`            | [bioptimus/H-optimus-1](https://huggingface.co/bioptimus/H-optimus-1) |
| **MUSK**              | 1024           | `--patch_encoder musk --patch_size 384 --mag 20`                 | [xiangjx/musk](https://huggingface.co/xiangjx/musk) |
| **Midnight-12k**      | 3072           | `--patch_encoder midnight12k --patch_size 224 --mag 20`          | [kaiko-ai/midnight](https://huggingface.co/kaiko-ai/midnight) |
| **Kaiko**             | 384/768/1024   | `--patch_encoder {kaiko-vits8, kaiko-vits16, kaiko-vitb8, kaiko-vitb16, kaiko-vitl14} --patch_size 256 --mag 20` | [1aurent/kaikoai-models-66636c99d8e1e34bc6dcf795](https://huggingface.co/collections/1aurent/kaikoai-models-66636c99d8e1e34bc6dcf795) |
| **Lunit**             | 384            | `--patch_encoder lunit-vits8 --patch_size 224 --mag 20`          | [1aurent/vit_small_patch8_224.lunit_dino](https://huggingface.co/1aurent/vit_small_patch8_224.lunit_dino) |
| **Hibou**             | 1024           | `--patch_encoder hibou_l --patch_size 224 --mag 20`              | [histai/hibou-L](https://huggingface.co/histai/hibou-L) |
| **CTransPath-CHIEF**  | 768            | `--patch_encoder ctranspath --patch_size 256 --mag 10`           | — |
| **ResNet50**          | 1024           | `--patch_encoder resnet50 --patch_size 256 --mag 20`             | — |

For the related feature extraction process, please refer to: https://github.com/mahmoodlab/TRIDENT.



**Baseline MIL Methods**

This repository provides implementations and comparisons of various MIL-based methods for Whole Slide Image (WSI) classification.

- **ABMIL** : "https://github.com/AMLab-Amsterdam/AttentionDeepMIL"

- **CLAM-SB** : "https://github.com/mahmoodlab/CLAM"
  
- **CLAM-MB** : "https://github.com/mahmoodlab/CLAM"

- **ACMIL** : "https://github.com/dazhangyu123/ACMIL"

- **DSMIL** : "https://github.com/binli123/dsmil-wsi"
  
- **IBMIL** : "https://github.com/HHHedo/IBMIL"
  
- **DGRMIL** : "https://github.com/ChongQingNoSubway/DGR-MIL"
  
- **ILRA-MIL** : "https://github.com/ChongQingNoSubway/DGR-MIL"

- **TransMIL** : "https://github.com/szc19990412/TransMIL"


## Train Models
```markdown
python clam.py
```


## Datastes

- **Only features of the histopathology image data are provided as the data has a privacy protection agreement.**
```markdown

link：https://pan.baidu.com/s/115tVCSwUjrZm5y_rBND5NQ?pwd=v9kq 
password：v9kq

link：https://pan.baidu.com/s/14xl48HY933k4JGdYR-RoVw?pwd=v9kq 
password：v9kq

link：https://pan.baidu.com/s/10kXNJdIW3toFQG7dTdYxZg?pwd=v9kq 
password：v9kq

```
- **We provide a permanent link to the raw data at  https://pan.baidu.com/s/1cVYwHXsUCmEUw2LRRwUcRg?pwd=3rac, but we strongly recommend using the preprocessed WSI features.**

- **We provide raw svs data on DLiPath. The original data requires permission. Please contact the corresponding author (slpeng@hnu.edu.cn) or first author (panlr@hnu.edu.cn) by email!!**
- **DLiPath:** The main indicators of donor liver histopathological assessment include cholestasis, portal tract fibrosis, portal inflammation, total steatosis, macrovesicular steatosis, and hepatocellular ballooning. Multiple pathologists will score the histopathology images based on their years of diagnostic experience; if two junior pathologists agree on a score, that label is assigned. If their scores differ, a senior pathologist is consulted to make the final determination. Each indicator is graded on a multiple point scale: none, mild, moderate, and severe. The scoring criteria for these indicators are listed in the table below.

**Table: Histopathological Assessment Indicators for Post‑mortem Donor Liver Biopsy**

| Indicator                  | None | Mild                  | Moderate             | Severe         |
|----------------------------|:----:|:---------------------:|:--------------------:|:--------------:|
| Cholestasis                | None | Mild (5%–30%)         | Moderate (30%–50%)   | Severe (>50%)  |
| Portal tract fibrosis      | None | Mild                  | Moderate             | Severe         |
| Portal inflammation        | None | Mild                  | Moderate             | Severe         |
| Overall steatosis          | None | Mild (5%–30%)         | Moderate (30%–60%)   | Severe (>60%)  |
| Macrovesicular steatosis   | None | Mild (5%–30%)         | Moderate (30%–60%)   | Severe (>60%)  |
| Hepatocellular ballooning  | None | Mild (5%–30%)         | Moderate (30%–60%)   | Severe (>60%)  |

**Table: Label Distribution for Donor Liver Histopathology Assessment**

| Histological Feature            | **0** | **1** | **2** | **3** |
|---------------------------------|:-----:|:-----:|:-----:|:-----:|
| Cholestasis                     | 131   | 128   | 2     | 0     |
| Portal tract fibrosis           | 187   | 76    | 0     | 0     |
| Portal inflammation             | 233   | 29    | 1     | 0     |
| Total steatosis                 | 160   | 93    | 10    | 0     |
| Macrovesicular steatosis        | 184   | 66    | 12    | 1     |
| Hepatocellular ballooning       | 3     | 45    | 133   | 81    |

## Installation
- Linux (Tested on Ubuntu 18.04)
- NVIDIA GPU (Tested on a single Nvidia GeForce RTX 4090)
- Python (3.7.11), h5py (2.10.0), opencv-python (4.1.2.30), PyTorch (1.10.1), torchvision (0.11.2), pytorch-lightning (1.5.10).


## License
If you need the original histopathology image slides, please send a request to our email address. The email address will be announced after the paper is accepted. Thank you!

[License MIT](../LICENSE)
