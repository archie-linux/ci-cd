### CI/CD Workflow

### Running the system

- docker-compose up --build

### Testing the system

- ./task_dispatcher.sh

### Check Logs

- docker exec -it [worker-node-1|worker-node-2] bash
- cat job_results.log

https://github.com/user-attachments/assets/e8e6d010-5372-4026-93ff-17f271ad7a84


### Minikube Deployment

1. Start Minikube

- minikube start --driver=docker
- minikube addons enable storage-provisioner

2. Restart minikube for a fresh install in case of errors

- minikube stop
- minikube delete
- minikube start --driver=docker \
    --extra-config=controller-manager.horizontal-pod-autoscaler-sync-period=5s \
    --extra-config=controller-manager.horizontal-pod-autoscaler-downscale-stabilization=30s
- minikube addons enable storage-provisioner

3. Verify Your Kubernetes version

- minikube version
- kubectl version

4. Use Minikube's Docker Daemon

- eval $(minikube docker-env)

5. Minikube Dashboard

- minikube dashboard

6. Build Docker Images

- docker build -t fastapi-job-manager:latest .
- docker build -t worker-node:latest .

7. Verify docker images loaded in minikube

- minikube ssh -- docker images

8. Note: These are one-time steps that have already been executed to convert
         existing docker-compose file to Kubernetes YAML.

- brew install kompose
- kompose convert

- Edit worker-node deployment files
    - Replace worker-node-1.yaml / worker-node-1.yaml to worker-node.yaml
    - Set Replicas to 3
    - Set imagePullPolicy: Never in both worker-node and fastapi-job-manager to prevent pulling image from registry
                           and fetch images built locally instead.

- Move docker-compose.yaml to docker-compose.yaml.bak so that kubernetes does not see it as a deployment file.

9. Deploy Services to Minikube

- kubectl apply -f .

10. Expose the FastAPI service to your local machine by port forwarding

- kubectl port-forward service/fastapi-job-manager 8000:8000

11. Submit Jobs

- ./task_dispatcher.sh

12. Check Job Manager Logs

- kubectl get pods
- kubectl logs [fastapi-job-manager]

13. Open an Interactive Shell in the Worker Pod

- kubectl get pods
- kubectl exec -it [worker-node] -- /bin/bash

14. Check Worker Logs

- cat job_results.log

15. Cleanup Resources

- kubectl delete pods --all
- kubectl delete svc --all
- kubectl delete deployment --all
- kubectl delete hpa worker-node-hpa

https://github.com/user-attachments/assets/b4c9c532-dac5-44e8-aced-bad0a247a9ce

### Horizontal Pod Autoscaler (HPA) Deployment

1. Deploy Services to Minikube

- kubectl apply -f .
- kubectl get pods
- kubectl get hpa

2. Run Stress Test

- ./task_dispatcher_load.sh

3. Monitor HPA with 5-second updates

- watch -n 1 "kubectl get hpa"
- kubectl describe hpa worker-node-hpa

4. Host-Level Monitoring

- minikube ssh
- top
- sudo killall yes # stops all yes processes

5. Observe Scale-Down Events

- watch -n 1 "kubectl describe hpa worker-node-hpa"

<pre>
MacBook-Air-2:ci-cd anish$ kubectl describe hpa worker-node-hpa
Name:                                                  worker-node-hpa
Namespace:                                             default
Labels:                                                <none>
Annotations:                                           <none>
CreationTimestamp:                                     Tue, 25 Feb 2025 14:02:32 +0530
Reference:                                             Deployment/worker-node
Metrics:                                               ( current / target )
  resource cpu on pods  (as a percentage of request):  2% (2m) / 50%
Min replicas:                                          3
Max replicas:                                          10
Deployment pods:                                       3 current / 3 desired
Conditions:
  Type            Status  Reason            Message
  ----            ------  ------            -------
  AbleToScale     True    ReadyForNewScale  recommended size matches current size
  ScalingActive   True    ValidMetricFound  the HPA was able to successfully calculate a replica count from cpu resource utilization (percentage of request)
  ScalingLimited  True    TooFewReplicas    the desired replica count is less than the minimum replica count
Events:
  Type     Reason                        Age                  From                       Message
  ----     ------                        ----                 ----                       -------
  Warning  FailedGetResourceMetric       10m (x10 over 10m)   horizontal-pod-autoscaler  failed to get cpu utilization: unable to get metrics for resource cpu: no metrics returned from resource metrics API
  Warning  FailedComputeMetricsReplicas  10m (x10 over 10m)   horizontal-pod-autoscaler  invalid metrics (1 invalid out of 1), first error is: failed to get cpu resource metric value: failed to get cpu utilization: unable to get metrics for resource cpu: no metrics returned from resource metrics API
  Warning  FailedComputeMetricsReplicas  9m59s (x2 over 10m)  horizontal-pod-autoscaler  invalid metrics (1 invalid out of 1), first error is: failed to get cpu resource metric value: failed to get cpu utilization: did not receive metrics for targeted pods (pods might be unready)
  Warning  FailedGetResourceMetric       9m54s (x3 over 10m)  horizontal-pod-autoscaler  failed to get cpu utilization: did not receive metrics for targeted pods (pods might be unready)
  Normal   SuccessfulRescale             9m4s                 horizontal-pod-autoscaler  New size: 6; reason: cpu resource utilization (percentage of request) above target
  Normal   SuccessfulRescale             8m59s                horizontal-pod-autoscaler  New size: 10; reason: cpu resource utilization (percentage of request) above target
  Normal   SuccessfulRescale             6m38s                horizontal-pod-autoscaler  New size: 3; reason: All metrics below target
</pre>

https://github.com/user-attachments/assets/d998b547-025d-4dcf-a985-ea00aa595ae0
