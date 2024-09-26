<p align="center">
  <img src="asserts/logo.png" alt="Logo" width="200"/>
</p>
<p align="center">
  <strong>Kai Li<sup>1</sup>, Wendi Sang<sup>1</sup>, Chang Zeng<sup>2</sup>, Runxuan Yang<sup>1</sup>, Guo Chen<sup>1</sup>, Xiaolin Hu<sup>1</sup></strong><br>
    <strong><sup>1</sup>Tsinghua University, China</strong><br>
    <strong><sup>2</sup>National Institute of Informatics, Japan</strong><br>
  <a href="#">Paper (Coming soon)</a> | <a href="https://cslikai.cn/SonicSim/">Demo</a>

<p align="center">
  <img src="https://visitor-badge.laobi.icu/badge?page_id=JusperLee.SonicSim" alt="访客统计" />
  <img src="https://img.shields.io/github/stars/JusperLee/SonicSim?style=social" alt="GitHub stars" />
  <img alt="Static Badge" src="https://img.shields.io/badge/license-CC_BY--NC--SA_4.0-blue">
</p>

<p align="center">


# SonicSim: A customizable simulation platform for speech models in moving sound source scenarios

We introduce SonicSim, a synthetic toolkit designed to generate highly customizable data for moving sound sources. SonicSim is developed based on the embodied AI simulation platform, Habitat-sim, supporting multi-level parameter adjustments, including scene-level, microphone-level, and source-level, thereby generating more diverse synthetic data. Leveraging SonicSim, we constructed a moving sound source benchmark dataset, SonicSet, using the LibriSpeech dataset, the Freesound Dataset 50k (FSD50K) and Free Music Archive (FMA), and 90 scenes from the Matterport3D to evaluate speech separation and enhancement models. 

## 🔥 News

- [2024-07-31] We release the SonicSim dataset, which includes speech separation and enhancement tasks.

- [2024-07-24] We release the scripts for `dataset construction` and the pre-trained models for `speech separation and enhancement`.

## <img src="asserts/logo.png" alt="Logo" width="5%"/> SonicSim Platform

![](./files/overview-sim.png)

-	3D Scene Import: Supports importing a variety of 3D assets from datasets like Matterport3D, enabling efficient and scalable generation of complex acoustic environments.

-	Acoustic Environment Simulation:
	1.	Simulates sound reflections within room geometries using indoor acoustic modeling and bidirectional path tracing algorithms.
	2.	Maps semantic labels of 3D scenes to material properties, setting the absorption, scattering, and transmission coefficients of surfaces.
	3.	Synthesizes moving sound source data based on source paths, ensuring high fidelity to real-world conditions.

-	Microphone Configurations: Offers a wide range of microphone setups, including mono, binaural, and Ambisonics, along with support for custom linear and circular microphone arrays.

-	Source and Microphone Positioning: Provides customization or randomization of sound source and microphone positions. Supports motion trajectories for moving sound source simulations, adding realism to dynamic acoustic scenarios.

## <img src="asserts/monitoring.png" alt="Logo" width="5%"/> SonicSet Dataset

![](./files/SonicSet.png)

You can download the pre-constructed dataset from the following link:

### 🔈 Speech Separation and 🔕 Speech Enhancement

