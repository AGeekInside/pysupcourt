function createTagcloud(inputWords,count,w,h) {
	// generates a tag cloud object and returns it
	return d3.layout.cloud().size([w,h])
		.words(inputWords.map(function(d,i) {
			return {text: d, size: 5 + count[i]*5};
		}))
		.rotate(function() { return ~~(Math.random() * 2) * 90; })
		.font("Impact")
		.fontSize(function(d) { return d.size; })
		.on("end", draw)
		.start();
}

function draw(words,location) {
var svg = d3.select("#speaker_0.chart").selectAll("svg")
			.append("svg")
			.attr("width", w)
			.attr("height", h);

	svg.append("g")
  		.attr("transform", "translate(250,250)")
  		.selectAll("text")
    	.data(words)
  		.enter()
  	  .append("text")
    	.style("font-size", function(d) { return d.size + "px"; })
    	.style("font-family", "Impact")
    	.style("fill", function(d, i) { return fill(i); })
    	.attr("text-anchor", "middle")
    	.attr("transform", function(d) {
      		return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
	    })
    	.text(function(d) { return d.text; });
}