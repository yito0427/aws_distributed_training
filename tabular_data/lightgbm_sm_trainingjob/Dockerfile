FROM ubuntu:18.04

# 必要なパッケージをインストールします
# インストールによって生じる不要なファイルは削除します
#RUN apt -y update && apt install -y --no-install-recommends \
#    wget \
#    python3-distutils \
#    nginx \
#    ca-certificates \
#    libgomp1 \
#    && apt clean

RUN apt-get -y update && apt-get install -y --no-install-recommends \
         wget \
         python3-distutils \
         python3-pip \
         python3-setuptools \
         nginx \
         ca-certificates \
         libgomp1 \
    && rm -rf /var/lib/apt/lists/*

RUN ln -s /usr/bin/python3 /usr/bin/python
RUN ln -s /usr/bin/pip3 /usr/bin/pip

# pythonパッケージをインストールします
# キャッシュファイルは重たいので、削除しておきます
#RUN wget https://bootstrap.pypa.io/get-pip.py && python3 get-pip.py && \
#    pip install wheel numpy scipy scikit-learn pandas lightgbm flask gevent gunicorn && \
#    rm -rf /root/.cache

#RUN pip --no-cache-dir install wheel numpy scipy scikit-learn pandas lightgbm flask gevent gunicorn

#RUN pip --no-cache-dir install wheel numpy scipy scikit-learn pandas lightgbm flask gevent gunicorn && \
#    rm -rf /root/.cache
    
RUN pip --no-cache-dir install wheel numpy scipy scikit-learn pandas lightgbm flask gunicorn && \
    rm -rf /root/.cache


# 環境変数の設定

# pythonからの出力をバッファしないようにする（ログが早く届くようにするため）
ENV PYTHONUNBUFFERED=TRUE
# .pycファイルを作成しないようにする
ENV PYTHONDONTWRITEBYTECODE=TRUE
# スクリプトがあるディレクトリへパスを通しておく(コンテナ起動時に実行するtrainとserveファイルのパスを意識しないで済むようにするため)
ENV PATH="/opt/program:${PATH}"

# スクリプトをコピーする
COPY lightgbm_container /opt/program

# 作業ディレクトリを設定する
WORKDIR /opt/program