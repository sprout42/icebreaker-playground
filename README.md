# Notes to myself
## Installing nMigen & Friends
This is just a copy of the official nMigen install instructions 
(https://nmigen.info/nmigen/latest/install.html), but I like keeping such things 
in my notes

### Yosys
```
git clone https://github.com/YosysHQ/yosys.git
pushd yosys
make PREFIX=$HOME/.local clang-config
make PREFIX=$HOME/.local -j$(nproc)
make PREFIX=$HOME/.local install
popd
```

### IceStorm
```
git clone https://github.com/YosysHQ/icestorm.git cd icestorm
pushd icestorm
make PREFIX=$HOME/.local -j$(nproc)
make PREFIX=$HOME/.local install
popd
```

### nextpnr
```
git clone https://github.com/YosysHQ/nextpnr
pushd nextpnr
mkdir build && cd build
cmake -DICESTORM_INSTALL_PREFIX=$HOME/.local -DCMAKE_INSTALL_PREFIX=$HOME/.local -DARCH=ice40 ..
make -j$(nproc)
make install
popd
```

### nMigen
```
pip install --upgrade git+https://github.com/nmigen/nmigen.git#egg=nmigen
pip install --upgrade git+https://github.com/nmigen/nmigen-boards.git#egg=nmigen-boards
pip install --upgrade git+https://github.com/nmigen/nmigen-stdio.git#nmigen-stdio
pip install --upgrade git+https://github.com/nmigen/nmigen-soc.git#nmigen-soc
```

### Optional
#### WebAssembly tools (instead of native Yosys tools)
Most likely would need to install the git versions of these tools, but just 
keeping this here for reference.
```
pip install nmigen-yosys yowasp-yosys yowasp-nextpnr-ice40-5k yowasp-nextpnr-ice40-8k
```

#### Glasgow
Glasgow is icebreaker of course, but similar enough to be a useful guide and 
reference.
```
git clone https://github.com/GlasgowEmbedded/glasgow
pushd glasgow/software
python setup.py develop --prefix=$HOME/.local
popd
```
