def update_status_based_on_function_app_status():
    try:
        # Use Managed Identity for authentication
        credential = DefaultAzureCredential(
            managed_identity_client_id=settings.UAMI_CLIENT_ID
        )

        # Check the status of the function app using Azure SDK or CLI
        function_app_name = "your-function-app-name"
        resource_group_name = "your-resource-group-name"

        # Example: Use Azure CLI to check the function app status
        import subprocess
        cmd = f"az functionapp show --name {function_app_name} --resource-group {resource_group_name} --query state -o tsv"
        function_app_status = subprocess.check_output(cmd, shell=True).decode("utf-8").strip()

        print(f"Function App status: {function_app_status}")

        # Determine the status to update in the blob based on function app status
        if function_app_status == "Running":
            new_status = "idle"
        else:
            new_status = "processing"

        # Update the blob with the new status
        account_url = f"https://{STORAGE_ACCOUNT_NAME}.blob.core.windows.net"
        blob_service_client = BlobServiceClient(account_url=account_url, credential=credential)

        container_client = blob_service_client.get_container_client(CONTAINER_NAME)
        blob_client = container_client.get_blob_client("processing_status.txt")

        blob_client.upload_blob(new_status, overwrite=True)
        print(f"Updated the status in blob to: {new_status}")

    except subprocess.CalledProcessError as e:
        print(f"Failed to retrieve function app status: {e}")
    except Exception as e:
        print(f"Failed to update the status in blob: {e}")
