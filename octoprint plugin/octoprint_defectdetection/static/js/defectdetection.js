/*
 * View model for OctoPrint-Defectdetection
 *
 * Author: Rishabh Changra
 * License: AGPLv3
 */
$(function() {
    function DefectdetectionViewModel(parameters) {
        var self = this;

        self.loginStateViewModel = parameters[0];
        self.settingsViewModel = parameters[1];		
		// self.prediction=undefined;
		// self.confidence=undefined;
		self.cam_url=ko.observable();
		self.cam_width=ko.observable();
		self.cam_height=ko.observable();
		self.model=ko.observable();
		self.interval=ko.observable();
		
		

		self.onStartup= function(){
	
			self.prediction=$('<span class="prediction-value"></span>');
			// self.confidence=$('<span class="confidence-value"></span>');
			// self.predictbutton=$('<button class="btn btn-primary" onclick="predictionbutton()"> Predict</button></span>');
			
			
			
			
			var container=$('<div class="Prediction-container"></div>');
			container.append(" ");
			container.append("</br>")
			container.append(self.prediction);
			// container.append("  ");
			// container.append(self.confidence);
			
			container.insertAfter($('.mjpg_container'));
			
			// var container_predict=$('<div></div>');
			// container_predict.append(self.predictbutton);
			// container_predict.insertAfter($('.Prediction-container'));
	

	
		}
		
		self.onBeforeBinding = function() {
		self.cam_url(self.settingsViewModel.settings.webcam.streamUrl());
		self.cam_width(self.settingsViewModel.settings.plugins.defectdetection.cam_width());
		self.cam_height(self.settingsViewModel.settings.plugins.defectdetection.cam_height());
		self.model(self.settingsViewModel.settings.plugins.defectdetection.model());
		self.interval(self.settingsViewModel.settings.plugins.defectdetection.interval());
		}
		
		
		
		self.onEventSettingsUpdated = function(payload) {
		self.cam_width(self.settingsViewModel.settings.plugins.defectdetection.cam_width());
		self.cam_height(self.settingsViewModel.settings.plugins.defectdetection.cam_height());
		self.model(self.settingsViewModel.settings.plugins.defectdetection.model());
		self.interval(self.settingsViewModel.settings.plugins.defectdetection.interval());
		}
		
		self.onDataUpdaterPluginMessage = function (plugin, data) {
			if (plugin !== "defectdetection") {
				console.log("inside if statement");
				return;
			}
			

			$('.prediction-value').css("font-size", "20px");
			$('.prediction-value').css("font-weight", "bold");
			$('.prediction-value').css("font-family", "Calibri");


			if (data.parameter1=='Normal'){

				$('.prediction-value').css("color","green");
			}
			
			else if(data.parameter1=="Underextrusion"){
				$('.prediction-value').css("color", "red");
			}

			else{
				$('.prediction-value').css("color", "black");
			}

			

			$('.prediction-value').text(data.parameter1);

			
			console.log(' Prediction = '+data.parameter1);      //+' Confidence= '+ data.parameter2);
		
		
		}

		// predictionbutton=function(){

		// 	self.predictbutton.

		// }
	
		
		
		
    }


    OCTOPRINT_VIEWMODELS.push({
        construct: DefectdetectionViewModel,
        dependencies: [  "loginStateViewModel", "settingsViewModel"  ],
        elements: ["#settings_plugin_defectdetection", "#tab_plugin_defectdetection"]
    });
});
