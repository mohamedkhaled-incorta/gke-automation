# GKE Automated Housekeeping

This repository contains a collection of automated housekeeping tasks for optimizing and managing Google Kubernetes Engine (GKE) environments. The primary focus is on improving resource utilization and reducing operational costs by automating routine tasks.

## Key Features

- **Automated Cleanup of Empty Nodes:**
  A Cloud Function that identifies and deletes GKE nodes with no critical workloads, reducing unnecessary cloud costs.
- **Historical Tracking:**
  Stores metadata about deleted nodes in Google Datastore for auditability and analysis.
- **Extendable:**
  Modular design for adding additional housekeeping tasks in the future.

## Getting Started

Follow these instructions to set up and deploy the `gke-empty-nodes` function, the first automated housekeeping task in this repository.

### Prerequisites

1. A Google Cloud Platform (GCP) project with billing enabled.
2. Access to the Google Cloud CLI (`gcloud`), with authentication configured.
3. Python 3.9 or higher installed locally for function development.
4. Terraform installed for infrastructure setup.

### Repository Structure

```
project-name/
├── functions/
│   ├── gke-empty-nodes/
│   │   ├── main.py              # Cloud Function code
│   │   ├── requirements.txt     # Python dependencies
│   │   ├── README.md            # Function-specific details
├── terraform/
│   ├── modules/
│   │   ├── cloud_function/      # Cloud Function deployment module
│   │   ├── service_account/     # Service Account creation module
│   ├── main.tf                  # Root Terraform configuration
│   ├── providers.tf             # Provider and version details
│   ├── variables.tf             # Input variables
│   ├── outputs.tf               # Outputs from Terraform
│   ├── terraform.tfvars         # Environment-specific variable values
├── .gitignore
├── README.md                    # Repository overview
```

---

## Deploying the `gke-empty-nodes` Function

### Step 1: Prepare the Function Code

1. Navigate to the function directory:
   ```bash
   cd functions/gke-empty-nodes
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Zip the function code:
   ```bash
   zip -r function.zip .
   ```

### Step 2: Set Up Infrastructure with Terraform

1. Navigate to the Terraform directory:
   ```bash
   cd terraform
   ```
2. Initialize Terraform:
   ```bash
   terraform init
   ```
3. Plan the infrastructure:
   ```bash
   terraform plan -var="project_id=<your-project-id>" -var="bucket_name=<bucket-name>"
   ```
4. Apply the changes:
   ```bash
   terraform apply -var="project_id=<your-project-id>" -var="bucket_name=<bucket-name>"
   ```



