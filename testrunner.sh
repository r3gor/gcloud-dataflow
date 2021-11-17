#!/bin/bash

. ./env.sh

python main.py \
    --region $DATAFLOW_REGION \
    --runner DirectRunner \
    --project $PROJECT_ID \
    --job_name testjob \
    --temp_location gs://$STORAGE_BUCKET/tmp/ \
    --staging_location gs://$STORAGE_BUCKET/staging/ \
    --setup_file ./setup.py