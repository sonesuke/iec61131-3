# how to setup

# llvm install

## setup enviroment
```
sudo apt-get install make
sudo apt-get install gcc g++
sudo apt-get install libtool
sudo apt-get install m4 autoconf automake texinfo
sudo apt-get install graphviz xdot
```

## compile llvm

```
wget http://llvm.org/releases/3.2/llvm-3.2.src.tar.gz
wget http://llvm.org/releases/3.2/clang-3.2.src.tar.gz
wget http://llvm.org/releases/3.2/compiler-rt-3.2.src.tar.gz

tar xvf llvm-3.2.src.tar.gz
tar xvf clang-3.2.src.tar.gz
tar xvf compiler-rt-3.2.src.tar.gz

mkdir ~/llvm/
mv llvm-3.2-src ~/llvm/
mv clang-3.2-src ~/llvm/llvm-3.2.src/tools/clang
mv compiler-rt-3.2-src ~/llvm/llvm-3.2.src/projects/compiler-rt

mkdir ~/llvm/llvm-build/
cd ~/llvm/llvm-build/

../llvm-3.2/src/configure --prefix=/usr/local/llvm --enable-optimized

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



