var courseList = [];
var rdesc = $("#rdesc").val();
var op = $("#rnum").val();

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
    courseList.append(course);
})

/** Create function that formats class number
 *  Also add course number to list
 */

// $.get('someurl', function(response){
//     // process the respose
// });

// $.get( "ajax/test.html", function( data ) {
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

