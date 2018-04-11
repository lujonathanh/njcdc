    // var lineChartData = {
    //     labels: ['', '', '', ''],
    //     datasets: [{
    //         label: "Memory Usage",
    //         fillColor: "rgba(151,187,205,0.2)",
    //         strokeColor: "rgba(151,187,205,1)",
    //         pointColor: "rgba(220,220,220,1)",
    //         pointStrokeColor: "#fff",
    //         pointHighlightFill: "#fff",
    //         pointHighlightStroke: "rgba(220,220,220,1)",
    //         data: [13, 56, 45, 34]
    //     }, {
    //         label: "Base Usage",
    //         fillColor: "rgba(246,150,121,0.2)",
    //         strokeColor: "rgba(242,108,079,1)",
    //         pointColor: "rgba(151,187,205,1)",
    //         pointStrokeColor: "#fff",
    //         pointHighlightFill: "#fff",
    //         pointHighlightStroke: "rgba(151,187,205,1)",
    //         data: [15, 18, 35, 66]
    //     }]
    // }

    // //Get the context of the canvas element we want to select
    // var ctx = $("#memoryTrendChart").get(0).getContext("2d");
    // // This will get the first returned node in the jQuery collection.
    // var myNewChart = new Chart(ctx).Line(lineChartData, {
    //     animationSteps: 15,
    //     bezierCurve: false,
    //     pointDot: false,
    //     showScale: false,
    //     scaleShowLabels: false,
    //     showTooltips: false,
    //     responsive: true
    // });
$( document ).ready(function() {

    var c=document.getElementById("canvas");
    var ctx=c.getContext("2d");
    ctx.beginPath();
    ctx.arc(95,50,40,0,2*Math.PI);
    ctx.stroke();

});

var densityCanvas = document.getElementById("densityChart");

Chart.defaults.global.defaultFontFamily = "Lato";
Chart.defaults.global.defaultFontSize = 18;

var densityData = {
  label: 'Density of Planets (kg/m3)',
  data: [5427, 5243, 5514, 3933, 1326, 687, 1271, 1638]
};

var barChart = new Chart(densityCanvas, {
  type: 'bar',
  data: {
    labels: ["Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"],
    datasets: [densityData]
  }
});