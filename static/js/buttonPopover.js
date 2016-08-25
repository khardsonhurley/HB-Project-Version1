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
                return result; 
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
            $('.panel-body').append(text + ':' + translatedText);
            //still need to add these things to the database. Do here or do in server 
            //file? 
        }

        function firstPopover(){
            // returns an object with {'text':text, 'selection':selection}
            var textSelection= getText();
            // gets the selection from the object. 
            var selection = textSelection['selection'];
            // gets the text from the object. 
            var text = textSelection['text'];
            //create the popover that has the buttons(template - global var) in it. 
            createPopover(template, selection);
        }
        
        function showTranslation(){
            console.log('im in showTranslation');
            var selection = getText();
            debugger;
            //seems like i shouldnt have to do this again. How can I pass it in from the previous function? 
            var translation = translateText(selection); 
            //change the content attribute of the popover to now include translation.
            $('.popover').data({'content': translation});

            
        }
        
        // function makeComment(){
        //   //this function would create an html element in the comment sidebar.
        // }
        

///////////////////////////////////////////////////////////////////////////////
/////////////////////////////    EVT LISTENERS    /////////////////////////////
///////////////////////////////////////////////////////////////////////////////

        $('#article-body').mouseup(function(event){
            firstPopover();
            console.log('Mouseup')
            event.stopPropagation(); 
        });

        $(document).on('click', '#translate-button', function(){
            console.log('clicked me');
            showTranslation();
        });

        $(document).on('click', '#comment-button', function(){
            alert('no comment allowed!');
        });

     

        //need an event listener that will clear the popover after user is done with translation.
        // $('#article-body').....
        
        
        // $('#comment-button').click(function(event){
        //     //need to call a function that opens a comment in the comment side-bar.
        // });
});

 
