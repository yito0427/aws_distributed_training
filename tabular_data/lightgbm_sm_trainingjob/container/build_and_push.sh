#!/usr/bin/sh

# アルゴリズム名
algorithm_name=sagemaker-lightgbm

# ファイルを実行可能にする
chmod +x src/train
chmod +x src/serve

# アカウントID取得
account=$(aws sts get-caller-identity --query Account --output text)

# リージョン名
#region='ap-northeast-1'
region='us-west-2'

# リポジトリarn
fullname="${account}.dkr.ecr.${region}.amazonaws.com/${algorithm_name}:latest"

# ECRのリポジトリが存在しなければ作成する
aws --region ${region} ecr describe-repositories --repository-names "${algorithm_name}" > /dev/null 2>&1

if [ $? -ne 0 ]
then
    aws --region ${region} ecr create-repository --repository-name "${algorithm_name}" > /dev/null
fi

# ECRへのログインコマンドを取得し、ログインする
$(aws ecr get-login --region ${region} --no-include-email)


# コンテナイメージをビルドする
docker build  -t ${algorithm_name} .
docker tag ${algorithm_name} ${fullname}

# ECRのリポジトリへプッシュする
docker push ${fullname}