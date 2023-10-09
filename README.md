# Parkinson's Disease Prediction Model Deployment on Azure Cloud

## Overview

This project aims to deploy a deep learning model for predicting Parkinson's disease using MRI images on Azure Cloud Services. Physicians worldwide use MRI images for disease diagnosis, and leveraging deep learning models can enhance the accuracy and speed of predictions. The deployed model allows users to determine whether a person has Parkinson's disease or not. Below are the steps to deploy this model on Azure Cloud using a Free Tier Account.

## Deployment Steps

### 1. Create an Azure Cloud Account and Resources

- Sign up for an Azure Cloud account if you don't have one.
- Use the "Azure_create_resources.txt" file in the repository to create the necessary Azure resources. These resources typically include a virtual machine, Azure Container Registry, and Azure App Service.

### 2. Train and Save the Model

- Train your deep learning model using MRI image data and save the trained model file. Ensure that you save the model file (e.g., `my_model.h5`) into the "Endpoint/Trained_Model/" directory.

### 3. Docker Image Creation

- Use the provided Dockerfile in both the "Endpoint" and "WEBAPP" directories to create Docker images for the model and web app.
- Build the Docker images using the `docker build` command.
- Push the Docker images to the Azure Container Registry using the following command (replace `mriprojectcontainerregistry` with your Azure Container Registry name):

```bash
docker push mriprojectcontainerregistry.azurecr.io/webapp
```

### 4. Deploy Docker Image on Azure Cloud

- Deploy the Docker image from the Azure Container Registry onto a Linux Virtual Machine on Azure Cloud using Azure App Service.
- Configure the necessary settings and environment variables for the deployed web app.

### 5. Access the Web App

- After successful deployment, you will receive a public URL to access the web app hosted on Azure App Service.
- Users can now visit this URL to use the model for predicting Parkinson's disease based on MRI images.

## Azure Architecture
![image](https://github.com/abhi-sama/PD-Prediction-Model-Deployment-on-Azure-Cloud/assets/129358937/352303f2-8359-47ea-a63f-6b7ff51ac3fc)

## Web App
![MRI_browse](https://github.com/abhi-sama/PD-Prediction-Model-Deployment-on-Azure-Cloud/assets/129358937/6bcfa799-2f29-45ed-8462-8616ec4cc272)

## Conclusion

This project demonstrates how to deploy a deep learning model for Parkinson's disease prediction using MRI images on Azure Cloud Services. By following the outlined steps, you can create Azure resources, train and save your model, containerize it using Docker, and deploy it on Azure App Service. This allows for efficient and accessible disease prediction, benefiting both medical professionals and patients.

Please note that this is a simplified readme, and the actual deployment process may require more detailed instructions depending on the specific Azure services and configurations used. Additionally, consider security and compliance requirements when handling medical data and deploying healthcare-related applications.
