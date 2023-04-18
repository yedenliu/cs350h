var courseList = [];
var rulesList = [];
var rdesc = $("#rdesc").val();
var op = $("#rnum").val();

var base_url = '/majormatch-admin'; 
var pathname = window.location.pathname;
var pathArray = pathname.split('/');
var dept = pathArray[pathArray.length-1];

function isCharNumber(c) {
    return c >= '0' && c <= '9';
  }

function formatClass(course) {
    var courseLet = '';
    var courseNum = '';
    course.forEach(function(char){
        if (isCharNumber(char)) {
            courseNum += char;
        }
        else {{
            courseLet += char;
        }}
    });
    
}
/**
 * event handler for button that adds course
 */
$("#add-class-button").on("click", function(event) {
    var clickee = event.target;
    var course = $("#add-class").val();
    var component = new courseChip(course, true);
    component.addToPage("added-courses-section");
    $("#courses-empty-state-container").css("display", "none");
    $("#add-class").val('');

    /** Append course to list */
    courseList.push(course);

     /**
     * event handler to remove course
     */
    $(".course-chip-remove").on("click", function(event) {
        var clickee = event.target;
        var $chip = $(clickee).closest(".course-chip");
        var courseName = $chip.find('.course-chip-name').html();
        console.log("removing: ", courseName);

        console.log("courseList: ", courseList);
        courseList = courseList.filter(item => item !== courseName)
        console.log("courseList updated: ", courseList);

        // remove course from HTML
        $chip.remove();
    });
})


/**
 * event handler for when user batch adds course
 */
$("#batch-add-button").on("click", function(event) {
    var clickee = event.target;
    var dept = $("#batch-add-dept").val();
    var level = $('#class-levels option:selected').val();

    // Call Query
    // need a prefix for the url
    // FIX!
    // var base_url = window.location.pathname; 
    var base_url = '/majormatch-admin'; 
    $.get( base_url + "/" + level + "levels/" + dept, function( data ) { 
        $( "#debug" ).html( data );
        // alert( "Load was performed." );

        $("#courses-empty-state-container").css("display", "none");
        var classArray = data['level' + level]
        classArray.forEach(function(course){
            var courseName = course[0] + ' ' + course[1];
            var component = new courseChip(courseName, true);
            component.addToPage("added-courses-section");

            /** Append course to list */
            courseList.push(courseName);
        });
        $("#batch-add-dept").val('');
    });
})

/**
 * event handler for button that adds a rule
 * by building a json and showing added courses on the right side
 */
$("#add-rule-button").on("click", function(event) {
    rdesc = $("#rdesc").val();
    op = $("#rnum").val();

    // if ((rdesc.length == 0) || (op.length == 0))

    var ruleDict = {
        "description": rdesc,
        "op": "nfrom-" + op,
        "arg": courseList
    };

    /** Append rules to list of rules */
    rulesList.push(ruleDict);
    var ruleElt = new ruleBlock(ruleDict);
    ruleElt.addToPage();
    console.log("Rule Added!")

    // Clear courses
    $("#courses-empty-state-container").css("display", "flex");
    $("#added-courses-section").empty();

    // Reset variables
    $("#rdesc").val('');
    $("#rnum").val('');
    courseList = [];
})

$('#submit-major').on("click", function(event) {
    // var pathname = window.location.pathname;
    // var pathArray = pathname.split('/');
    // var dept = pathArray[pathArray.length-1];

    var finalJSON = {
        "deptName" : dept,
        "rules": rulesList
    }

    var base_url = '/majormatch-admin';
    $.post( base_url + "/submit/" + dept, {"majorJSON": JSON.stringify(finalJSON)})
    alert( "POST was performed." );
});


// Get dept from input
/** Create function that formats rules into a list of dictionaries
 */
function formatRules (){
    // Use courselist, descrip, nfrom to turn into dictionary
    // EVENT LISTNER
}

// Create rule front-end given existing rules
// var rulesList = document.getElementById("rulesList").value;
//     rulesList.forEach(function(el){
//         var ruleElt = new ruleBlock(el);
//         ruleElt.addToPage();
// });

$.get( base_url + "/rules/" + dept, function( data ) { 
    rulesList = data['rules']
    console.log("rulesList: ", rulesList);
    rulesList.forEach(function(course){
        var ruleElt = new ruleBlock(course);
        ruleElt.addToPage();
    });
});


