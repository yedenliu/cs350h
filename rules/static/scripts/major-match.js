var userCourseList = [];
var userMajors = [];
var matchResults = [];

// get majors entered
function onlyUnique(value, index, array) {
    return array.indexOf(value) === index;
  }
  
// usage example:
// array.filter(onlyUnique);

function ruleCheck(courseList, relevantList, requirementNum) {
    /*
    Checks if enough course are taken from a list of applicable courses
    
    Params - courseList: user's course list
    relevantList: courses that apply to rule
    requirement: how many courses they need to fulfill
    
    Return - Array: [courseCount, boolean, countedCourses]
    courseCount: how many courses have been fulfilled
    boolean: true if requirements are fulfilled. false otherwise
    countedCourses: the courses that have been counted
    */
    
    let courseCount = 0; // how many courses have been fulfilled
    let countedCourses = [];
    
    for (let i = 0; i < courseList.length; i++) {
        let course = courseList[i];
        if (relevantList.includes(course)) {
            courseCount++;
            countedCourses.push(course);
            if (courseCount === requirementNum) {
                return [courseCount, true, countedCourses];
                }
        }
    }
    
    return [courseCount, false, countedCourses];
}

function parseMajor(inputJSON, courseList) {
    /*
    Takes in a user's course list and a department's major requirement JSON with
    the relevant rules, giving back the user's major progress
    
    Param - inputJSON: department's JSON w/ major requirements
    courseList: list of user's taken courses
    Return - major progress (proportion)
    */
    
    let parseDict = JSON.parse(inputJSON);
    let totalUnits = parseDict['units'];
    let studentUnits = 0;
    let currentCourses = courseList;
    
    for (let i = 0; i < parseDict['rules'].length; i++) {
    let rules = parseDict['rules'][i];
    let requirementNum = rules['op'].split('-')[1];
    let relevantList = rules['arg'];

    let [courseCount, isFulfilled, countedCourses] = ruleCheck(currentCourses, relevantList, requirementNum);
    currentCourses = [...new Set(currentCourses.concat(countedCourses))]; // a course can only be counted for one rule 
    studentUnits += courseCount;
    }

    console.log("Student Units / Total Units: ", studentUnits, "/", totalUnits);
    var unitsLeft = totalUnits - studentUnits;
    if (unitsLieft < 0) {
        unitsLeft = 0
    }
    console.log("Units left: ", unitsLeft);
    return [studentUnits / totalUnits, unitsLeft];
    }

    // #-------------------------------------------------------------------------------
    // # DEPARTMENT JSONS
    // #-------------------------------------------------------------------------------
    // # example dictionary...will move to JSON
    // # Focus on majority (think about edge cases later...aka someone who skipped CS111 or CS230)
    csJSON = '{"deptName": "cs", "units": 10, "rules": [ \
                        {"title": "intro", "op": "nfrom-2", "arg": ["cs 111", "cs 230"]},\
                        {"title": "math", "op": "nfrom-1", "arg": ["math 225"]},\
                        {"title": "core", "op": "nfrom-3", "arg": ["cs 231", "cs 235", "cs 240"]},\
                        {"title": "200 levels", "op": "nfrom-2", "arg": ["cs 204", "cs 220", "cs 221", "cs 232", "cs 234", "cs 242", "cs 251", "cs 304", "cs 305", "cs 307", "cs 313", "cs 315", "cs 320", "cs 321", "cs 323", "cs 333", "cs 342", "cs 343"]}, \
                        {"title": "300 levels", "op": "nfrom-2", "arg": ["cs 304", "cs 305", "cs 307", "cs 313", "cs 315", "cs 320", "cs 321", "cs 323", "cs 333", "cs 342", "cs 343"]} \
                    ] \
            }'


test1_courses = ['cs 111', 'cs 230', 'cs 231', 'cs 235', 'cs 242', 'cs 304', 'cs 305', 'cs 240', 'cs 220', 'math 225']
test2_courses = ['cs 111', 'cs 230', 'cs 231', 'cs 235', 'cs 204', 'cs 220', 'cs 304', 'cs 321', 'cs 323', 'math 225']
            
parseMajor(csJSON, test1_courses)
parseMajor(csJSON, test2_courses)


// Front-End Add Courses

/**
 * event handler for button that adds course
 */
$("#add-class-button").on("click", function(event) {
    var clickee = event.target;
    var course = $("#add-class").val();
    var component = new courseChip(course, true);
    component.addToPage("added-courses-section");

    // Add major abbrehviation to major list 
    var major = course.split(' ')[0];
    console.log("major: ", major);
    userMajors.push(major);

    // Empty input and remove state
    $("#courses-empty-state-container").css("display", "none");
    $("#add-class").val('');

    /** Append course to list */
    userCourseList.push(course);
     /**
     * event handler to remove course
     */
    $(".course-chip-remove").on("click", function(event) {
        var clickee = event.target;
        var $chip = $(clickee).closest(".course-chip");
        var courseName = $chip.find('.course-chip-name').html();
        console.log("removing: ", courseName);

        console.log("courseList: ", userCourseList);
        userCourseList = userCourseList.filter(item => item !== courseName)
        console.log("courseList updated: ", userCourseList);

        // remove course from HTML
        $chip.remove();
    });
})

$("#major-match").on('click', function(event) {
    getMajorJSON();
});
                
async function getMajorJSON() {
    var majorList = onlyUnique(userMajors);   
    for (m of majorList) {
        await $.get( base_url + "/major-match/" + dept, function( data ) { 
            var majorJSON = data['majorJSON']
            console.log("majorJSON: ", majorJSON);
            
            // Major Matching
            var matchInfoList = parseMajor(majorJSON, userCourseList);
            var matchDict = {'dept': dept, 
                            'matchList': matchInfoList};
            matchResults.push(matchInfoList); 
        });
    }
    console.log("All done");
}

getMajorJSON();


// Write up - audience some student (someone who would like to build off this project)
// Take them through the project
// Include things that we didn't finish and would like to
// Ask Indira? 