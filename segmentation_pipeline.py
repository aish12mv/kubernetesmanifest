# -*- coding: utf-8 -*-
"""
Created on Fri Apr 22 16:32:15 2022

@author: XAI_PLATFORM

@project: XAI

@input: 

@output: 

@des:
"""

import kfp
import json
import logging
from kfp import dsl, components

@dsl.pipeline(name='Segmentation Pipeline', description='Provides segmentation.')
def train_segmentation():   

    # Downloading data from BQ
    input = kfp.components.load_component_from_file('components/download_data/Big_query/download_data.yaml')
    input_task = input()
    input_task.execution_options.caching_strategy.max_cache_staleness = "P0D"

    # segmentation = kfp.components.load_component_from_file(segmentation_model_training)

    # # trainig the Segmentation Model
    # segmentation_sys = segmentation(input_task.output)

    # cloud_storage = kfp.components.load_component_from_file(model_storage)

    # # Store the saved model in Google Storage
    # store_model = cloud_storage(segmentation_sys.output)

    # # Use Kserve to deploy models 
    # kserve_op = components.load_component_from_file(kserve_component)

    # deploy_op = kserve_op(
    # action='apply',
    # model_name='segmentationkfp',
    # model_uri=store_model.output,
    # framework='tensorflow',
    # namespace = 'default',
    # )

# Get configuration from config file
# try:
#     config = json.load(open('config.json'))
#     download_data = config.get('download_data')
#     segmentation_model_training = config.get('segmentation_model_training')
#     model_storage = config.get('model_storage')
#     kserve_component = config.get('kserve_component')
# except Exception as e:
#     logging.error(e)

client = kfp.Client(host="https://479f022e1a83c110-dot-us-east1.pipelines.googleusercontent.com")
client.create_run_from_pipeline_func(train_segmentation, arguments={})
    

