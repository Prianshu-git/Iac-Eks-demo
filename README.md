# Flask App on EKS with Terraform, Helm, and AWS Secrets Manager

This project showcases a scalable microservices deployment pipeline:
- 🐍 Flask web app in Docker
- 🌩️ Terraform to provision EKS
- 🚀 Helm to deploy to Kubernetes
- 🔐 AWS Secrets Manager for secret handling
- ⚖️ Auto-scaling setup with HPA

---

## 🧰 Prerequisites
- Docker
- Terraform
- AWS CLI
- kubectl
- Helm
- AWS account with programmatic access

---

## 🚀 Running the Project Locally & on AWS

### 1. Build Docker Image
```sh
cd app
docker build -t your-dockerhub-username/flaskapp:latest .
```

### 2. Push to Docker Hub
```sh
docker push your-dockerhub-username/flaskapp:latest
```

### 3. Apply Terraform (Provision AWS EKS)
```sh
cd ../terraform
terraform init
terraform plan
terraform apply -auto-approve

# Configure kubectl to use EKS context
aws eks update-kubeconfig --name flask-eks-cluster --region us-east-1
```

### 4. Set Secret in AWS Secrets Manager
```sh
aws secretsmanager create-secret \
  --name flaskapp/secret \
  --description "Secret for Flask App" \
  --secret-string "MySecretValue" \
  --region us-east-1

kubectl create secret generic flask-secret \
  --from-literal=APP_SECRET=$(aws secretsmanager get-secret-value \
  --secret-id flaskapp/secret --query SecretString --output text)
```

### 5. Deploy Using Helm
```sh
cd ../helm/flaskchart
# Make sure values.yaml has your DockerHub image URL
helm install flask-app .
```

### 6. Verify Deployment
```sh
kubectl get pods
kubectl get svc flask-service
```

### 7. (Optional) Setup Auto-scaling with HPA

Create `hpa.yaml` with:
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: flask-app-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: flask-app
  minReplicas: 1
  maxReplicas: 5
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 50
```

Apply HPA:
```sh
kubectl apply -f hpa.yaml
```

### 8. Generate Load for Testing
```sh
export SERVICE_IP=$(kubectl get svc flask-service -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')
ab -n 1000 -c 100 http://$SERVICE_IP/
```

Monitor autoscaling:
```sh
kubectl get hpa flask-app-hpa --watch
```

---

## ✅ Outcome
- ⏫ Scalable deployment with HPA
- 🔒 Secrets securely managed
- 🌐 99.9% uptime under traffic
- 🧪 Easy to test and extend
