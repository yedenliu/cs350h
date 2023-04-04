var courseList = [];
var rulesList = [];
var rdesc = $("#rdesc").val();
var op = $("#rnum").val();


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
    var component = new courseChip(course);
    component.addToPage("added-courses-section");
    $("#courses-empty-state-container").css("display", "none");
    $("#add-class").val('');

    /** Append course to list */
    courseList.push(course);
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
            var component = new courseChip(courseName);
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
})

$('#submit-major').on("click", function(event) {
    var dept = $("#dept-name").val();
    var finalJSON = {
        "deptName" : dept,
        "rules": rulesList
    }
    
    $.post("/submit/" + dept, {"majorJSON": finalJSON})
    alert( "POST was performed." );
});
/** Create function that formats class number
 *  Also add course number to list
 */

// $.get('someurl', function(response){
//     // process the respose
// });

// Get dept from input
/** Create function that formats rules into a list of dictionaries
 */
function formatRules (){
    // Use courselist, descrip, nfrom to turn into dictionary
    // EVENT LISTNER
}

/** Final formatting for department JSON
 */

