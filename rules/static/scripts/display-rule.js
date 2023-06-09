class ruleBlock {
    constructor(ruleDict) {
        this.dict = ruleDict;
        this.desc = ruleDict['description'];
        this.num = ruleDict['op'];
        this.courseList = ruleDict['arg'];
        
        console.log("desc: ", this.desc);
        console.log("num: ", this.num);
        console.log("courseList: ", this.courseList);

        // Create parent container
        var $container = $('<div>', {
            'class':'rules-container',
            'id' : this.desc.replace(/\s+/g, '') // Use description as ID w/ no spaces
        }); 
        
        // Create container to hold chips
        var $courseContainer = $('<div>', {
            'class':'rules-chip-container'
        }); 

        // Create title container 
        var $headerContainer = $('<div>', {
            'class': 'rules-chip-header'
        })
        
        // Create title for container
        var $title = $('<h3>');
        $title.html(this.desc);
        $headerContainer.append($title);

        // Create remove button
        var $remove = $('<h3>', {
            'class': 'rules-remove'
        });
        $remove.html('Remove');
        $headerContainer.append($remove);

        $container.append($headerContainer);

        // Create list of components
        if (this.courseList.length > 8) { // If this has more than 8 classes...
            for (let i = 0; i < 8; i++) {
                var chip = new courseChip(this.courseList[i], false);
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
            this.courseList.forEach(function(course){
                var chip = new courseChip(course, false);
                $courseContainer.append(chip.getComponent());
            }); 
            $container.append($courseContainer);  
        }

        $($container).on("click", '.rules-remove', event => {
           this.removeRule();
           // Update rules var
           rulesList = rulesList.filter(item => item !== ruleDict);
           console.log("rulesList in display-rule: ", rulesList);
        });

        this.elt = $container;
    }

    addToPage() {
        $("#rule-display-container").append(this.elt);
     }

    removeRule() {
        console.log("Remove rule !!!");
        $(this.elt).remove();
        return this.desc
    }
}