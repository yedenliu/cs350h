class courseChip {
    constructor(name) {
        this.name = name;
        this.elt = $('<div>', {
            'class':'course-chip'
        }); 
        var courseName =  $('<div>'); 
        courseName.html(name);

        var remove = $('<image>', {
            'class': 'course-chip-remove',
            'src':'../images/remove.png'
        }); 

        this.elt.append(courseName).append(remove);
    }

    addToPage(destination) {
        $("#" + destination).append(this.elt);
     }

    getComponent() {
        return this.elt;
    }

    remove() {
        $(this.elt).remove();
    }
}