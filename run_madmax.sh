#! /bin/bash

sed 's/localhost:5432/localhost:5431/' application.conf > application_madmax3.conf
sed -i 's/parallelism     : 4/parallelism     : 60/g' application_madmax3.conf

cd "$(dirname $0)/../deepdive";
ROOT_PATH=`pwd`

$ROOT_PATH/../cleanpaleo/prepare_data.sh
env /lfs/madmax3/0/czhang/software/sbt/bin/sbt "run -c $ROOT_PATH/../cleanpaleo/application_madmax3.conf"
