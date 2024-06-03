PGP Decryption
==============

This folder contains steps to decrypt PGP files on AWS S3 using Sparkflows.

Details
--------

The PGP files are on S3. Below are the steps to decrypt the files using the shell node in Sparkflows

* Create a workflow.
* Add a shell node to the workflow. Add commands to the shell node to copy the PGP files onto the local machine, decrypt it and then copy it back to the destination folder on S3.
* Execute the workflow

The input and output folders to the workflow can be parameterized.

Shell script
------------

Below is the shell script that goes into the shell node in the worflows.

