class courseChip {
    constructor(name, remove) {
        this.name = name;
        this.elt = $('<div>', {
            'class':'course-chip'
        }); 
        var $courseName =  $('<div>',{
            'class':'course-chip-name'
        }); 
        $courseName.html(name);

        var $remove = $('<img>', {
            'class': 'course-chip-remove',
            'src':'static/images/remove.png'
        }); 

        if (remove) {
            console.log("remove: ", remove);
            this.elt.append($courseName).append($remove);
        }
        else {
            this.elt.append($courseName);
        }

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