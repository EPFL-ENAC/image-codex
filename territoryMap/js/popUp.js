//Popup On Mouse Over
function popUpOnMouseHover(feature, layer){ //isolate this function out
    layer.on('mouseover', function (e) {
        this.openPopup();
    });
    layer.on('mouseout', function (e) {
        this.closePopup();
    });
}


function popUp(feature, layer){
    var author = String(feature.properties.author);
    var title = String(feature.properties.title);
    var popUpContent = "Image: " + title + "<br>" 
                    + "Author: " + author + "<br>"   
                    + "<img src='data/sample_images/MF_01.jpeg' width='120'>";
    layer.bindPopup(popUpContent);
    popUpOnMouseHover(feature, layer);

}