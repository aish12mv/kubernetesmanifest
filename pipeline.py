# -*- coding: utf-8 -*-


"""
Created on Mon Feb 14 10:23:21 2022

@author: anilkumar.Lenka,, Preetam Verma, Mitali, Cuburt Balanon

@project: XAI

@input:

@output:

@des:
"""


import json
import logging
from argparse import Namespace
from email.policy import default

import kfp
import yaml
from kfp import Client, components, dsl
from oauth2client.client import GoogleCredentials

credentials = GoogleCredentials.get_application_default()
credentials.get_access_token()
token1 = credentials.access_token 

PIPELINE_NAME ="regression-pipeline"
NAMESPACE = "default"
MODEL_NAME="regression-model"



kserve_op = components.load_component_from_url('https://raw.githubusercontent.com/kubeflow/pipelines/master/components/kserve/component.yaml')

def read_json_file(file_path):
      """loading  json file"""
      with open(file_path, "r") as file_obj:
         data = json.load(file_obj)
      return data 

container_spec_json = read_json_file("components_files/model_serving.json")
model_serving_image_name = container_spec_json["image"]


@dsl.pipeline(name=PIPELINE_NAME, description='Regression Pipeline ')
def regression_pipeline(model_config=dict):


      container_spec = '{"image":"%s", "port":8080, "name": "regression-model"}'%(model_serving_image_name)

      model_training_comp_file_path   = "model_training/model_training.yaml"
      gcp_storage_comp_file_path = "gcp_storage/storage.yaml"
      
      model_training_comp = components.load_component_from_file(model_training_comp_file_path)
      model_training_comp_response = model_training_comp(config=model_config)

      model_saving_comp = components.load_component_from_file(gcp_storage_comp_file_path)
      model_saving_comp_response = model_saving_comp(model=model_training_comp_response.output, gcp_path="gs://xai-nitesh/models/xgboost")

      kserve_op(action='apply',model_name=MODEL_NAME, custom_model_spec=container_spec,namespace=NAMESPACE).after(model_saving_comp_response)



model_config = read_json_file("config.json")
arguments = {"model_config":model_config}
client = Client(host="https://479f022e1a83c110-dot-us-east1.pipelines.googleusercontent.com", )
client.create_run_from_pipeline_func(regression_pipeline, arguments=arguments, enable_caching=False)
