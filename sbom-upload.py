import requests
import json

# Replace with your FOSSA API Token
FOSSA_TOKEN = ''

# Project and revision details
package_spec = 'sbom-project-name'
revision = 'sbom-revision'
file_type = 'sbom'

# Step 1: Get a signed URL from the FOSSA API
def get_signed_url(package_spec, revision, file_type):
    url = f'https://app.fossa.io/api/components/signed_url?packageSpec={package_spec}&revision={revision}&fileType={file_type}'
    headers = {
        'Authorization': f'Bearer {FOSSA_TOKEN}'
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()['signedUrl']
    else:
        print(f"Error getting signed URL: {response.status_code}, {response.text}")
        return None

# Step 2: Upload the SBOM file to the signed URL
def upload_sbom_to_signed_url(signed_url, sbom_file_path):
    with open(sbom_file_path, 'rb') as file:
        headers = {'Content-Type': 'application/octet-stream'}
        response = requests.put(signed_url, data=file, headers=headers)

        if response.status_code == 200:
            print("Successfully uploaded the SBOM")
        else:
            print(f"Error uploading SBOM: {response.status_code}, {response.text}")

# Step 3: Trigger a build via the FOSSA API
def trigger_fossa_build(package_spec, revision, file_type):
    url = 'https://app.fossa.io/api/components/build'
    headers = {
        'Authorization': f'Bearer {FOSSA_TOKEN}',
        'Content-Type': 'application/json'
    }
    data = {
        "archives": [{"packageSpec": package_spec, "revision": revision, "fileType": file_type}]
        # "selectedTeams": [{"id": team-id, "name": "existing-team-name", "organizationId": org-id}]
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 201:
        print("Successfully triggered the build")
    else:
        print(f"Error triggering the build: {response.status_code}, {response.text}")

# Main execution
def main():
    signed_url = get_signed_url(package_spec, revision, file_type)
    if signed_url:
        # Replace with your local SBOM file path
        sbom_file_path = 'this-is-an-sbom.json'
        upload_sbom_to_signed_url(signed_url, sbom_file_path)
        trigger_fossa_build(package_spec, revision, file_type)

if __name__ == '__main__':
    main()
