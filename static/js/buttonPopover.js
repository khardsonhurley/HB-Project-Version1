"use strict";

$(document).ready(function() {

    $('.comment-window').hide();
    //global variable 
    var template = `<button class="btn btn-default translate-button">
            <span class='glyphicon glyphicon-transfer' aria-hidden='true'</span></button>` 
            + " " + 
            `<div class="btn btn-default comment-button">
            <span class='glyphicon glyphicon-comment' aria-hidden='true'</span></div>`+ " "+
            `<div class="btn btn-default twilio-button">
            <span class='glyphicon glyphicon-send' aria-hidden='true'</span></div>`;

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
            console.log(position);
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
        
        function showCommentWindow(){
            //Get the User's selection
            var textSelection = getText();
            //get the selection object
            var selection = textSelection['selection'];
            //find the position using the selection object
            var position = selection.getRangeAt(0).getBoundingClientRect();
            
            var text = textSelection['text'];
            
            //This just moves the comment-window that already exists in the DOM
            //to the position on the same line as the selection. 
            $('#comment-window').offset({top:(position.top) + $(window).scrollTop()});
            $('.commentReference').html('"'+ text+ '"');
            $('.comment-sidebar').css('visibility', 'visible');

            addCommentFormatting(selection); 


        }

        function addCommentFormatting(selection){

            var startOfSelection = selection.getRangeAt(0)['startOffset']; 

            var endOfSelection = selection.getRangeAt(0)['endOffset']; 

            var articleText = $('#article-text').html();

            // var slicedText = articleText.slice(0, startOfSelection) + 
            // commentOpenTag + articleText.slice(startOfSelection, endOfSelection)+ 
            // commentCloseTag + articleText.slice(endOfSelection);


            // var commentOpenTag = '<span class="commentedText">';
            var openSpanTag = '<span>'
            var commentOpenTag = '<span class="commentedText">';

            // commentSpan.attr({'class':'commentedText'})

            // commentSpan.append(articleText.slice(startOfSelection, endOfSelection));


            // commentOpenTag.data({'class': 'commentedText'});

            var closeTag = '</span>'
            
            var slicedText = openSpanTag + articleText.slice(0, startOfSelection) + closeTag
            commentOpenTag + articleText.slice(startOfSelection, endOfSelection)+ 
            closeTag + openSpanTag + articleText.slice(endOfSelection)+ closeTag;

            // console.log(slicedText);

                            
            $('#article-text').replaceWith(slicedText);
            // console.log($('#article-text').children());

        }

        function addComment(evt){
            evt.preventDefault();
            //Gets the text from the input field. 
            var inputText= $('input').val();
            //removes input value
            $('input').val("");

            var commentInput = {
                "comment": inputText
            }
            //sends an Ajax request to server where the comment should be stored
            //in the database. The server returns all comments with that comment_id
            $.post('/comments', commentInput, function(result){
                displayComments(result);
            });
        }

        
        function displayComments(result){

            var commentObject = result.commentData

            for(var i=0; i<commentObject.length; i++){
                var comment = commentObject[i]['userComment'];
                var image = commentObject[i]['userImage'];
                var userName = commentObject[i]['userName'];
                var htmlComment = formatComment(image, userName, comment);
                $('.commentTemplate').append(htmlComment);

            }
        }

        function formatComment(imageUrl, userName, comment){

                var htmlComment= `<li class="">
                    <div class="commenterImage">
                    <img class= "userImage" src=` + imageUrl +
                    `/>
                    </div>
                <div class="commentText">
                    <h6 class='userName'>` + userName + `</h6>
                    <p class="commentBody">` + comment + `</p>
                    <span class="date sub-text">
                    </span>
                </div>
                </li>`

                return htmlComment;

        }
            
            

        
        

///////////////////////////////////////////////////////////////////////////////
/////////////////////////////    EVT LISTENERS    /////////////////////////////
///////////////////////////////////////////////////////////////////////////////

        $('.article-body').mouseup(function(event){
            firstPopover();
            event.stopPropagation(); 
        });


        $(document).on('click', '.translate-button', function(){
            var textSelection = getText();
            var text= textSelection['text'];
            // This function calls the showTranslation function. 
            var translatedText = translateText(text);
            console.log('in the translate click');
        });

        $('.article-body').on('mousedown', function(){
            if ($('.popover')){
                $('.popover').remove();
                }
        });

        $(document).on('click', '.comment-button', function(){
            $('.popover').remove();
            showCommentWindow(); 
            //call some other function here that shows form for comment. 
        });

        $(document).on('click', '#add-comment-button', addComment);
        //Event listener that listens for user to his the 'X' button in the corner
        //of the comment window. 
        $(document).on('click', '.close', function(){
             $('.comment-sidebar').css('visibility', 'hidden');
             $('.commentTemplate').html("");
        });

        //PSEUDO-CODE: User enters a comment into the comment window and clicks
        //"add." This should make a ajax post request to the '/comment' route. 
        //Adding the comment to the DB and now displaying it as one of the comments.

        //PSEUDO-CODE: Another event listener for when the user clicks off the 
        //comment window. Comment window collapses into a icon that is located
        //at the same top position as the selection. Also would like to make 
        //the selection highlighted a light grey so other users can see that it 
        //has a comment on it. 

});

 
