/***
@title:
Live Search

@version:
2.0

@author:
Andreas Lagerkvist

@date:
2008-08-31

@url:
http://andreaslagerkvist.com/jquery/live-search/

@license:
http://creativecommons.org/licenses/by/3.0/

@copyright:
2008 Andreas Lagerkvist (andreaslagerkvist.com)

@requires:
jquery, jquery.liveSearch.css

@does:
Use this plug-in to turn a normal form-input in to a live ajax search widget.
The plug-in displays any HTML you like in the results and the search-results
are updated live as the user types.

@howto:
jQuery('#q').liveSearch({url: '/ajax/search.php?q='}); would add the
live-search container next to the input#q element and fill it with the
contents of /ajax/search.php?q=THE-INPUTS-VALUE onkeyup of the input.

@exampleHTML:
<form method="post" action="/search/">

 <p>
  <label>
   Enter search terms<br />
   <input type="text" name="q" />
  </label> <input type="submit" value="Go" />
 </p>

</form>

@exampleJS:
jQuery('#jquery-live-search-example input[name="q"]').liveSearch(
  {url: Router.urlForModule('SearchResults') + '&q='});
***/
(function($) {
$.fn.liveSearch = function (conf) {
    var config = $.extend({
	cog_oid_:undefined,
	cog_fqtn_:undefined,
	cog_method:undefined,
	target:undefined,
	id: 'jquery-live-search',
	data_type: undefined,
        duration:  400, 
        typeDelay:  200,
	top: 0,
        min_length: 3,
        loadingClass: 'loading', 
        onSlideUp:  function () {}, 
        position: 'absolute'
    }, conf);

    var liveSearchResId = config.id + '_res';
    var liveSearch = $('#' + liveSearchResId);
    var positioned = false;
    // Create live-search if it doesn't exist
    if (!liveSearch.length) {
        liveSearch = $(
	    '<div id="' + liveSearchResId +
		'" class="jquery-live-search"></div>')
            .appendTo(document.body)
            .hide()
            .slideUp(0);

        // Close live-search when clicking outside it
        $(document.body).click(function(event) {
            var clicked = $(event.target);

            if (!(clicked.is('input'))) {
                liveSearch.slideUp(config.duration, function () {
                    config.onSlideUp();
                });
            }
        });
    }

    return this.each(function () {
        var input = $(this).attr('autocomplete', 'off');
	$(this).attr('size', 12);
        var liveSearchPaddingBorderHoriz = parseInt(
            liveSearch.css('paddingLeft'), 10) +
            parseInt(liveSearch.css('paddingRight'), 10) +
            parseInt(liveSearch.css('borderLeftWidth'), 10) +
            parseInt(liveSearch.css('borderRightWidth'), 10);

        // Re calculates live search's position
        var repositionLiveSearch = function () {
            var tmpOffset = input.offset();
            var inputDim = {
                left:  tmpOffset.left, 
                top:  tmpOffset.top, 
                width:  input.outerWidth(), 
                height:  input.outerHeight()
            };

            inputDim.topPos  = inputDim.top + inputDim.height;
            inputDim.totalWidth = inputDim.width - liveSearchPaddingBorderHoriz;

            liveSearch.css({
                position: config.position, 
                left:  inputDim.left + 'px', 
                top:  inputDim.topPos + 'px',
                width:  inputDim.totalWidth + 'px'
            });
        };

        // Shows live-search for this input
        var showLiveSearch = function () {
            // Always reposition the live-search every time it is shown
            // in case user has resized browser-window or zoomed in or whatever
	    if(!positioned){
		repositionLiveSearch();
		positioned = true;
	    };
            // We need to bind a resize-event every time live search is shown
            // so it resizes based on the correct input element
            $(window).unbind('resize', repositionLiveSearch);
            $(window).bind('resize', repositionLiveSearch);
            $('#cog_container .page > article').unbind(
		'scroll', repositionLiveSearch);
            $('#cog_container .page > article').bind(
		'scroll', repositionLiveSearch);

            liveSearch.slideDown(config.duration);
        };

        // Hides live-search for this input
        var hideLiveSearch = function () {
            liveSearch.slideUp(config.duration, function () {
                config.onSlideUp();
            });
        };

        input
        // On focus, if the live-search is empty, perform an new search
        // If not, just slide it down. Only do this if there's something
        // in the input
            .focus(function () {
                if (this.value !== '') {
                    // Perform a new search if there are no search results
                    if (liveSearch.html() == '') {
                        this.lastValue = '';
                        input.keyup();
                    }
                    // If there are search results show live search
                    else {
                        // HACK: In case search field changes width onfocus
                        setTimeout(showLiveSearch, 1);
                    }
                }
		else {
		    liveSearch.html($(this).attr("hint") || '');
		    showLiveSearch();
		}
            })
        // Auto update live-search onkeyup
            .keyup(function () {
                // Don't update live-search if it's got the same value as
                // last time or the length of the string is less than min_length
                if (this.value.length >= config.min_length &&
                    this.value != this.lastValue) {
                    input.addClass(config.loadingClass);

                    var q = this.value;

                    // Stop previous ajax-request
                    if (this.timer) {
                        clearTimeout(this.timer);
                    }

                    // Start a new ajax-request in X ms
                    this.timer = setTimeout(function () {
			var proxy = '';
			ref_obj = 'cog_fqtn_=' + config.cog_fqtn_;
			if(config.cog_oid_){
			    ref_obj = '&cog_oid_=' + config.cog_oid_;
			}
			url ='?' + ref_obj +
			    '&target=' + config.target +
			    '&cog_method=' + config.cog_method +
			    '&cog_ajax=True' +
			    '&q=' + q;
			if(config.callback){
			    url += '&callback=' + config.callback;
			}
			if(config.action){
			    url += '&action=' + config.action;
			}
			//console.log(url)
                        $.get(url, function (data) {
                            input.removeClass(config.loadingClass);

                            // Show live-search if results and search-term
                            // aren't empty
			    json_data = $.parseJSON(data);
                            if (data.length && q.length >= config.min_length) {
                                liveSearch.html(
				    //data);
				    json_data['null']["content"]);
                                showLiveSearch();
                            }
                            else {
                                hideLiveSearch();
                            }
                        });
                    }, config.typeDelay);

                    this.lastValue = this.value;
                }
            });
    });
};
})(jQuery)
