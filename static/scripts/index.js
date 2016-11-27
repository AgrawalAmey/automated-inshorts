var sb = null;

function getData(){
    $.getJSON('/get_stories',function(data){
        $.each(data.stories, function(i,data){
        	var content = '';
			content += "<div class='card-panel grey lighten-5 z-depth-1'>";
			content +=		"<h4 class='card-title'>" + data.title + "</h4>";
			content +=      "<div class='row valign-wrapper card-content'>";
			content +=	        "<div class='col s12'>";
			content +=	         	"<span class='black-text'>";
			content +=	            	data.short;
			content +=	            "</span>";
			content +=	        "</div>";
			content +=      "</div>";
			content +=      "<span class='date-log'><i>"+ data.created_on +"</i></span>";
			content += "</div>";
            $(content).appendTo('#stories');
        });
    }); 
}

$(document).ready(function(){
	getData();
	
	// Refresh every 15 mins
	setInterval(function(){
		getData();
	}, 900000);
});