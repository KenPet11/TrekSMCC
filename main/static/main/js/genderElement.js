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
            removeElement("labelCol");
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
    svg.setAttribute('style', "display: inline-block");
    genderBlock.appendChild(svg);

    var config1 = liquidFillGaugeDefaultSettings();
    config1.circleColor = "#375a7f";
    config1.textColor = "#fff";
    config1.waveTextColor = "#fff";
    config1.waveColor = "#3498DB";
    config1.circleThickness = 0.2;
    config1.waveAnimateTime = 1000;

    var percentage = loadLiquidFillGauge("gendergauge", 100*male/(male+female), config1);

    var genderCol = document.getElementById("labelCol");
    var cdiv = document.createElement("div");
    cdiv.setAttribute('style','text-align: center');
    genderCol.appendChild(cdiv);
    var div = document.createElement("div");
    div.setAttribute('id', 'genderLabel');
    div.setAttribute('style', "display: inline-block;");
    cdiv.appendChild(div)

    var malelabel = document.createElement("span"); 
    var divLabel = document.createElement("div");
    divLabel.setAttribute('style', "height: 50px; width: 50px; margin: 20px 20px 20px 20px; float: center; border-radius: 50px; background: #3498DB; display: inline-block;");
    malelabel.appendChild(divLabel);
    var maletext = document.createTextNode(percentage[0]); 
    malelabel.appendChild(maletext); 
    div.appendChild(malelabel);

    var femalelabel = document.createElement("span"); 
    var fdivLabel = document.createElement("span");
    fdivLabel.setAttribute('style', "height: 50px; width: 50px; margin: 20px 20px 20px 20px; float: center; border-radius: 50px; background: #e83e8c; display: inline-block;");
    femalelabel.appendChild(fdivLabel);
    var femaletext = document.createTextNode(percentage[1]); 
    femalelabel.appendChild(femaletext); 
    malelabel.appendChild(femalelabel);
}