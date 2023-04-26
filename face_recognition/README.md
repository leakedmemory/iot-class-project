# Face Recognition

## Neural Network

The neural network used in this project can be found in this paper:
[Siamese Neural Networks for One-shot Image Recognition](https://www.cs.cmu.edu/~rsalakhu/papers/oneshot1.pdf).

## Dataset for data training

[Labeled Faces in the Wild](https://vis-www.cs.umass.edu/lfw/) was the dataset
used for training our project's model. This dataset is NOT meant to be used in
a real commercial use, more information about the disclaimer can be found
in the previously mentioned link.

## Requirements

All of the requirementes below are needed because of the [TensorFlow](https://tensorflow.org/)
package and were taken from [tensorflow installation guide](https://www.tensorflow.org/install/pip).

### System requirementes

- Ubuntu 16.04 or higher (64-bit)
- macOS 10.12.6 (Sierra) or higher (64-bit) *(no GPU support)*
- Windows Native: Windows 7 or higher (64-bit) *(no GPU support after TensorFlow 2.10)*
- Windows WSL2: Windows 10 19044 or higher (64-bit)

### Hardware requirements

- NVIDIA&reg; GPU card with CUDA&reg; architectures 3.5, 5.0, 6.0, 7.0, 7.5, 8.0
and higher. See the list of [CUDA&reg;-enabled GPU cards](https://developer.nvidia.com/cuda-gpus).
- For GPUs with unsupported CUDA&reg; architectures, or to avoid JIT compilation
from PTX, or to use different versions of the NVIDIA&reg; libraries, see the
[Linux build from source](https://www.tensorflow.org/install/source) guide.
- Packages do not contain PTX code except for the latest supported CUDA&reg;
architecture; therefore, TensorFlow fails to load on older GPUs when
`CUDA_FORCE_PTX_JIT=1` is set. (See [Application Compatibility](https://docs.nvidia.com/cuda/cuda-c-programming-guide/index.html#application-compatibility) for details.)

### Software requirements

- [Python](https://www.python.org/) 3.8-3.11
- [pip](https://pip.pypa.io/en/stable/) version 19.0 or higher for Linux (requires `manylinux2014` support) and
Windows.pip version 20.3 or higher for macOS.
- Windows Native Requires [Microsoft Visual C++ Redistributable for Visual Studio 2015, 2017 and 2019](https://learn.microsoft.com/pt-br/cpp/windows/latest-supported-vc-redist?view=msvc-170)

If you want to use NVIDIA&reg; GPU to speed up your trainig, the follow are required:

- [NVIDIA&reg; GPU drivers](https://www.nvidia.com/download/index.aspx?lang=en-us) version 450.80.02 or higher
- [CUDA&reg; Toolkit 11.8](https://developer.nvidia.com/cuda-toolkit-archive)
- [cuDNN SDK 8.6.0](https://developer.nvidia.com/cudnn)
- [TensorRT](https://docs.nvidia.com/deeplearning/tensorrt/archives/index.html#trt_7) to improve latency and throughput for inference *(optional)*

## Package dependencies

You will need to install the following packages if you want to test it on your
machine:

- [TensorFlow](https://tensorflow.org/)

NOTE: this install process is on linux and Windows WSL2. If you use other OS, please find what
better suites for you [here](https://www.tensorflow.org/install/pip).
```zsh
conda install -c conda-forge cudatoolkit=11.8.0
python3 -m pip install nvidia-cudnn-cu11==8.6.0.163 tensorflow==2.12.*
mkdir -p $CONDA_PREFIX/etc/conda/activate.d
echo 'CUDNN_PATH=$(dirname $(python -c "import nvidia.cudnn;print(nvidia.cudnn.__file__)"))' >> $CONDA_PREFIX/etc/conda/activate.d/env_vars.sh
echo 'export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$CONDA_PREFIX/lib/:$CUDNN_PATH/lib' >> $CONDA_PREFIX/etc/conda/activate.d/env_vars.sh
source $CONDA_PREFIX/etc/conda/activate.d/env_vars.sh

# Verify install:
python3 -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"
```

- [Matplotlib](https://matplotlib.org/)
```zsh
pip install matplotlib
```

- [OpenCV](https://opencv.org/) (python version)
```zsh
pip install opencv-python
```

- [python-dotenv](https://saurabh-kumar.com/python-dotenv/)
```zsh
pip install python-dotenv
```

## Usage

**TODO!**