| Dataset Name | Onedrive | Baidu Disk |
|-----|-----|-----|
| train folder (40 split rar files, 377G) | [[Download Link](https://1drv.ms/f/c/ba3b81b8a2ef83ae/EsO9TFmnSdNMohY3fYYQu7YBV8LasO-EmkpKEN10dXAl7g?e=n4z3io)] | [[Download Link](https://pan.baidu.com/s/1gC2LVErchEkO7ENdNOIb0A?pwd=c9gw)] |
| val.rar (4.9G) | [[Download Link](https://1drv.ms/u/c/ba3b81b8a2ef83ae/EX9938DRcx5NhfMfKdNq6NgBVcRdNnjF4syTWhetGa8sew?e=EnEtVn)] | [[Download Link](https://pan.baidu.com/s/11oybiPkFwihj9DZI0H_-vw?pwd=j36i)] |
| test.rar (2.2G) | [[Download Link](https://1drv.ms/u/c/ba3b81b8a2ef83ae/EeyzjZ9MgeJJsmAfdGTyGCEBMBtwjamGIDLkNLVMU1t2_w?e=KNJRoM)] | [[Download Link](https://pan.baidu.com/s/1GEcvmOs0VyP23v5gBfGREg?pwd=pyyf)] |
| sep-benchmark data (8.57G) | [[Download Link](https://1drv.ms/f/c/ba3b81b8a2ef83ae/EvDfTqiuSUxCrLKKcFpfGfIBeIgIvHuQkiuvcGBPjplcFg?e=ZeD7Kj)] | [[Download Link](https://pan.baidu.com/s/11oJ457YTA91gDgsVlWlaJA?pwd=kq79)] |
| enh-benchmark data (7.70G) | [[Download Link](https://1drv.ms/f/c/ba3b81b8a2ef83ae/EmMlMKMYRIVOiYQrRbHIU5wBt52R-Ej5-KdUuzZWsOFb0Q?e=pi05ve)] | [[Download Link](https://pan.baidu.com/s/15QHCdVwhTL_UipvgwAxLCg?pwd=x46b)] |

## <img src="asserts/monitoring.png" alt="Logo" width="5%"/> Dataset Construction

![](./files/sonicset-pipeline.png)

To construct the dataset yourself, please refer to the README in the `SonicSim-SonicSet/data-script` folder. This document provides detailed instructions on how to use the scripts provided to generate the dataset.

## 🕹️ Environment Setup for Training and Inference

### Conda Environment Setup

To set up the environment for training and inference, use the provided YAML file:

```bash
conda env create -f SonicSim/torch-2.0.yml
conda activate SonicSim
```

### Download Checkpoints

Please check the contents of README.md in the [sep-checkpoints](https://github.com/JusperLee/SonicSim/tree/main/sep-checkpoints) and [enh-checkpoints](https://github.com/JusperLee/SonicSim/tree/main/enh-checkpoints) folders, download the appropriate pre-trained models in `Release` and unzip them into the appropriate folders.

### Speech Separation Inference

Navigate to the `separation` directory and run the inference script with the specified configuration file:

```bash
cd separation
python inference.py --conf_dir=../sep-checkpoints/TFGNet-Noise/config.yaml
```

### Speech Enhancement Inference

Navigate to the `enhancement` directory and run the inference script with the specified configuration file:

```bash
cd enhancement
python inference.py --conf_dir=../enh-checkpoints/TaylorSENet-Noise/config.yaml
```

## 🏆 Leaderboard

We have trained separation and enhancement models on the SonicSim dataset. The results are as follows:

### 🔈 Speech Separation (Only two speakers)

#### Noise Environment

| Model            | SI-SNR | SDR   | NB-PESQ | WB-PESQ | STOI  | MOS_NOISE | MOS_REVERB | MOS_SIG | MOS_OVRL | WER (%) |
|------------------|--------|-------|---------|---------|-------|-----------|------------|---------|----------|---------|
| Conv-TasNet | 4.81   | 7.13  | 2.00    | 1.46    | 0.73  | 2.45      | 3.04       | 2.30    | 2.10     | 53.82   |
| DPRNN       | 4.87   | 6.65  | 2.17    | 1.63    | 0.77  | 2.54      | 3.28       | 2.47    | 2.11     | 47.81   |
| DPTNet      | 11.51  | 13.00 | 2.82    | 2.35    | 0.87  | 3.00      | 3.15       | 2.68    | 2.32     | 28.13   |
| SuDoRM-RF   | 8.01   | 9.70  | 2.47    | 1.98    | 0.81  | 2.95      | 3.26       | 2.63    | 2.25     | 35.61   |
| A-FRCNN     | 9.17   | 10.63 | 2.70    | 2.16    | 0.84  | 2.98      | 3.24       | 2.72    | 2.32     | 35.44   |
| TDANet      | 9.27   | 11.00 | 2.72    | 2.22    | 0.85  | 3.05      | 3.22       | 2.74    | 2.36     | 30.46   |
| SKIM        | 7.23   | 8.78  | 2.34    | 1.86    | 0.79  | 2.65      | 3.23       | 2.47    | 2.11     | 38.92   |
| BSRNN       | 9.10   | 10.86 | 2.82    | 2.26    | 0.85  | 2.93      | 3.11       | 2.84    | 2.45     | 29.86   |
| TF-GridNet  | 15.38  | 16.81 | 3.58    | 3.08    | 0.93  | 3.11      | 3.10       | 2.91    | 2.49     | 12.04   |
| Mossformer  | 14.72  | 15.97 | 3.02    | 2.67    | 0.91  | 3.11      | 3.24       | 2.76    | 2.39     | 21.10   |
| Mossformer2 | 14.84  | 16.09 | 3.17    | 2.83    | 0.91  | 3.20      | 3.21       | 2.78    | 2.40     | 19.51   |

#### Music Environment

| Model            | SI-SNR | SDR   | NB-PESQ | WB-PESQ | STOI  | MOS_NOISE | MOS_REVERB | MOS_SIG | MOS_OVRL | WER (%) |
|------------------|--------|-------|---------|---------|-------|-----------|------------|---------|----------|---------|
| Conv-TasNet | 4.12   | 5.38  | 1.84    | 1.42    | 0.65  | 1.98      | 3.53       | 2.21    | 1.81     | 63.21   |
| DPRNN       | 4.37   | 5.73  | 1.98    | 1.50    | 0.73  | 2.47      | 3.28       | 2.45    | 2.07     | 51.33   |
| DPTNet      | 11.69  | 12.80 | 2.67    | 2.13    | 0.84  | 2.91      | 3.14       | 2.54    | 2.23     | 29.05   |
| SuDoRM-RF   | 6.84   | 8.34  | 2.15    | 1.66    | 0.77  | 2.80      | 3.28       | 2.48    | 2.12     | 41.37   |
| A-FRCNN     | 7.59   | 9.32  | 2.52    | 2.00    | 0.82  | 2.94      | 3.24       | 2.67    | 2.29     | 33.82   |
| TDANet      | 7.00   | 8.68  | 2.26    | 1.71    | 0.79  | 2.71      | 3.25       | 2.58    | 2.19     | 37.16   |
| SKIM        | 6.00   | 7.42  | 2.23    | 1.75    | 0.77  | 2.63      | 3.29       | 2.44    | 2.10     | 42.82   |
| BSRNN       | 6.96   | 8.66  | 2.36    | 1.76    | 0.79  | 2.54      | 3.13       | 2.79    | 2.32     | 41.73   |
| TF-GridNet  | 14.37  | 15.69 | 3.45    | 2.84    | 0.91  | 3.31      | 3.15       | 2.96    | 2.58     | 14.43   |
| Mossformer  | 11.80  | 13.17 | 2.82    | 2.26    | 0.86  | 3.05      | 3.28       | 2.61    | 2.25     | 26.64   |
| Mossformer2 | 11.12  | 12.34 | 2.62    | 2.09    | 0.83  | 2.87      | 3.31       | 2.55    | 2.20     | 32.65   |


#### Efficiency Metrics

| Model            | Params (M) | MACs (G/s) | CPU Inference (1s, ms) | GPU Inference (1s, ms) | Inference GPU Memory (1s, MB) | Backward GPU (1s, ms) | Backward GPU Memory (1s, MB) |
|------------------|------------|------------|------------------------|------------------------|----------------------|-----------------------|----------------------|
| Conv-TasNet | 5.62       | 10.23      | 71.67                  | 8.59                   | 134.34               | 42.34                 | 647.22               |
| DPRNN       | 2.72       | 43.79      | 379.49                 | 15.88                  | 285.49               | 38.57                 | 1757.00              |
| DPTNet      | 2.80       | 53.37      | 481.37                 | 20.04                  | 20.67                | 58.28                 | 3120.22              |
| SuDoRM-RF   | 2.72       | 4.60       | 87.81                  | 17.83                  | 138.94               | 68.40                 | 1058.76              |
| A-FRCNN     | 6.13       | 81.20      | 102.22                 | 36.19                  | 157.20               | 128.40                | 1141.86              |
| TDANet      | 2.33       | 9.13       | 169.47                 | 32.88                  | 145.56               | 89.62                 | 3064.75              |
| SKIM        | 5.92       | 21.92      | 245.98                 | 10.54                  | 273.07               | 38.62                 | 1083.77              |
| BSRNN       | 25.97      | 123.10     | 577.11                 | 59.78                  | 135.48               | 184.26                | 2349.62              |
| TF-GridNet  | 14.43      | 525.68     | 1525.98                | 64.59                  | 615.04               | 165.55                | 6687.60              |
| Mossformer  | 42.10      | 85.54      | 473.74                 | 49.71                  | 163.68               | 153.84                | 4385.91              |
| Mossformer2 | 55.74      | 112.67     | 830.66                 | 93.33                  | 163.52               | 297.07                | 5617.39              |

### 🔕 Speech Enhancement

#### Noise Environment

| Model            | SI-SNR | SDR   | NB-PESQ | WB-PESQ | STOI  | MOS_NOISE | MOS_REVERB | MOS_SIG | MOS_OVRL | WER (%) |
|------------------|--------|-------|---------|---------|-------|-----------|------------|---------|----------|---------|
| DCCRN            | 8.41   | 11.29 | 2.81    | 2.17    | 0.87  | 2.94      | 3.01       | 2.80    | 2.39     | 21.78   |
| Fullband         | 7.82   | 8.34  | 3.05    | 2.34    | 0.89  | 3.30      | 3.04       | 2.95    | 2.54     | 22.04   |
| FullSubNet       | 9.48   | 11.92 | 3.19    | 2.48    | 0.90  | 3.24      | 3.05       | 2.98    | 2.54     | 20.01   |
| Fast-FullSubNet  | 8.14   | 8.71  | 3.13    | 2.41    | 0.90  | 3.31      | 3.05       | 2.99    | 2.58     | 21.13   |
| FullSubNet+      | 8.93   | 11.07 | 3.06    | 2.35    | 0.89  | 3.12      | 2.97       | 2.91    | 2.47     | 20.73   |
| TaylorSENet      | 10.11  | 12.67 | 3.07    | 2.45    | 0.89  | 2.72      | 3.01       | 2.65    | 2.22     | 21.61   |
| GaGNet           | 10.01  | 12.78 | 3.12    | 2.48    | 0.89  | 2.77      | 3.05       | 2.64    | 2.23     | 21.40   |
| G2Net            | 9.82   | 12.22 | 3.03    | 2.39    | 0.89  | 2.78      | 3.00       | 2.64    | 2.22     | 22.02   |
| Inter-SubNet     | 10.34  | 12.87 | 3.32    | 2.61    | 0.91  | 3.39      | 3.10       | 3.05    | 2.62     | 18.83   |
| SudoRMRF         | 11.28  | 13.35 | 2.75    | 2.20    | 0.87  | 3.64      | 2.88       | 2.80    | 1.88     | 93.54   |


#### Music Environment

| Model            | SI-SNR | SDR   | NB-PESQ | WB-PESQ | STOI  | MOS_NOISE | MOS_REVERB | MOS_SIG | MOS_OVRL | WER (%)
|------------------|--------|-------|---------|---------|-------|-----------|------------|---------|----------|---------|
| DCCRN            | 11.56  | 11.98 | 2.72    | 2.00    | 0.85  | 3.30      | 3.51       | 2.94    | 2.59     | 25.13 |
| Fullband         | 10.07  | 11.098| 2.80    | 2.02    | 0.86  | 3.13      | 2.99       | 2.88    | 2.46     | 25.27 |
| FullSubNet       | 11.60  | 12.31 | 3.10    | 2.22    | 0.88  | 3.34      | 3.08       | 3.05    | 2.63     | 20.82 |
| Fast-FullSubNet  | 10.36  | 11.24 | 2.93    | 2.08    | 0.87  | 3.22      | 3.03       | 2.93    | 2.51     | 24.98 |
| FullSubNet+      | 10.64  | 11.50 | 2.80    | 1.99    | 0.86  | 3.02      | 2.93       | 2.82    | 2.38     | 24.11 |
| TaylorSENet      | 12.18  | 13.04 | 3.06    | 2.33    | 0.88  | 2.76      | 2.92       | 2.65    | 2.24     | 23.46 |
| GaGNet           | 12.20  | 13.17 | 2.95    | 2.27    | 0.87  | 2.78      | 2.86       | 2.64    | 2.21     | 23.36 |
| G2Net            | 12.14  | 13.13 | 3.00    | 2.32    | 0.88  | 2.80      | 2.88       | 2.64    | 2.23     | 22.96 |
| Inter-SubNet     | 12.07  | 13.01 | 3.15    | 2.28    | 0.88  | 3.34      | 3.11       | 3.04    | 2.64     | 20.07 |
| SudoRMRF         | 12.99  | 13.86 | 2.61    | 2.01    | 0.85  | 3.91      | 2.80       | 2.98    | 1.93     | 88.72 |

#### Efficiency Metrics

| Model            | Params (M) | MACs (G/s) | CPU Inference (1s, ms) | GPU Inference (1s, ms) | Inference GPU Memory (1s, MB) | Backward GPU (1s, ms) | Backward GPU Memory (1s, MB) |
|------------------|------------|------------|------------------------|------------------------|----------------------|-----------------------|----------------------|
| DCCRN            | 3.67       | 14.38      | 98.42                  | 5.81                   | 30.42                | 35.42                 | 124.66               |
| Fullband         | 6.05       | 0.39       | 5.98                   | 1.99                   | 23.01                | 10.21                 | 73.39                |
| FullSubNet       | 5.64       | 30.87      | 58.46                  | 3.66                   | 144.21               | 15.25                 | 491.20               |
| Fast-FullSubNet  | 6.84       | 4.14       | 12.33                  | 4.63                   | 26.75                | 20.12                 | 111.45               |
| FullSubNet+      | 8.66       | 31.11      | 110.44                 | 9.50                   | 147.02               | 37.40                 | 521.49               |
| TaylorSENet      | 5.40       | 6.15       | 70.96                  | 26.84                  | 139.33               | 76.63                 | 329.40               |
| GaGNet           | 5.95       | 1.66       | 66.72                  | 29.72                  | 129.59               | 84.05                 | 226.49               |
| G2Net            | 7.39       | 2.85       | 98.29                  | 47.56                  | 130.33               | 162.51                | 291.98               |
| Inter-SubNet     | 2.29       | 36.71      | 78.81                  | 4.40                   | 216.91               | 14.59                 | 725.93               |
| SudoRMRF         | 2.70       | 2.12       | 42.43                  | 11.42                  | 8.52                 | 52.59                 | 293.44               |


## Acknowledgements

We would like to express our gratitude to the following:

- [LibriSpeech](http://www.openslr.org/12) for providing the speech data.
- [SoundSpaces](https://github.com/facebookresearch/sound-spaces) for the simulation environment.
- Apple for providing dynamic audio synthesis scripts.

## Citation

If you use this dataset in your research, please cite our repository as follows:

```
@misc{SonicSim2024,
  title={SonicSim: A Simulated Audio Dataset for Speech Enhancement and Separation},
  author={Kai Li, Wendi Sang, Chang Zeng, Runxuan Yang, Guo Chen, Xiaolin Hu},
  year={2024},
  publisher = {GitHub}
}
```

Thank you for using SonicSim! We hope it helps advance your research in speech enhancement and separation. For any questions or issues, please open an issue in our GitHub repository.

## Contact

If you have any concerns or technical problems, please contact `tsinghua.kaili@gmail.com`.

## License

This dataset is licensed under the [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) license.
