#!/bin/bash

. ./env.sh

python main.py \
    --region $DATAFLOW_REGION \
    --runner DataflowRunner \
    --project $PROJECT_ID \
    --job_name demo-job \
    --temp_location gs://$STORAGE_BUCKET/tmp/ \
    --staging_location gs://$STORAGE_BUCKET/staging/ 