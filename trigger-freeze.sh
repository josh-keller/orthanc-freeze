#!/bin/bash

echo 'Performing C-FIND'
qid=$(curl --user orthanc:orthanc http://localhost:4042/modalities/PACS/query -X POST -v -d '{ "Level": "Patient", "Query": {}}' | jq -r '.ID')

echo "C-FIND returned with query id: $qid"
echo "Trying C-MOVE..."
curl --user orthanc:orthanc http://localhost:4042/queries/$qid/answers/0/retrieve -X POST
