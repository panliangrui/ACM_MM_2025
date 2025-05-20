

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
link: https://pan.baidu.com/s/1-V1Zb1YJ65wb4Fhh7SJbkw?pwd=4xep password: 4xep
```
- **We provide a permanent link to the raw data at https://pan.baidu.com/s/14NAjUSu78OKQHPEWz082lA?pwd=5gux, but we strongly recommend using the preprocessed WSI features.**

- **We provide raw NGS data on PathGene. The datasets_csv folder contains the labels corresponding to the driver genes we processed and can be used directly. The original NGS requires permission. Please contact the corresponding author (slpeng@hnu.edu.cn) or first author (panlr@hnu.edu.cn) by email!!**
- **PathGene-CSU:** The PathGene‐CSU cohort comprises 1,576 lung cancer patients, predominantly diagnosed with adenocarcinoma or adenosquamous carcinoma (For related content, please refer to Table 8 in the appendix of this article.). All cases underwent NGS, yielding per‐patient labels for driver‐gene mutation status, mutation subtypes, and exon‐level variant locations. We focus on five prediction tasks (For related content, please refer to Table 9 in the appendix of this article): (1) binary mutation status (presence/absence) for TP53, EGFR, KRAS, and ALK; (2) TP53 mutation subtype (wild‐type, nonsense, missense); (3) TP53 exon hotspots (EX5, EX6, EX7, EX8, other) based on functional‐domain distribution; (4) EGFR exon variants (EX19, EX20, EX21), chosen for their mutation frequency, TKI sensitivity, and clinical response differences; and (5) binary TMB status (high/low; 9 mut/Mb cutoff). For KRAS, we consolidate EX3 and rarer exons into an “other” category due to low sample counts. ALK subtypes are divided into EML4–ALK fusions and non‐fusion point mutations, reflecting the availability of fusion‐targeted therapies.

- **PathGene-TCGA_LUAD:** This dataset includes 510 WSIs from 448 TCGA lung adenocarcinoma cases. Multiple sections from the same tumor share identical NGS profiles. We retrieved driver‐gene labels from cBioPortal and define mutation status as 0/1 and TMB status (high/low) at a 10 mut/Mb threshold. TP53 subtypes were reclassified by pathologists as wild type/nonsense mutation/missense mutation. Exon‐level prediction was not evaluated here owing to insufficient per‐exon sample sizes (total counts: 296, 75, 29, 48).


## Installation
- Linux (Tested on Ubuntu 18.04)
- NVIDIA GPU (Tested on a single Nvidia GeForce RTX 4090)
- Python (3.7.11), h5py (2.10.0), opencv-python (4.1.2.30), PyTorch (1.10.1), torchvision (0.11.2), pytorch-lightning (1.5.10).


## License
If you need the original histopathology image slides, please send a request to our email address. The email address will be announced after the paper is accepted. Thank you!

[License MIT](../LICENSE)
