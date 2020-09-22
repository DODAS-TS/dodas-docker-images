#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, subprocess, shutil, sys, uuid, time, base64

from pyspark import SparkConf, SparkContext
from string import Formatter
import socket

try:
    from kubernetes import config, client
    from kubernetes.client.rest import ApiException
except ImportError:
    pass

class SparkConfigurationFactory:

    def __init__(self, connector):
        self.connector = connector

    def create(self):
        cluster_name = os.environ.get('SPARK_CLUSTER_NAME', 'local')

        # Define configuration based on cluster type
        if cluster_name == 'local':
            # local
            return SparkLocalConfiguration(self.connector, cluster_name)

class SparkConfiguration(object):

    def __init__(self, connector, cluster_name):
        self.cluster_name = cluster_name
        self.connector = connector

    def get_cluster_name(self):
        """ Get cluster name """
        return self.cluster_name

    def get_spark_memory(self):
        """ Get spark max memory """
        return os.environ.get('MAX_MEMORY', '2')

    def get_spark_version(self):
        """ Get spark version """
        from pyspark import __version__ as spark_version
        return spark_version

    def get_spark_user(self):
        """ Get cluster name """
        return os.environ.get('SPARK_USER', '')

    def get_spark_needs_auth(self):
        """ Do not require auth if SPARK_AUTH_REQUIRED is 0,
        e.g. in case HADOOP_TOKEN_FILE_LOCATION has been provided
        """
        return os.environ.get('SPARK_AUTH_REQUIRED', 'false') == 'true'

    def close_spark_session(self):
        sc = self.connector.ipython.user_ns.get('sc')
        if sc and isinstance(sc, SparkContext):
            sc.stop()

    def _parse_options(self, _opts):
        """ Parse options and set defaults """
        _options = {}
        if 'options' in _opts:
            for name, value in _opts['options'].items():
                replaceable_values = {}
                for _, variable, _, _ in Formatter().parse(value):
                    if variable is not None:
                        replaceable_values[variable] = os.environ.get(variable)

                value = value.format(**replaceable_values)
                _options[name] = value
        return _options

    def configure(self, opts, ports):
        """ Initializes Spark configuration object """

        # Check if there's already a conf variablex
        # If using SparkMonitor, this is defined but is of type SparkConf
        conf = SparkConf().setMaster("k8s://https://kubernetes:443")\
         .setAppName("Notebook")\
         .set("spark.executor.memory", "1g")\
         .set("spark.executor.instances", "1")\
         .set("spark.kubernetes.container.image", "dodasts/spark:v3.0.0")\
         .set("spark.kubernetes.authenticate.driver.serviceAccountName","default")\
         .set("spark.submit.deployMode", "client")\
         .set('spark.extraListeners', 'sparkmonitor.listener.JupyterSparkMonitorListener')\
         .set('spark.driver.extraClassPath', '/opt/conda/lib/python3.7/site-packages/sparkmonitor/listener.jar')\
         .set('spark.driver.host', socket.gethostbyname(socket.getfqdn()))\
         #.set("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")\
         #.set("spark.hadoop.fs.s3a.path.style.access", "true")\
         #.set("spark.hadoop.fs.s3a.fast.upload", "true")
         #.set("spark.hadoop.fs.s3a.endpoint", "<minio host>:31311")
         #.set("spark.hadoop.fs.s3a.access.key", "admin")
         #.set("spark.hadoop.fs.s3a.secret.key", "adminminio")
         #.set("spark.hadoop.fs.s3a.fast.upload", "true")
         #.set("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") 

        return conf


class SparkLocalConfiguration(SparkConfiguration):

    def configure(self, opts, ports):
        """ Initialize YARN configuration for Spark """

        conf = super(self.__class__, self).configure(opts, ports)

        return conf


    def get_spark_session_config(self):
      conn_config = {}
      sc = self.connector.ipython.user_ns.get('sc')
      if sc and isinstance(sc, SparkContext):
         history_url = 'http://' + socket.gethostbyname(socket.getfqdn()) + ':' + '8080'
         conn_config['sparkhistoryserver'] = history_url
      return conn_config
