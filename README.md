# ML-Azure-Cloud-Model
All around the world, doctors use MRI images to predict diseases that a patient may be suffering from. For example, they may use this technology to determine if a person has a brain tumor or if they are suffering from Parkinson's disease. Making these predictions requires a great deal of knowledge and experience. To improve the accuracy of these predictions, we can use a deep learning model that is faster and more accurate.

The goal of this project is to deploy this model on the cloud using Azure Cloud (Free Tier Account). This repository provides the code to deploy a deep learning model to Azure Cloud Services.

To deploy the model, please follow these steps:

1)Create an Azure Cloud account and create the resources mentioned in the "Azure_create_resources.txt" file in the repo.

2)Train the model and save it. Copy and paste this saved model file into the "Endpoint/Trained_Model/" directory.

3)Using the Dockerfile present in the "Endpoint" and "WEBAPP" directories, create the Docker image. Push this Docker image to the Azure Container Registry using the command below, replacing "mriprojectcontainerregistry" with the name of the container register you created in Azure.

`docker push mriprojectcontainerregistry.azurecr.io/webapp`

4)In the last step, deploy this Docker image from the Azure Container Registry on a Linux Virtual Machine using Azure App Service.

5)You can find the public URL to access this web app in the Azure App Service.

Thank you for using this repository, and we hope it helps you deploy your deep learning model to the cloud successfully.
