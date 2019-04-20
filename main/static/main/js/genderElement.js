function removeElement(elementId) {
    // Removes an element from the document
    var myNode = document.getElementById(elementId);
    while (myNode.firstChild) {
        myNode.removeChild(myNode.firstChild);
    }

}

function getGenderElement(){
    let xhr = new XMLHttpRequest();
    
    xhr.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200){
            let data = JSON.parse(this.responseText);
            male = data['male'];
            female = data['female'];
            removeElement("gendergauge");
            makeGenderElement(male, female);
        }
    };
    
    xhr.open("GET", "/genderData/", true);
    xhr.send();
}

function makeGenderElement(male, female){
    var genderBlock = document.getElementById("genderBlock");
    var svg = document.createElement("svg");
    svg.setAttribute('id','gendergauge');
    svg.setAttribute('width',"100%");
    svg.setAttribute('height',"200");
    genderBlock.appendChild(svg);

    var config1 = liquidFillGaugeDefaultSettings();
    config1.circleColor = "#375a7f";
    config1.textColor = "#fff";
    config1.waveTextColor = "#fff";
    config1.waveColor = "#3498DB";
    config1.circleThickness = 0.2;
    config1.textVertPosition = 0.2;
    config1.waveAnimateTime = 1000;

    var gendergauge = loadLiquidFillGauge("gendergauge", 100*male/(male+female), config1);
}