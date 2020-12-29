function getData() {
  d3.csv("./assets/data/score.csv").then(function(data) {
    console.log(data[0]);
    console.log(data[0].date);
    document.getElementById("latest date").innerHTML = data[0].date.toString();
    document.getElementById("indicated").innerHTML = data[0].quote.toString();
    document.getElementById("certainty").innerHTML = data[0].current_score.toString();
  });
}

function plot() {
  d3.csv("./assets/data/score.csv").then(function(data) {
    var current_score = parseFloat(data[0].current_score);
    var past_score = parseFloat(data[0].past_score);
    var data = [
      {
        type: "indicator",
        value: current_score,
        delta: { reference: past_score },
        gauge: { axis: { visible: false, range: [-100, 100] } },
        domain: { row: 0, column: 0 }
      }
    ];

    var layout = {
      width: 400,
      height: 250,
      margin: { t: 25, b: 25, l: 25, r: 25 },
      template: {
        data: {
          indicator: [
            {
              title: { text: "Score" },
              mode: "number+delta+gauge",
              delta: { reference: 90 }
            }
          ]
        }
      }
    };
    GAUGE = document.getElementById("gauge");
    Plotly.newPlot(GAUGE, data, layout);
  });
}
