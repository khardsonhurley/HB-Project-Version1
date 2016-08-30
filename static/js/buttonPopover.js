"use strict";

$(document).ready(function() {

//global variable 
var template = '<button class="btn btn-success" id="translate-button">Translate</button>  ' +
               '  <div class="btn btn-default" id="comment-button">Comment</div>';

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////    FUNCTIONS    ///////////////////////////////
///////////////////////////////////////////////////////////////////////////////

        function getText(){
            //on the window, this gets the translated text from the window. 
            var selection = window.getSelection();  

            var text = selection.toString();

            return {
                    'selection': selection,
                    'text':text
            }
        }

        function translateText(text){

            // Request.form.get requires a dictionary to read it.
            var translationInput = {
                "phrase": text
            }
            //send a post request to the translate route, remember the middle 
            //value is the data you are sending to the route. This must be in 
            //dictionary format for request.form.get(). The result of that
            //is passed into the an anonymous function (because we wanted to
            // pass in two things: translated result and the location of it.)
            $.post("/translate", translationInput, function(result){
                showTranslation(result);
                addToVocabList(translationInput["phrase"], result);
            });
        }

        function createPopover(content, selection){
            // get the position of the selection. This instantiates an object
            //of the class ClientRect that has all information about the position
            //of the rectangle placed around the selection. 
            var position = selection.getRangeAt(0).getBoundingClientRect();
            var thePopover = $('<span>');
            var length = selection.toString().length

            //sets the tooltip data. 
            thePopover.data({'content': content , 'toggle':'popover', 'placement': 'top', 'html': true});

            //add the span to the html. 
            $('body').append(thePopover);

            //puts the popover right above the position of the selection. 
            thePopover.offset({top: (position.top) + $(window).scrollTop(), left: position.left + (7*length)/2});

            //initializes the popover, without this it will not show. 
            thePopover.popover('show');

        }

        function addToVocabList(text, translatedText){
            // add text and translatedText to the html panel vocab list area. 
            $('.panel-body').append(text + ': ' + translatedText+".");
        }

        function firstPopover(){
            // returns an object with {'text':text, 'selection':selection}
            var textSelection= getText();
            // gets the selection from the object. 
            var selection = textSelection['selection'];
            var text = textSelection['text'];
            //Only want to create a popover if there is text in the selection.
            if (text){
                //create the popover that has the buttons(template - global var) in it. 
                createPopover(template, selection);
            }
        }
        
        function showTranslation(translation){
            //had to make this in html because the tooltip's html value was set
            //to true so it now only takes html. Is there a better way to do this? 
            var htmlTranslation = '<p>'+translation+'</p>';
            //Changes the html to display the translation. Also moves the popover
            //over slightly. Why is this? 
            $('.popover-content').html(htmlTranslation);

        }
        
        function createComment(){
            //creates a placeholder div. 
            // var comment = $('<div>');
            // comment.data({'content':'<p>this is a test</p>', toggle:'popover', html:true}); 
            var textSelection = getText();
            var selection = textSelection['selection'];
            var position = selection.getRangeAt(0).getBoundingClientRect();

            var commentField = `
                <div class="form-group">
                    <input class="form-control" type="text" placeholder="Your comments" />
                </div>
                <div class="form-group">
                    <a><button class="btn btn-default">Add</button></a>
                </div>
            `;


            $('#comment-sidebar').html(commentField).offset({top:(position.top)});
            console.log('in create comment');

        }
        

///////////////////////////////////////////////////////////////////////////////
/////////////////////////////    EVT LISTENERS    /////////////////////////////
///////////////////////////////////////////////////////////////////////////////

        $('.article-body').mouseup(function(event){
            firstPopover();
            console.log('Mouseup')
            event.stopPropagation(); 
        });


        $(document).on('click', '#translate-button', function(){
            var textSelection = getText();
            var text= textSelection['text'];
            // This function calls the showTranslation function. 
            var translatedText = translateText(text);
        });

        $('.article-body').on('mousedown', function(){
            if ($('.popover')){
                $('.popover').remove();
                }
        });

        $(document).on('click', '#comment-button', function(){
            $('.popover').remove();
            createComment(); 
            //call some other function here that shows form for comment. 
        });

});

 
