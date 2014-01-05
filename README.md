# how to setup

# llvm install

## setup enviroment
```
mkdir ~/llvm
cd ~/llvm
```

```
sudo apt-get install make
sudo apt-get install gcc g++
sudo apt-get install libtool
sudo apt-get install m4 autoconf automake texinfo
sudo apt-get install graphviz xdot
sudo apt-get install cmake
```

## compile llvm 3.4

```
wget http://llvm.org/releases/3.4/llvm-3.4.src.tar.gz
wget http://llvm.org/releases/3.4/clang-3.4.src.tar.gz
wget http://llvm.org/releases/3.4/compiler-rt-3.4.src.tar.gz
wget http://llvm.org/releases/3.4/lld-3.4.src.tar.gz

tar xvf llvm-3.4.src.tar.gz
tar xvf clang-3.4.src.tar.gz
tar xvf compiler-rt-3.4.src.tar.gz
tar xvf lld-3.4.src.tar.gz

mv clang-3.4 llvm-3.4/tools/clang
mv lld-3.4 llvm-3.4/tools/lld
mv compiler-rt-3.4 llvm-3.4/projects/compiler-rt


mkdir llvm-build/
cd llvm-build/

cmake -DCMAKE_INSTALL_PREFIX=/usr/local/llvm -DCMAKE_CXX_FLAGS:STRING=-std=c++11 -G "Unix Makefiles" ../llvm-3.4

REQUIRES_RTTI=1 make -j4
sudo make install

echo "export PATH=$PATH:/usr/local/llvm/bin/
```

## compile llvm 3.2

```
wget http://llvm.org/releases/3.2/llvm-3.2.src.tar.gz
wget http://llvm.org/releases/3.2/clang-3.2.src.tar.gz
wget http://llvm.org/releases/3.2/compiler-rt-3.2.src.tar.gz

tar xvf llvm-3.2.src.tar.gz
tar xvf clang-3.2.src.tar.gz
tar xvf compiler-rt-3.2.src.tar.gz

mv clang-3.2 llvm-3.2.src/tools/clang
mv compiler-rt-3.2 llvm-3.2.src/projects/compiler-rt


mkdir llvm-build/
cd llvm-build/

cmake -DCMAKE_INSTALL_PREFIX=/usr/local/llvm -DCMAKE_CXX_FLAGS:STRING=-std=c++11 -G "Unix Makefiles" ../llvm-3.2.src

REQUIRES_RTTI=1 make -j4
sudo make install

echo "export PATH=$PATH:/usr/local/llvm/bin/
```
## install llvmpy

```
sudo apt-get install python-dev
cd ~/llvm
git clone https://github.com/llvmpy/llvmpy.git
cd llvmpy

LLVM_CONFIG_PATH=/usr/local/llvm/bin/llvm-config python setup.py install
```

# install pyparsing

```
pip install pyparsing
```

# memo

```
clang -S -emit-llvm hoge.c
llc -march=arm -mcpu=cortex-a8 hoge.s 
```

# QEMU

http://wwwdantyo.wordpress.com/qemuでarm環境を手にいれる/

sudo apt-get install gcc-4.8-arm-linux-gnueabi g++-4.8-arm-linux-gnueabi
sudo apt-get install qemu
sudo apt-get install qemu-kvm-extras
