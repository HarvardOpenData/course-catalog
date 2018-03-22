/* 
courses_happening is a vector of length 24*60 where the i-th entry in the vector
counts the number of courses happening at i minutes from midnight
*/
var courses_happening = [];
for (var i = 0; i < 24*60; i++) {
	// Set every value to zero
	courses_happening[i] = 0;
}
for (var i = 0; i < courses.length; i++) {
	for (var j = courses[i].start_time; j < courses[i].end_time; j++) {
		courses_happening[j] += 1;
	}
}

var svg = d3.select("svg"),
    margin = {top: 20, right: 20, bottom: 30, left: 50},
    width = +svg.attr("width") - margin.left - margin.right,
    height = +svg.attr("height") - margin.top - margin.bottom,
    g = svg.append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");

// Time vector
var time = [];
for (var i = 0; i < 24*60; i++) {
	time[i] = i;
}


// Struggling with d3
var line = d3.line()
    .x(function(d) { return time; })
    .y(function(d) { return courses_happening; });

svg.append("path")
      .attr("d", line);