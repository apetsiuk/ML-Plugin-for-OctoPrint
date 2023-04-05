# coding=utf-8
from __future__ import absolute_import



import flask
import numpy as np 
import cv2
import os
import urllib
from keras.models import load_model
from PIL import Image
import math
import tensorflow as tf


import octoprint.plugin

class DefectdetectionPlugin(octoprint.plugin.SettingsPlugin,
                            octoprint.plugin.AssetPlugin,
                            octoprint.plugin.TemplatePlugin):


    INTERVAL = 5.0
    CAM_WIDTH=640
    CAM_HEIGHT=480
    MODEL='Model-3'
    PREDICTION_ON=False



    def __init__(self):
        self._timer= None
        self._interval=None
        # self._interpreter1 = tf.lite.Interpreter(model_path='./OctoPrint-Defectdetection/octoprint_defectdetection/3Dresnet101.tflite')
        # self._interpreter1.allocate_tensors()
        # self._input_details = self._interpreter1.get_input_details()
        # self._output_details = self._interpreter1.get_output_details()
        # self._input_shape=self._input_details[0]['shape']
  
        self._model3=load_model("./OctoPrint-Defectdetection/octoprint_defectdetection/3dnet_resnet.h5")

    
    def initialize(self):
        self._interval=self._settings.get_float(["interval"])
        self._logger.info(self._interval)
        self._cam_width=self._settings.get(["cam_width"])
        self._logger.info(self._cam_width)
        self._cam_height=self._settings.get(["cam_height"])
        self._logger.info(self._cam_height)
        self._cam_url=self._settings.global_get(["webcam", "snapshot"])
        self._logger.info(self._cam_url)
        self._model=self._settings.get(["model"])
        self._logger.info(self._model)
        self._prediction_on=self._settings.get(["prediction_on"])
        self._timer=octoprint.util.RepeatedTimer(self.interval, self._myfunction)

        self.categories=["Normal", "Underextrusion"]
        self._timer.start()
        
    def interval(self):
        return self._interval        
        
     ##~~ SettingsPlugin mixin   
    def get_settings_defaults(self):
    
        return dict(cam_width=self.CAM_WIDTH,cam_height=self.CAM_HEIGHT, model=self.MODEL, interval=self.INTERVAL, prediction_on=self.PREDICTION_ON)

    
    def on_settings_save(self,data):
        old_interval=self._settings.get_float(["interval"])
        old_model=self._settings.get(["model"])
        old_cam_height=self._settings.get(["cam_height"])
        old_cam_width=self._settings.get(["cam_width"])
        
        
        octoprint.plugin.SettingsPlugin.on_settings_save(self,data)
        new_model=self._settings.get(["model"])
        new_cam_height=self._settings.get(["cam_height"])
        new_cam_width=self._settings.get(["cam_width"])
        new_interval=self._settings.get_float(["interval"])
        
        if old_interval!=new_interval:
            self._interval=new_interval
        if old_model!=new_model:
            self._model=new_model
        if old_cam_height!=new_cam_height:
            self._cam_height=new_cam_height
        if old_cam_width!=new_cam_width:
            self._cam_width=new_cam_width    
    
    def get_settings_version(self):
        return 1   
    
    ##~~ AssetPlugin mixin

    def get_assets(self):
        # Define your plugin's asset files to automatically include in the
        # core UI here.
        return {
            "js": ["js/defectdetection.js"],
            "css": ["css/defectdetection.css"],
            "less": ["less/defectdetection.less"]
        }
    
    
    # def _predictionbutton(self):
    #     # if self._prediction_on:
    #     #     self._timer.start()
    #     # else:
            
    #     #     self._timer.stop()
    
    def _myfunction(self):
        self._logger.info("myfunction called")
        
        
        testdata=[]
        # self._logger.info(self._settings.global_get(["webcam", "snapshot"]))
        resp = urllib.request.urlopen(self._cam_url)
        image = np.asarray(bytearray(resp.read()), dtype="uint8")
        
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)



        h,w=image.shape[:2]
        if w>h:
          image=image[0:h,0:w]
        else:
          image=image[0:w,0:w]
        image = Image.fromarray(image, 'RGB')
        image = image.resize((256, 256))
        # testdata.append(np.array(image, dtype=np.float32))
        testdata.append(np.array(image))
        testdata=np.array(testdata) 
        testdata=testdata/255
        

        # self._interpreter1.set_tensor(self._input_details[0]['index'], testdata)

        # self._interpreter1.invoke()
        # ypred = self._interpreter1.get_tensor(self._output_details[0]['index'])





        self._logger.info(self._model)
        if self._model=='Model-1':
            ypred=self._model1.predict(testdata)
        elif self._model=='Model-2':
            ypred=self._model2.predict(testdata)
        else:
            ypred=self._model3.predict(testdata)
            

        if np.squeeze(ypred)==1.0:
            prediction='None'
            #confidence=None

        else:
            y_pred=np.squeeze((ypred>=0.2).astype(int))
            prediction=self.categories[y_pred]
            # if np.squeeze(ypred)>=0.5:
            #     confidence=math.floor(np.squeeze(ypred)*100)
            # else:
            #     confidence=math.floor((1-np.squeeze(ypred))*100)
          
        self._logger.info('Prediction =' + prediction) #+'Confidence= '+ str(confidence))

        self._plugin_manager.send_plugin_message(self._identifier,{"parameter1": prediction})#, "parameter2": confidence})   
    ##~~ Softwareupdate hook

    def get_update_information(self):
        # Define the configuration for your plugin to use with the Software Update
        # Plugin here. See https://docs.octoprint.org/en/master/bundledplugins/softwareupdate.html
        # for details.
        return {
            "defectdetection": {
                "displayName": "Defectdetection Plugin",
                "displayVersion": self._plugin_version,

                # version check: github repository
                "type": "github_release",
                "user": "rishabhchangra",
                "repo": "OctoPrint-Defectdetection",
                "current": self._plugin_version,

                # update method: pip
                "pip": "https://github.com/rishabhchangra/OctoPrint-Defectdetection/archive/{target_version}.zip",
            }
        }


# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py
# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.
__plugin_name__ = "Defectdetection Plugin"


# Set the Python version your plugin is compatible with below. Recommended is Python 3 only for all new plugins.
# OctoPrint 1.4.0 - 1.7.x run under both Python 3 and the end-of-life Python 2.
# OctoPrint 1.8.0 onwards only supports Python 3.
__plugin_pythoncompat__ = ">=3,<4"  # Only Python 3

def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = DefectdetectionPlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
    }
