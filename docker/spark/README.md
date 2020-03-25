# Spark on Kubernetes Docker Image
Apache Spark is a fast and general-purpose cluster computing system.
In order to get a working image of Apache Spark 2.4.4 for K8s:

```bash
    sudo apt install openjdk-8-jdk
    git clone https://github.com/apache/spark.git -o spark_src
    cd spark_src
    git checkout tags/v2.4.4
    build/mvn -Pkubernetes -DskipTests clean package
    cd -
```

In order to build and push the images you can use:
```
    docker build .  -t myimage:mytag
    docker push myrepo/myimage:mytag
```

This can be then used to deploy Spark on a K8s cluster using a Helm chart: https://github.com/DODAS-TS/helm_charts.git