<!--
 Copyright 2021 dciangot
 
 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at
 
     http://www.apache.org/licenses/LICENSE-2.0
 
 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
-->

# Dev deployment

You only need to launch a k8s cluster with either [Minikube](https://minikube.sigs.k8s.io/docs/start/) (using vbox or qemu), or one of [KinD](https://kind.sigs.k8s.io/docs/user/quick-start/) or [K3d](https://k3d.io/) for an instance inside Docker.

Then deploy you image with the manifests in `docker/spark/kubernetes`.