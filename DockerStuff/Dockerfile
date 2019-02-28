FROM ubuntu:18.04

# update
#RUN apt-get update
#RUN apt-get upgrade -y

# basic
RUN apt-get install -y git wget zsh vim

# only install python3 
# install python3 and pip3 and map to python and pip RUN apt-get install -y python3
RUN ln -s /usr/bin/python3.6 /usr/bin/python
RUN apt-get update --fix-missing
RUN apt-get install -y python3-pip
RUN ln -s /usr/bin/pip3 /usr/bin/pip

# install some basic pip packages
RUN pip install ipython
RUN pip install r2pipe
RUN pip install git+https://github.com/arthaud/python3-pwntools.git
RUN pip install frida-tools

# developing
RUN apt-get install -y make gcc g++ cmake

# install oh-my-zsh with autosuggestions
RUN wget https://github.com/robbyrussell/oh-my-zsh/raw/master/tools/install.sh -O - | zsh || true
RUN sed -i -e 's/THEME="robbyrussell"/THEME="avit"/g' /root/.zshrc
RUN git clone https://github.com/zsh-users/zsh-autosuggestions ~/.zsh/zsh-autosuggestions
RUN echo 'source ~/.zsh/zsh-autosuggestions/zsh-autosuggestions.zsh' >> /root/.zshrc
RUN echo 'cd /root' >> /root/.zshrc


################################################################################
# Basic Tools
################################################################################

# make gitrepo directory
RUN mkdir /root/git-repos

# install r2
RUN git clone https://github.com/radare/radare2.git /root/git-repos/radare2
RUN ./root/git-repos/radare2/sys/install.sh

# install keystone from source
RUN git clone https://github.com/keystone-engine/keystone.git /root/git-repos/keystone
RUN mkdir /root/git-repos/keystone/build
RUN cd /root/git-repos/keystone/build && ../make-share.sh && make install
RUN cd /root/git-repos/keystone/bindings/python && make install
RUN ln -s /root/git-repos/keystone/build/llvm/lib/libkeystone.so /usr/local/lib/python3.6/dist-packages/keystone

# install capstone from source
RUN git clone https://github.com/aquynh/capstone.git /root/git-repos/capstone
RUN cd /root/git-repos/capstone && ./make.sh
RUN cd /root/git-repos/capstone && ./make.sh install
RUN cd /root/git-repos/capstone/bindings/python && make install

# install unicorn (it needs python2.x for installation)
# Note: python3 is not tested, for installation it needs python2 (28.2.2019)
# but it worked with my code snippets so I will try with python3
RUN git clone https://github.com/unicorn-engine/unicorn.git /root/git-repos/unicorn
RUN apt-get install -y python
RUN cd /root/git-repos/unicorn && ./make.sh
RUN cd /root/git-repos/unicorn && ./make.sh install
RUN apt-get remove -y python2.7
RUN apt-get autoremove -y
RUN ln -s /usr/bin/python3.6 /usr/bin/python
RUN cd /root/git-repos/unicorn/bindings/python && make install3

# install binwalk
#RUN git clone https://github.com/ReFirmLabs/binwalk.git /root/git-repos/binwalk
#RUN cd /root/git-repos/binwalk && python setup.py install
#RUN pip install pylzma

# install Triton
#https://github.com/JonathanSalwan/Triton/


################################################################################
# Reversing ARM-Binaries ToolChain
################################################################################

RUN apt-get install -y qemu
RUN apt-get install -y gcc-arm-linux-gnueabi g++-arm-linux-gnueabi

# Tested with:
# qemu-arm -singlestep -L /usr/arm-linux-gnueabi/ -g 1234 <binary> <args>  &
# r2 -a arm -b 32 -d gdb://127.0.0.1:1234
# works for static and dynamic linked binaries
# don't forget to add -L /usr/arm-linux-gnueabi for dynimcally linked binaries

