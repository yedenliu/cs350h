var courseList = [''];
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
    console.log("dept: ", dept, "level: ", level);

    // Call Query
    $.get( "/" + level + "levels/" + dept, function( data ) {
        $( "#debug" ).html( data );
        alert( "Load was performed." );

        $("#courses-empty-state-container").css("display", "none");
        console.log(data)
        var classArray = data['level' + level]
        console.log(classArray)
        classArray.forEach(function(course){
            console.log('course: ', course);
            var courseName = course[0] + ' ' + course[1];
            var component = new courseChip(course);
            component.addToPage("added-courses-section");

            /** Append course to list */
            courseList.push(course);
        });
        $("#batch-add-dept").val('');
    });
})
/** Create function that formats class number
 *  Also add course number to list
 */

// $.get('someurl', function(response){
//     // process the respose
// });

// Get dept from input

// $.get( "/200levels/" + dept, function( data ) {
//     $( ".result" ).html( data );
//     alert( "Load was performed." );
//   });

// Wnen we're ready to post to the database
// $.post('someURL', 
//     JOSN.stringify(myVar),
//     myVar,
//     function(resp){}
// );
/** Create function that formats rules into a list of dictionaries
 */
function formatRules (){
    // Use courselist, descrip, nfrom to turn into dictionary
    // EVENT LISTNER
}

/** Final formatting for department JSON
 */

