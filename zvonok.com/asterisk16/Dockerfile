FROM centos:centos7
LABEL authors="hes88@mail.ru, kud.rom.sh@gmail.com"

RUN yum -y upgrade
RUN yum -y install \
kernel-headers gcc gcc-c++ cpp bzip2 patch \
ncurses ncurses-devel libxml2 libxml2-devel \
sqlite sqlite-devel openssl-devel newt-devel \
kernel-devel libuuid-devel net-snmp-devel unixODBC \
unixODBC-devel mysql-connector-odbc libtool-ltdl \
libtool-ltdl-devel xinetd tar make git wget file \
openssh-server postgresql-odbc libuuid-devel speex-devel \
jansson-devel lua lua-devel unzip readline-devel \
postgresql-devel mysql-devel curl-devel lualibedit-devel \
libedit-devel epel-release
RUN yum -y upgrade \
    && yum -y install luarocks
RUN mkdir -p /usr/src/asterisk \
    && cd /usr/src \    
    && wget https://downloads.asterisk.org/pub/telephony/asterisk/asterisk-16-current.tar.gz \
    && tar -xzvf /usr/src/asterisk-16-current.tar.gz --strip-components=1 -C /usr/src/asterisk \
    && mv /etc/localtime /etc/localtime.bak \
    && ln -s /usr/share/zoneinfo/Europe/Moscow /etc/localtime \
    && cd /usr/src/asterisk \
    && ./configure --libdir=/usr/lib64 --with-jansson-bundled --with-pjproject-bundled \
    && make menuselect.makeopts \
    && menuselect/menuselect \
  --disable BUILD_NATIVE \
  --enable res_config_mysql \
  --enable app_mysql \
  --enable CORE-SOUNDS-RU-WAV \
  --enable CORE-SOUNDS-RU-ULAW \
  --enable G711_NEW_ALGORITHM \
  --enable G711_REDUCED_BRANCHING \
  --disable cdr_pgsql \
  --disable cdr_csv \
  --disable cdr_sqlite3_custom \
  --enable chan_sip \
  --enable res_snmp \
  --enable func_speex \
  menuselect.makeopts \
  && make && make install && make samples
#Install Lame to Centos, converting WAV to MP3 app
RUN cd /usr/src \
    && wget https://sourceforge.net/projects/lame/files/lame/3.100/lame-3.100.tar.gz \
    && tar -xzf lame-3.100.tar.gz \
    && cd lame-3.100 \
    && ./configure \
    && make \
    && make install
RUN cd /usr/src \
    && git clone https://github.com/keplerproject/luasql.git \
    && cd /usr/src/luasql \
    && /usr/bin/sed -i 's/5.2/5.1/g' config \
    && /usr/bin/sed -i 's/\/lib\/lua/\/lib64\/lua/g' config \
    && /usr/bin/sed -i 's/\/usr\/lib/\/usr\/lib64/g' config \
    && /usr/bin/sed -i 's/lib64\ \-lmysqlclient/lib64\/mysql\ \-lmysqlclient/g' config \
    && make mysql \
    && make install
RUN /usr/bin/luarocks-5.1 install lua-resty-socket \
    && /usr/bin/luarocks install sha1 \
    && /usr/bin/luarocks install lua-MessagePack \
    && /usr/bin/luarocks install luasocket \
    && /usr/bin/luarocks install luasql-postgres \
    && /usr/bin/luarocks install luacrypto \
    && /usr/bin/luarocks install lunit \
    && /usr/bin/luarocks install lua-cjson \
    && /usr/bin/luarocks install luaposix \
    && /usr/bin/luarocks install luasec \
    && /usr/bin/luarocks install lua-requests \
    && /usr/bin/luarocks install lbase64 \
    && /usr/bin/luarocks install md5 \
    && /usr/bin/luarocks install xml \
    && /usr/bin/luarocks install luasec \
    && /usr/bin/luarocks install inspect \
    && /usr/bin/luarocks install luajson \
    && /usr/bin/luarocks install lua-curl \
    && cd /usr/src \
    && git clone https://github.com/tarantool/tarantool-lua.git \
    && git clone https://github.com/cloudflare/raven-lua \
    && cp -r /usr/src/raven-lua/raven /usr/share/lua/5.1/ \
    && cd /usr/src/tarantool-lua \
    && /usr/bin/luarocks install lua-tarantool-scm-1.rockspec
RUN wget http://asterisk.hosting.lv/bin/codec_g729-ast160-gcc4-glibc-x86_64-pentium4.so -O /usr/lib64/asterisk/modules/g729.so

#MAX FILES UP
RUN sed -i 's/'\#\ MAXFILES\=\32768'/'MAXFILES\=\99989'/g' /usr/sbin/safe_asterisk && sed -i 's/TTY=9/TTY=/g' /usr/sbin/safe_asterisk
CMD /usr/sbin/asterisk -f -vvvg -c
