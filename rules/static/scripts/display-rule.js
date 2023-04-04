class ruleBlock {
    constructor(ruleDict) {
        this.desc = ruleDict['description'];
        this.num = ruleDict['op'];
        this.rulesList = ruleDict['arg'];
        
        // Create container to hold chips
        var $container = $('<div>', {
            'class':'rules-container',
            'id' : desc.replace(/\s+/g, '') // Use description as ID w/ no spaces
        }); 
        
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
                var chip = new courseChip(rulesList[i]);
                $courseContainer.append(chip.getComponent());
            } 

            var $seeMoreButton = $('<button>', {
                'class':'see-more-button',
            }).html('See More'); 
            $container.append($courseContainer);
            $container.append($seeMoreButton);
        }
        else {
            rulesList.forEach(function(course){
                var chip = new courseChip(course);
                $courseContainer.append(chip.getComponent());
            }); 
            $container.append($courseContainer);  
        }

        this.elt = $container;
    }

    addToPage() {
        $("#rule-display").append(this.elt);
     }

    // remove() {
    //     $(this.elt).remove();
    // }
}