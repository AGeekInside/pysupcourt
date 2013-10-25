var rowLabelOffset = 130;
var colLabelOffset = 160;
//height of each row in the heatmap
var h = 40;
//width of each column in the heatmap
var w = 40;

function createSVG(name,cols,rows) {
	return d3.select("#"+name)
	.append("svg")
	.attr("width", (w * cols.length) + (rowLabelOffset + (h+0.5))) 
	.attr("height", (h * rows.length + colLabelOffset))
/* 		         
   	.style('position','absolute')
	.style('top',0)
	.style('left',0);
 */   
}	
   
function createHeatmapRows(workSVG,workData) {
	return workSVG.selectAll(".heatmap")
	.data(workData)
	.enter().append("g");
}
   
function createHeatmapRects(workHeatmapRows) {
	return workHeatmapRows
	.selectAll(".rect")
	.data(function(d) {
		return d;
	})
//	.enter().append("svg:rect")
//	.attr('width',w)
//	.attr('height',h)
//	.attr('x', function(d) {
//		return (d[2] * w) + 65;
//	})
//	.attr('y', function(d) {
//		return (d[1] * h) + 50;
//	})
//	.style('fill',function(d) {
//		return colorScale(d[0]);
//	});	   
	.enter().append("svg:circle")
	.attr('r',18)
	.attr('cx', function(d) {
		return (d[2] * w) + rowLabelOffset + (0.5*w);
	})
	.attr('cy', function(d) {
		return (d[1] * h) + colLabelOffset + (0.5*h);
	})
	.style('fill',function(d) {
		return colorScale(d[0]);
	});	   

}
   
function createColumnLabel(workSVG,cols) {
	return workSVG.selectAll(".colLabel")
	.data(cols)
	.enter().append('svg:text')
//	.attr('rotate', function(d,i) {
//		x = ((i + 0.5) * w) + rowLabelOffset;
//		return '( 90 '+x+' 0 )';
//	})
	.attr('x', function(d,i) {
		return ((i + 0.5) * w) + rowLabelOffset;
	})
	.attr('y', 30)
	.attr('class','label')
	.style('text-anchor','right')
	.text(function(d) {return d;})
	.attr('transform', function(d,i) {
		x = ((i + 0.5) * w) + rowLabelOffset;
		y = 30;
		workStr = 'rotate(90 '+x+' '+y+')';
		return workStr
	});
}
   
function createRowLabel(workSVG,rows) {
	return workSVG.selectAll(".rowLabel")
	.data(rows)
	.enter().append('svg:text')
	.attr('x', 0)
	.attr('y', function(d,i) {
		return((i+0.5) * h) + colLabelOffset + 5;
	})
	.attr('class','label')
	.style('text-anchor','left')
	.text(function(d) {return d;});
}

function mouseOver(obj, d, i) {
	d3.select(obj)
	.attr('stroke-width',1)
	.attr('stroke','black')
	div.transition()        
       .duration(200)      
       .style("opacity", .9);      
    div.html('dist = '+d[0].toPrecision(3)+
    		'<br>row = '+d[1]+
    		'<br>col = '+d[2])  
       .style("left", (d3.event.pageX) + "px")     
       .style("top", (d3.event.pageY - 28) + "px");
	displayChart(d);
}

function mouseOut(obj, d, i) {
   d3.select(obj)
   	.attr('stroke-width',0)
   	.attr('stroke','none')
   	div.transition()        
   	.duration(500)      
   	.style("opacity", 0); 
}

   
   /*       var expLab = d3.select("body")
   .append('div')
   .style('height',23)
   .style('position','absolute')
   .style('background','FFE53B')
   .style('opacity',0.8)
   .style('top',0)
   .style('padding',10)
   .style('left',40)
   .style('display','none');
*/
//heatmap mouse events
/*        heatmapRow
   .on('mouseover', function(d,i) {
      d3.select(this)
         .attr('stroke-width',1)
         .attr('stroke','black')
*//*                .attr("text-anchor", "middle")
		   .text(function(d,i) {return d;})
*/ 
/* 			output = '<b>' + rows[i] + '</b><br>';
      for (var j = 0 , count = data[i].length; j < count; j ++ ) {
         output += data[i][j][0].toPrecision(3) + ", ";
      }
      expLab
         .style('top',(i * h))
         .style('display','block')
         .html(output.substring(0,output.length - 3));
})
.on('mouseout', function(d,i) {
   d3.select(this)
      .attr('stroke-width',0)
      .attr('stroke','none')
   expLab
      .style('display','none')
});
*/

