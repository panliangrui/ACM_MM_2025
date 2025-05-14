

<div align="center">
  <a href="(https://github.com/panliangrui/NIPS2025/blob/main/liucheng.png)">
    <img src="https://github.com/panliangrui/NIPS2025/blob/main/liucheng.png" width="800" height="400" />
  </a>

  <h1>PathGene(NGS, Histopathology images)</h1>
  Flowchart of the collection and preprocessing of lung cancer patients’ histopathology images and NGS data.

  <p>
  Anonymous Author et al. is a developer helper.
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

# DLiPath: A Benchmark for the Comprehensive Evaluation of Graft Livers Based on Histopathological Image Datasets

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

- **ABMIL** is a deep multiple instance learning framework that employs an attention mechanism to aggregate instance-level features within a bag. By projecting instances into a low-dimensional feature space and applying a gated attention mechanism, ABMIL assigns dynamic weights to each instance, facilitating permutation-invariant aggregation. This approach enables end-to-end training for bag-level classification tasks, such as tumor grading, and provides interpretability by highlighting the contribution of individual instances to the overall prediction.

- **CLAM-SB** is a simplified variant of the CLAM framework, tailored for binary classification tasks. It utilizes a single attention branch to aggregate instance features, focusing on regions with high attention scores as evidence for the positive class. The model incorporates a combination of slide-level classification loss and instance-level clustering loss, enabling end-to-end training and enhancing the model's ability to distinguish between tumor and normal tissue.
  
- **CLAM-MB** extends the CLAM framework to handle multi-class classification tasks by employing multiple attention branches, each corresponding to a specific class. During training, the model generates pseudo-labels for each branch and applies clustering constraints to enforce class-specific feature learning. This design allows CLAM-MB to perform end-to-end bag-level classification while providing interpretable localization of class-relevant regions within whole-slide images.

- **ACMIL** is a multiple instance learning model designed to address the overfitting problem caused by excessive attention concentration in whole-slide image classification. Through UMAP and Top-K attention value statistical analysis, ACMIL introduces two innovative techniques into the ABMIL framework: Multiple Branch Attention (MBA) and Stochastic Top-K Instance Masking (STKIM). These techniques compel the model to focus on more predictive instances and alleviate attention concentration, significantly enhancing the model's generalization and robustness.

- **DSMIL** is a dual-stream attention-based multiple instance learning model. The first stream employs max pooling to select the most representative instance. The second stream calculates self-attention weights for all instances in the bag based on the selected instance and aggregates them. The model jointly learns an instance classifier and a bag classifier within the same embedding space, enabling end-to-end optimization.
  
- **IBMIL** introduces the "backdoor adjustment" strategy from causal inference into the MIL framework to achieve deconfounding of bag-level contextual prior biases. This approach enhances the robustness and generalization capability of bag-level classification by mitigating spurious correlations between bags and labels. IBMIL is orthogonal to existing MIL methods, allowing it to be integrated with various architectures to consistently improve performance.
  
- **DGRMIL** is a novel MIL aggregation method that models the diversity of instances within a bag through a set of learnable global vectors. It utilizes a cross-attention mechanism to measure the similarity between instance embeddings and global vectors, replacing traditional strategies that focus on instance correlations. The model further introduces a positive instance alignment module and a diversification learning paradigm based on determinantal point processes to enhance the global vectors' descriptive ability for the entire bag.
  
- **ILRA-MIL** is a specialized MIL model for whole slide images (WSIs) in pathology. It first employs Low-Rank Contrastive (LRC) learning to generate embeddings for specific pathological tissues. Subsequently, it introduces learnable low-rank latent vectors into a standard Transformer aggregation module, enabling iterative global interaction modeling among instances within a bag. This design captures the low-rank structure inherent in WSIs, facilitating more effective representation learning.

- **TransMIL** addresses the limitations of traditional MIL methods that assume independent and identically distributed (i.i.d.) instances by modeling correlations among instances within a bag. It segments WSIs into patches (instances), extracts features, and incorporates positional encoding before feeding them into multi-head self-attention Transformer layers. This architecture captures both morphological and spatial information. To mitigate the impact of noisy pixel-level annotations, TransMIL employs an efficient random masking strategy during mixed supervision training, enhancing the model's robustness to label noise. Experiments demonstrate that TransMIL achieves superior performance and faster convergence compared to state-of-the-art methods on datasets like CAMELYON16, TCGA-NSCLC, and TCGA-RCC.


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
