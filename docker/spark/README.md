# Spark on Kubernetes Docker Image
Apache Spark is a fast and general-purpose cluster computing system.
In order to get a working image of Apache Spark 2.4.4 for K8s:
```   
    git clone https://github.com/apache/spark.git
    git checkout tags/v2.4.4
    build/mvn -Pkubernetes -DskipTests clean package
````
Then, modify the Dockerfile to get the updated k8s client:
````
    cd resource-managers/kubernetes/docker/src/main/dockerfiles/spark
    rm Dockerfile
    vim Dockerfile
````
and insert the content of [this Dockerfile](Dockerfile).

In order to build and push the images you can use:
```
    ./bin/docker-image-tool.sh -r <repo> -t my-tag build
    ./bin/docker-image-tool.sh -r <repo> -t my-tag push
```

This can be then used to deploy Spark on a K8s cluster using a Helm chart: https://github.com/DODAS-TS/helm_charts.git