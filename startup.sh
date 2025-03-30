#!/bin/bash

set -e  # Exit on any error

# Function to wait for resource deletion
wait_for_deletion() {
    local resource_type=$1
    local resource_name=$2
    echo "Waiting for $resource_type $resource_name to be deleted..."
    while kubectl get $resource_type $resource_name &>/dev/null; do
        sleep 2
    done
    echo "$resource_type $resource_name deleted or never existed."
}

# Function to wait for pods to be ready
wait_for_pods() {
    local label=$1
    echo "Waiting for pods with label $label to be ready..."
    kubectl wait --for=condition=Ready pod -l $label --timeout=300s
}

# Check Docker context and switch to Minikube’s environment
echo "Checking Docker context..."
docker context ls
echo "Switching to Minikube’s Docker environment..."
eval $(minikube docker-env)

# Delete existing resources (idempotent with --ignore-not-found)
echo "Deleting existing Kubernetes resources..."
kubectl delete -f ale-service.yaml --ignore-not-found=true
kubectl delete -f ale-config.yaml --ignore-not-found=true
kubectl delete -f ale-deployment.yaml --ignore-not-found=true
kubectl delete -f mysql-statefulset.yaml --ignore-not-found=true

# Wait for deletions to complete (avoids race conditions)
wait_for_deletion "service" "ale-service"
wait_for_deletion "configmap" "ale-config"
wait_for_deletion "deployment" "ale-app"
wait_for_deletion "statefulset" "mysql"

# Rebuild the Docker image (force rebuild to ensure latest code)
echo "Rebuilding Docker image ale-app:latest..."
docker build --no-cache -t ale-app:latest .
docker images | grep ale-app

# Apply new resources
echo "Applying Kubernetes resources..."
kubectl apply -f mysql-statefulset.yaml
kubectl apply -f ale-deployment.yaml
kubectl apply -f ale-config.yaml
kubectl apply -f ale-service.yaml

# Wait for pods to be ready
wait_for_pods "app=ale-app"
wait_for_pods "app=mysql"  # Adjust label based on your mysql-statefulset.yaml

# Verify pods
echo "Current pod status:"
kubectl get pods

# Get service URL
echo "Deployment complete!"
echo "Getting service URL..."
minikube service ale-service --url

