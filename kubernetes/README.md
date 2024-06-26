# Sparkflows Installations on Kubernetes

This document describes the details of Sparkflows image and other configuration for deploying Sparkflows pod on kubernetes Cluster.

## Docker image

Use the docker image sparkflows/fire:py_3.2.1_3.2.78-rc6

### Ports

Expose the port 8080 for http and 8443 for https.

### Ingress

Use the ingress url of the service pointing to the port 8080/8443 to access the service.

### Deployment Steps

NOTE: This is not recommended for production deployments.

1. Use the configuration defined in the `fire-pv.yaml` file to setup the persistent volume. We'll be using this volume to mount on the sparkflows pod.

2. Once you have the persistent volumes deployed, you can use the `deployment.yaml` and `service.yaml` configuration to deploy Sparkflows with the above volume mounted.

```bash
 $ kubectl apply -f deployment.yaml
 $ kubectl apply -f service.yaml
```

3. Verify if the pod is running. This might take 2-3 minutes depending on the network speed. The sparkflows image size is ~ 7GB.

```bash
$ kubectl get po -A | grep sparkflows-app

default    sparkflows-app-6499d496cb-qvk2q      1/1     Running     0     14m

```

4. The above service configuration will deploy using LoadBalancer. You can also use NodePort for quick testing using the below command.

```bash
kubectl create service nodeport sparkflows-svc --tcp=5050:8080
```

Here 8080 is the target port, while 5050 is the exposed port.

You can open the browser and navigate to the http://<dsn.loadbalancer.sparkflows>:<exposed-port>/ to view the login page
