
var current_tab = "live";
var live_data = [];
var live_labels = [];
var chartColor;


function makeChart(labels, data, tab){

	current_tab = tab;
	if (current_tab == "live"){
		chartColor = "rgb(231,76,60)";
	}
	else if (current_tab == "day"){
		chartColor = "rgb(55,90,127)";
	}
	else if (current_tab == "week"){
		chartColor = "rgb(0,188,140)";
	}
	else if (current_tab == "month"){
		chartColor = "rgb(52,152,219)";
	}
	else if (current_tab == "year"){
		chartColor = "rgb(243,156,18)";
	}
	var config = {
		type: 'line',
		data: {
			labels: labels,
			datasets: [{
				label: 'Tweet Sentiment',
				backgroundColor: chartColor,
				borderColor: chartColor,
				data: data,
				fill: false
			}]
		},
		options: {
			responsive: true,
			title: {
				display: true,
				text: 'How People are Talking About Trek'
			},
			tooltips: {
				mode: 'index',
				intersect: false,
			},
			hover: {
				mode: 'nearest',
				intersect: true
			},
			scales: {
				xAxes: [{
					display: true,
					scaleLabel: {
						display: true,
						labelString: 'Time'
					}
				}],
				yAxes: [{
					display: true,
					scaleLabel: {
						display: true,
						labelString: 'Tweet Sentiment'
					}
				}]
			}
		}
	};

	var ctx = document.getElementById('canvas').getContext('2d');
	window.myLine = new Chart(ctx, config);
}

function getData(){
	let xhr = new XMLHttpRequest();
	
	xhr.onreadystatechange = function () {
		if (this.readyState == 4 && this.status == 200){
			let data = JSON.parse(this.responseText);
			live_data = data["scores"];
			live_labels = data["times"];
			if (current_tab === "live"){
				makeChart(live_labels, live_data,"live");
			}
		}
	};
	
	xhr.open("GET", "/latest/", true);
	xhr.send();
}

function respondToTweet(args){
	console.log(args);
	let http = new XMLHttpRequest();

	http.onreadystatechange = function () {
		if (this.readyState == 4 && (this.status == 200 || this.status == 404)){
			//let data = JSON.parse(this.responseText);
			console.log(this.responseText)
		}
	};
	
	http.open("GET", "/sendTweet/" + args, true);
	http.send();
}

window.onload = function() {
	setInterval(getData, 60000);
	makeChart(live_data, live_labels, "live");
	getData();
	document.getElementById("Live").addEventListener('click', function () {
		makeChart(live_labels, live_data,"live");
	});
	setInterval(getFeed, 60000);
	getFeed();
	document.getElementById("feed").addEventListener("click",function(e) {
        if(e.target && (e.target.nodeName == "A" || e.target.nodeName == "P") ) {
            console.log(e.target.id + " was clicked");
            respondToTweet(e.target.id);
        }
    });
    setInterval(getWordCloud, 60000);
    getWordCloud();
};