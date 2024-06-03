PGP Decryption
==============

This folder contains steps to decrypt PGP files on AWS S3 using Sparkflows.

Details
--------

The PGP files are on S3. Below are the steps to decrypt the files using the shell node in Sparkflows

* Create a workflow.
<img width="1327" alt="WorflowWithShellNode" src="https://github.com/sparkflows/fire-tools/assets/51231386/dda8b522-8db4-4be3-a669-49d9cbcac923">

* Add a shell node to the workflow. Add commands to the shell node to copy the PGP files onto the local machine, decrypt it and then copy it back to the destination folder on S3.
```
aws s3 cp ${S3_LOCATION}/encrypted_files/a.csv.gpg ${LOCAL_PATH}/encrypted_files;
aws s3 cp ${S3_LOCATION}/check.sh ${LOCAL_PATH}/;
sh ${LOCAL_PATH}/check.sh ${S3_LOCATION} ${LOCAL_PATH}
```

<img width="1413" alt="ShellCommands" src="https://github.com/sparkflows/fire-tools/assets/51231386/b6da39c9-b765-4509-8892-5071d4f6c1f1">

* Execute the workflow

The input and output folders to the workflow can be parameterized.

<img width="1387" alt="WorkflowWithParmeters" src="https://github.com/sparkflows/fire-tools/assets/51231386/a188e86d-9f35-416a-917f-f6a1aa50d9bf">

Shell script
------------

Below is the shell script that goes into the shell node in the workflows.

```
usage() {
  echo "Usage: $0 param1 param2"
  echo "  param1: s3 path"
  echo "  param2: local path"
  exit 1
}

# Check if the number of parameters is exactly 2
if [ "$#" -ne 2 ]; then
  echo "Error: Invalid number of parameters"
  usage
fi

# Assign parameters to variables

s3_path=$1
local_path=$2


for entry in  $local_path/encrypted_files/*
do
        echo $entry
        input=$(echo "$(basename "$entry")" | cut -f 1 -d '.')".csv.gpg"
        echo $input

        output=$(echo "$(basename "$entry")" | cut -f 1 -d '.')".csv"

        gpg --no-tty --batch --import $local_path/public.key

        gpg --no-tty --batch --yes --ignore-mdc-error --pinentry-mode=loopback --passphrase-fd 1 --passphrase-file $local_path/Passphrase.txt --output $local_path/decrypted_files/$output --decrypt $local_path/encrypted_files/$input
done
```
