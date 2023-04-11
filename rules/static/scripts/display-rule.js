class ruleBlock {
    constructor(ruleDict) {
        this.desc = ruleDict['description'];
        this.num = ruleDict['op'];
        this.rulesList = ruleDict['arg'];
        
        console.log("desc: ", this.desc);
        console.log("num: ", this.num);
        console.log("rulesList: ", this.rulesList);

        // Create parent container
        var $container = $('<div>', {
            'class':'rules-container',
            'id' : this.desc.replace(/\s+/g, '') // Use description as ID w/ no spaces
        }); 
        
        // Create container to hold chips
        var $courseContainer = $('<div>', {
            'class':'rules-chip-container',
        }); 

        // Create title for container
        var $title = $('<h3>');
        $title.html(this.desc);
        $container.append($title);

        // Create list of components
        if (this.rulesList.length > 8) { // If this has more than 8 classes...
            for (let i = 0; i < 8; i++) {
                var chip = new courseChip(this.rulesList[i], false);
                $courseContainer.append(chip.getComponent());
            } 
            
            var $seeMoreButton = $('<button>', {
                'class':'see-more-button',
            }).html('See More'); 
            $container.append($courseContainer);
            $container.append($seeMoreButton);
        }
        else {
            console.log("Less than 8");
            this.rulesList.forEach(function(course){
                var chip = new courseChip(course, false);
                $courseContainer.append(chip.getComponent());
            }); 
            $container.append($courseContainer);  
        }

        this.elt = $container;
    }

    addToPage() {
        $("#rule-display-container").append(this.elt);
     }

    // remove() {
    //     $(this.elt).remove();
    // }
}