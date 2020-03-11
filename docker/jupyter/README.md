# Jupyter Docker Stacks

These are a set of ready-to-run [Docker images](https://hub.docker.com/u/jupyter)
containing Jupyter applications based on Python 3.6.

## Quick Start
In order to create the images:
```   
    git clone https://github.com/DODAS-TS/docker-img_jupyter.git
    cd docker-img_jupyter
    make build-all
````
based on https://github.com/jupyter/docker-stacks

### Default configuration values ([spark-defaults](pyspark-notebook/spark-defaults.conf))

| Parameter               | Description                        | Default                                                    |
| ----------------------- | ---------------------------------- | ---------------------------------------------------------- |
| `spark.app.id`           |  Root namespace used for driver or executor metrics  | `KubernetesSpark`  |
| `spark.master`  |  The cluster manager to connect to.      | `k8s://https://kubernetes:443`     |
| `spark.driver.port`|Port for the driver to listen on. This is used for communicating with the executors and the standalone Master.| `7077`|
| `spark.executor.memory`| Amount of memory to use per executor process, in the same format as JVM memory strings with a size unit suffix ("k", "m", "g" or "t") (e.g. 512m, 2g). | `1g`  |
| `spark.executor.instances` | Number of executors to run  | `1` |
| `spark.kubernetes.container.image`            | Container image to use for the Spark application. This is usually of the form example.com/repo/spark:v1.0.0. This configuration is required and must be provided by the user, unless explicit images are provided for each different container type.          | `ttedesch/spark-py:base_k8s_2.4.4`                                                     |
|`spark.kubernetes.authenticate.driver.serviceAccountName`| Service account that is used when running the driver pod. The driver pod uses this service account when requesting executor pods from the API server. Note that this cannot be specified alongside a CA cert file, client key file, client cert file, and/or OAuth token. In client mode, use ```spark.kubernetes.authenticate.serviceAccountName``` instead. | `default`|
| `spark.submit.deployMode ` |  The deploy mode of Spark driver program, either "client" or "cluster", Which means to launch driver program locally ("client") or remotely ("cluster") on one of the nodes inside the cluster. | `client`|