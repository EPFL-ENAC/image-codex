		//Layer Toggling

		function toggleOn(layer, elementIL) { 
			layer.addTo(mainMap);
			x = document.getElementById(elementIL);
			x.className = "ILImage";
		}

		function toggleOff(layer, elementIL) {
			mainMap.removeLayer(layer); //toggle off()
			x = document.getElementById(elementIL);
			x.className = "close";
		}

		//LayerLegendToggleFunction
		function layerLegendToggle(layer, elementIL, checkBox) {
			var checkbox = document.getElementById(checkBox);
			if (checkbox.checked == true){
				toggleOn(layer, elementIL);
			} else{
				toggleOff(layer, elementIL);
	}
}