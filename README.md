# Orthanc Hang During Pending C-MOVE

This gist is a minimal working example of how to trigger a bug/unexpected behavior in Orthanc when a remote modality sends repeated C-MOVE-RSP messages with a `Pending` Status and no associated incoming C-STORE messages.

See the [Orthanc forum discussion](https://discourse.orthanc-server.org/t/frozen-jobs-and-rest-api-not-responding-after-stuck-c-move/6280)

## Starting and triggering the behavior

1. Run `docker compose up`
2. Trigger the behavior by running `bash trigger-freeze.sh` (or run curl commands manually)
3. The final `curl` command will never return. You can cancel and after that Orthanc should show the "frozen" behaviors described below.

## Contents

### Python script mimicking misbehaving PACS

The script provided in `dicom-server/server.py` responds with one result to a C-FIND with an empty query. The C-MOVE handler is unimportant because the desired behavior is triggered with a patch to the `pynetdicom` library. This script may have unneeded code as it took a lot of trial and error to make work, but I left the example as is because it was working.

### Patch to pynetdicom

Pynetdicom expects certain `yield` arguments from the handler. In addition, it attempts to run the C-STORE. To circumvent this, I have patched it, adding a loop that repeatedly sends a pending C-MOVE-RSP message no matter what the handler yields.

### trigger-freeze script

A simple script to trigger the behavior:

1. Use the `/modalities/PACS/query` endpoint to trigger a C-FIND.
2. Use the `/queries/id/answers/0/retrieve` endpoint to trigger a C-MOVE

## Observed behavior

1. Jobs are not able to be cancelled, paused, or deleted (at least the `DicomMoveScu` jobs, unsure about others)
2. Other C-MOVE scu requests do not seem to trigger and DICOM messages
3. Triggering a C-FIND from the REST API triggers the C-FIND request and response, but the API call never returns.
4. Unable to cleanly shutdown Orthanc (seems to stall when shutting down the jobs engine)
