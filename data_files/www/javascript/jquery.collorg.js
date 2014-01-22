(function($) {
    var trace_page = false;
    $.cog = {};
    var creole = new Parse.Simple.Creole( {
        forIE: document.all,
        interwiki: {
            WikiCreole: 'http://www.wikicreole.org/wiki/',
            Wikipedia: 'http://en.wikipedia.org/wiki/'
        },
        linkFormat: ''
    } );
    var init_path = window.location.pathname;
    var init_path_link = '<a class="action" href="' + init_path +
        '" target="#cog_container">first access</a>"';

    $.fn.cog_resize = function()
    {
        $.cog.header_height_ = $('#header').outerHeight(true);
        $.cog.footer_height_ = $('#footer').outerHeight(true);
        $(this).each(function(){
            //trace_page && console.log('cog_resize: ' + $(this).attr('id'));
            $(this).cog_resizeCogContainer();
            $.cog.height_ = $(window).height() -
                ($.cog.header_height_ + $.cog.footer_height_);
            $(this).cog_pageHeight();
        });
        $('#cog_container').scrollPage();
        return $(this);
    }

    $.fn.cog_resizeCogContainer = function()
    {
        return $(this).each(function(){
            $("#cog_container").css("width", ($(window).width()) + "px");
        });
    }

    $.fn.cog_pageHeight = function()
    {
        // hpage = valeur
        // article = valeur - sigma(h(elt_fixes));
        var velt = 'article';
        var height_ = $.cog.height_;
        $('#cog_container').css('height', height_ + 'px');
        return $('#cog_container > .page').each(function(){
            var h_fixed_elts = 0;
            $(this).css('height', height_ + 'px');
            $(this).children().not('article').each(function(){
                h_fixed_elts += parseInt($(this).outerHeight(true));
            });
            $(this).find('article').first().css(
                'height', height_ - (h_fixed_elts) - 20 + 'px');
        });
    }

    $.fn.scrollPage = function()
    {
        //trace_page && console.log('scrollPage');
        //trace_page && console.log($('#cog_container > section.page').length);
        var pageWidth = $('#cog_container .active').outerWidth(true);
        var leftOffset = ($(window).width() - pageWidth)/2;
        $('#cog_container').animate({
            scrollLeft : (
                $('#cog_container > .page.active')
                    .prevAll('.page.inactive').length) *
                (pageWidth) - leftOffset + 'px'
        }, 'slow');
        return $(this);
    }

    $.fn.hasPage = function(page_ref)
    {
        //trace_page && console.log('hasPage: ' + page_ref);
        if(page_ref != undefined)
        {
            return $('#cog_container > .page#' + page_ref)
                .length > 0;
        }
        return false;
    }

    $.fn.getCogRefObj = function()
    {
        return $(this).find("header > .title > a").first().attr('page_ref');
    }

    function _cog_reloadAnonymousPage()
    {
        var active_page = $(".page.active");
        if(_cog_connected()) {
	    var is_anonymous = active_page.find(".anonymous").length;
	    if(is_anonymous){
		active_page.find(".anonymous").each(function(){
		    $(this).remove();
		});
		active_page.find("header > .title > a").first().click();
            }
        }
    }

    $.fn.referencePage = function(page_ref)
    {
        //trace_page && console.log('referencePage: ' + page_ref);
        $(this).attr('id', page_ref);
        var title = $(this).find("header > .title > a").first();
        if(title)
        {
            title.attr("target", '#' + page_ref);
        }
        return page_ref;
    }

    $.fn.inactivatePage = function()
    {
        return $(this).each(function(){
            //trace_page && console.log('inactivatePage: ' + $(this).attr('id'));
            $(this).removeClass('active')
                .removeClass('to_inactivate')
                .addClass('inactive')
                .attr('title', $(this).find('header > .title:first').text());
        });
    }

    $.fn.activatePage = function(page_ref)
    {
        if(! page_ref)
        {
            page_ref = $(this).getCogRefObj();
            $(this).referencePage(page_ref);
        }
        //trace_page && console.log('activatePage: ' + page_ref);
        $(this).removeClass('active');
        $('#cog_container > .page.active').addClass('to_inactivate');
        $('#' + page_ref).removeClass('inactive').addClass('active')
            .removeAttr('title')
            .children().show();
        $('.to_inactivate').inactivatePage();
        $('#cog_container > .page').loadedPagesMenu();
        $('#cog_container > .page.active').cog_resize();
        $.address.value(
            $('#cog_container > .page.active>header>.title a')
                .attr('href'));
	//XXX $.address.change ?
        _cog_reloadAnonymousPage();
        return $(this);
    }

    $.fn.deletePage = function()
    {
        //trace_page && console.log('deletePage');
        var previous_page = $(this).prev();
        $(this).remove();
        $(document).loadedPagesMenu();
        return previous_page;
    }

    $.fn.getActivePage = function()
    {
        return $('#cog_container > .page.active');
    }

    $.fn.loadedPagesMenu = function()
    {
        //trace_page && console.log('loadedPagesMenu');
        var links = $("#cog_container > .page > header > .title > a");
        $('#cog_ariadne_menu').empty();
        links.each(function(){
            //trace_page && console.log(' * ' + $(this).attr('page_ref'));
            $('#cog_ariadne_menu').append($(this).clone());
            $('#cog_ariadne_menu > a').wrap('<li class="ui-menu-item" />');
            $('#cog_ariadne_menu').menu();
        });
        var page_id = $('#cog_container > section.page.active').attr('id');
        $('#cog_ariadne_menu > li > a').each(function(){
            var page_ref = $(this).attr('target');
            if(page_ref)
            {
                page_ref = page_ref.substring(1);
                $(this).attr('page_ref', page_ref)
                    .removeAttr('target');
                if(page_ref == page_id)
                {
                    $(this).addClass('active');
                }
            }
        });
    }

    $.fn.updateMathGlyphs = function()
    {
        MathJax.Hub.Queue(["Typeset",MathJax.Hub]);
    }

    function __check_cookies()
    {
        try{
            var $S = window.localStorage;
            $('.no_cookies').addClass('hidden');
            $('.cookies').removeClass('cookies');
        }catch(err){
            console.log('need cookies');
        }
        return $S;
    }

    function trim()
    {
        return String(this).replace(/^\s*|\s*$/g, '');
    }

    function exists(elt)
    {
        return elt && elt.length > 0;
    }

    function random_id()
    {
        var rand1 = Math.ceil(Math.random() * 1000000);
        var rand2 = Math.ceil(Math.random() * 1000000);
        var rand_id = 'id_' + rand1 + '_' + rand2;
        return rand_id;
    }

    function _close(elt)
    {
        $($(elt).attr('target')).html("");
    }

    function _switch_loaded_link(elt)
    {
        var rand_id = random_id()
        var refresh_link = $(elt).clone();
        $(refresh_link)
            .addClass('button small left')
            .attr('target', '#' + rand_id)
            .html('<img class="icon" alt="reload" title="reload" ' +
                  'src="/collorg/images/refresh.svg" />').after('&nbsp;');
        $(elt).after(
            '<div id="' + rand_id + '" class="page">' + '</div>');
        $(elt).before($(refresh_link));
        var a_label = $(elt).html();
        $(elt).replaceWith(
            '<span class="link toggle_delt">' + a_label + '</span> '
        );
        return $('#' + rand_id)
    }

    function _get_target(elt)
    {
        /* returns the target referenced by the attr 'target'
         *
         * this_, after_, previous_, parent_
         * an explicit id: #something
         */
        var special_targets = [
            '_page_article_', '_page_', '_reset_', 'this_',
            '_after_', 'previous_', 'next_', 'parent_'];
        var target = $(elt).attr('target') || undefined;
        if(target && $.inArray(target, special_targets) == -1 &&
           target[0] != '#'){
            target = '#' + target;
            if($(target).length == 0){
                console.log("Wrong target " + target);
            }
        }
        switch(target) {
        case 'this_':
            return $(elt);
        case '_page_article_':
            return '#' + $(document).getActivePage()
                .find('article').first().attr('id');
        case '_reset_':
            $('#cog_container').empty();
            return undefined;
        case '_page_':
            return '#' + $(document).getActivePage().attr('id');
        case '_after_':
            // need a better random ID.
            return _switch_loaded_link($(elt));
        case 'previous_':
            return $(elt).prev().show();
        case 'next_':
            return $(elt).next().show();
        case 'parent_':
            return $(elt).parent();
        default:
            return $(target).show();
        }
    }

    $.fn.map_ = function(posted_data)
    {
        /* récup. les informations dans <div id="#cog_data">...</div>.
           (string representation of a json object).
        */
        return this.each(function() {
            var json_data = $.parseJSON(posted_data);
            try{
                var cog_data = $.parseJSON($("#cog_data").html());
            } catch(err) {
                console.log(err);
            }
            if($(this).attr('target')) {
                json_data.cog_target = $(this).attr('target');
            }
            $.data(document.body, 'cog_data', json_data);
            $.each(cog_data, function(key, val){
                json_data[key] = val;
            });
            var cog_environment = $("#cog_environment").html()
            if(cog_environment != '') {
                json_data.cog_environment = cog_environment;
            }
        });
    }

    $.fn.post_modal = function(key)
    {
        return this.each(function(){
            var cont = $(this).html();
            var dmodal = key == '#cog_dialog_modal';
            $(this).dialog({
                modal: dmodal, hide: 'slide',
                title: $(cont).attr('title'),
                width: $(cont).attr('width'),
            });
        });
    }

    function __check_page(elt)
    {
        return elt.hasClass('page')
    }

    function __preview_wiki(elt)
    {
        var target = $($(elt).attr('target'));
        if(elt.hasClass('ewiki')){
            elt.addClass('hidden').prev().removeClass('hidden');
            target.removeClass('hidden').parent().next().addClass('hidden');
        } else {
            elt.addClass('hidden').next().removeClass('hidden');
            target.addClass('hidden').next();
            node = target.parent().next();
            $(node).html('').removeClass('hidden');
            creole.parse(node['0'], target.val());
            $(node).updateMathGlyphs();
        }
    }

    $.fn.wrapPage = function(elt, page_ref)
    {
        //trace_page && console.log('wrapPage: page_ref: ' + page_ref);
        var new_page = $('#cog_new_page').clone()
            .removeAttr('id').html(elt)
            .addClass('page')
            .removeClass('hidden');
        page_ref = new_page.referencePage(page_ref);
        if($('#cog_container > .page').length > 0)
        {
            $("#cog_container > .page").last().after(new_page);
        } else {
            $("#cog_container").html(new_page);
        }
        $("#cog_container > .page").last().activatePage(page_ref);
    }

    $.fn.initPage = function()
    {
        $('#cog_container').html($().wrapPage($('#cog_container').html()));
    }

    $.fn.post_result = function(data)
    {
        return this.each(function() {
            var elt_target = _get_target(this);
            var dialog = false;
            $.each(data, function(key, val) {
                if(key.substr(0,11) == "#cog_dialog") {
                    dialog = true;
                }
                $('.cog_new_post_link').addClass('hidden');
                if(key[0]!=='#') {
                    key="#"+$(elt_target).attr("id");
                }
                if(key == '#cog_reload') {
                    $('body').data('cog_reload', '#cog_container');
                }
                if($(key).hasClass('reload')) {
                    $(key).replaceWith(val.content);
                } else {
                    if($(key).length != 0) {
                        if(key == '#cog_container') {
                            var page_ref = data['#page_ref']['content'];
                            if(page_ref) {
                                if($('#cog_container')
                                   .find('#' + page_ref).length) {
                                    $('#' + page_ref)
                                        .html(val.content)
                                        .activatePage();
                                } else {
                                    $('#cog_container').append(
                                        $().wrapPage(val.content, page_ref));
                                }
                            }
                        } else {
                            $(key).html(val.content);
                            $(key).find(':first-child')
                                .parent('#cog_container>.page.active')
                                .each( function() { $(this).activatePage(); } );
                        }
                    }
                }
                if(key.substr(0,11) == "#cog_dialog"
                   && trim($(key).html()) != '') {
                    dialog = true;
                    $(key).post_modal(key);
                }
            });
            if(!dialog) {
                try{$("#cog_dialog_modal").dialog('close');}catch(err){}
            }
        });
    }

    $.fn.post_upload_result = function(target)
    {
        $('#callback_' + target).click();
    }

    $.fn.attach_ = function(data_form_id)
    {
        var url = undefined;
        return this.each(function() {
            $.blockUI({ message:'',overlayCSS: { opacity: 0.1} });
            var form = $('#' + data_form_id);
            var uploader = $(form).attr('action');
            var target = $(form).find('input[name="cog_target"]').val();
            var formData = new FormData($(form)[0]);
            var data_ = $(':file');
            $.ajax({
                url: uploader,
                type: 'POST',
                data: formData,
                cache: false,
                contentType: false,
                processData: false,
                success: function(data)
                {
                    $(this).post_upload_result(target);
                }
            });
        });
    }

    $.fn.post_ = function()
    {
        return this.each(function(){
            var elt = this;
            var link = this;
            $('body').css('cursor', 'wait');
            $.blockUI({ message:'',overlayCSS: { opacity: 0.1} });
            var posted_data = $(this).attr('data-cog') || '{}';
            $(this).map_(posted_data);
            $.cog.data_href = $(this).attr('data-href');
            $.cog.href = $(this).attr('href');
            $.ajax({
                type:'POST',
                url:$.cog.data_href || $.cog.href,
                data:$.data(document.body, 'cog_data'),
                success:function(data){
                    if(data['#cog_container'] !== undefined)
                    {
                        $(elt).parents('.page').nextAll('.page').remove();
                    }
                    try{
                        $(elt).post_result(data);
                        $(elt).parents('.page').find('a')
                            .removeClass('clicked').end();
                        $(elt).addClass('clicked');
                        $(elt).liveCalendar();
                        svgFallback();
                        _cog_reloadAnonymousPage();
                    }catch(err){
                        console.log(err);
                    }
                },
                complete:function(){
		    $('#cog_container>section.page').first()
			.on('swipeleft', function(evt){
			    $(this).next().click();
			    evt.preventDefault();
			});
		    $('#cog_container>section.page.active')
			.on('swiperight', function(evt){
			    $(this).prev().click();
			    evt.preventDefault();
			}).on('swipeleft', function(evt){
			    $(this).next().click();
			    evt.preventDefault();
			});
                    var y = parseInt($(elt).attr('cog_position')) || 0;
                    $('this').post_item_links();
                    $('a:not([target])').attr('target', 'blank_');
                    if($('body').data('cog_reload') != ''){
                        $('.reload').each(function(){
                            $(this).trigger('click');
                        });
                        $('body').data('cog_reload', '');
                    }
                    $('body').data('cog_reload', '');
                    $('.datepicker').datepicker({
                        dateFormat: "yy-mm-dd",
                        appendText: "(yyyy-mm-dd)",
                        changeMonth: true,
                        changeYear: true,
                        showWeek: true
                    });

                    $('.timepicker').datetimepicker({
                        dateFormat: "yy-mm-dd",
                        changeMonth: true,
                        changeYear: true,
                        showWeek: true,
                        stepMinute: 15,
                        timeFormat: 'HH:mm:ss'
                    });

                    initDragEvents();
                    $(".tabs").tabs();
                    $('select[trigger]').on('change', function(){
                        $(this).find('option:selected[triggered]')
                            .each(function(){
                                $($(this).attr('triggered')).trigger('click');
                        });
                        $(this).prop('selectedIndex', 0);
                    });

                    try{
                        $(document).getActivePage().updateMathGlyphs();
                    }catch(err){
                        console.log(err);
                    }
                },
/*                error:function(xhr, status, error)
                {
                    console.log(error);
                },
*/
                dataType:'json'

                // end of ajax
            });
            $('body').css('cursor', 'auto');
        });
    }

    $.fn.serializeObject = function()
    {
        var o = {};
        var a = this.serializeArray();
        $.each(a, function() {
            if (o[this.name] !== undefined)
            {
                if (!o[this.name].push) {
                    o[this.name] = [o[this.name]];
                }
                o[this.name].push(this.value || '');
            }
            else
            {
                o[this.name] = this.value || '';
            }
        });
        return o;
    };

    $.fn.form_to_json = function()
    {
        var a_form = {};
        function isArray()
        {
            if (typeof arguments[0] == 'object') {
                var criterion = arguments[0]
                    .constructor.toString().match(/array/i);
                return (criterion != null);
            }
            return false;
        }
        $(this).find(':input').each(function(){
            var elt = this
            // .not(':checkbox') doesn't work
            if($(elt).attr('type') != 'checkbox' &&
               $(elt).attr('type') != 'radio'){
                var key = $(this).attr('name');
                var val = $(this).val();
                if(key != undefined){
                    a_form[key] = val;
                }
            }
        }).end().find(':checkbox:checked').each(function(){
            var key = $(this).attr( "name" );
            var val = $(this).val();
            if ( ! isArray( a_form[key] ) ) {
                a_form[key] = new Array;
            }
            a_form[key].push(val);
        });
        return $.toJSON(a_form);
    };

    $.fn.liveCalendar = function()
    {
        return this.each(function(){
            $(".calendar").each(function(){
                if($(this).html() != '')
                {
                    return;
                }
                var cog_oid = $(this).first().attr('id');
                $(this).fullCalendar({
                    events: '?cog_method=w3get_events&amp;' +
                        'cog_oid_=' + cog_oid + '&amp' +
                        'cog_ajax=true&cog_raw=true',
                    header: {
                        left: 'prev,next today',
                        center: 'title',
                        right: 'month,agendaWeek,agendaDay'
                    },
                    eventClick: function(calEvent,jsEvent,view){
                        var url_event = '?cog_oid_=' + calEvent.cog_oid +
                            '&amp;cog_method=w3display&amp;cog_ajax=true' +
                            '&amp;cog_target=event';
                        var result = $.getJSON(url_event, function(data) {
                            $("#cog_dialog_modal").html(data.event.content)
                                .post_modal();
                        });
                    },
                    defaultView: 'agendaWeek',
                    minTime: 7,
                    maxTime: 21,
                    firstDay: 1,
                });
            });
        });
    };

    $.fn.post_item_links = function()
    {
	$(".post_item").mousemove(function(event){
	    if($(".post_item:hover").length){
		if($.cog.pagex != event.pageX || $.cog.pagey != event.pageY){
		    $.cog.pagex = event.pageX;
		    $.cog.pagey = event.pageY;
		    $(this).siblings().removeClass('focus');
		    $(this).addClass('focus');
		}
	    }
	});
    };

    $.fn.getOidFromUrl = function()
    {
        return $.url($(this).attr('data-href')).param('cog_oid_');
    }

    $.fn.__make_draggable = function()
    {
        /**
         * is draggable each a.action having a cog_oid attribute and a
         * cog_method attribute with w3display value.
         */
        $(this).each(function(){
            var element = $(this);

            if($(this).hasClass('post_item'))
            {
                element = $(this).find('span.title > a');
                if(element.length == 0) { link = $(this).find('a'); }
            }

            element.addClass('af');
            var href = element.attr('href');
            var cog_oid = $.url(href).param('cog_oid_');
            var cog_method = $.url(href).param('cog_method');
            var text = $(this).text().replace('>', '&gt;').replace('<', '&lt;');

            if(cog_oid && cog_method == 'w3display')
            {
                var follow = element
                    .attr('href', href)
                    .attr('text', text)
                    .attr('cog_oid', cog_oid)
                    .addClass('follow icon');
            }
        });
    }

    function __follow(item)
    {

        var followed = $(item)
            .clone()
            .draggable({helper:'clone', iFrameFix: true})
            .addClass('action d_see_also')
                    .html(item.text());

            var del = $('<a></a>')
                .addClass('cart-remove-action')
                .attr('onclick','$(this).parent().remove();');

            var here = false;

            $("#cog_cart").find('li>a').each(function(){
                if($(this).attr('href') == followed.attr('href')){
                    here = true;
                }
            });
        followed.attr('target', '#cog_container');
            if(here){ return; }

            $('<li style="position:relative"></li>')
                .append(del).append(followed).appendTo("#cog_cart>ul");
    }

    $.fn.show_cart = function(){
	return this.each(function(){
	    $(this).addClass('extend');
	});
    }

    $.fn.hide_cart = function(){
	return this.each(function(){
	    $(this).removeClass('extend');
	});
    }

    /**
     * Initialize all the dom components
     * an droppable events.
     */
    function __init()
    {
        $('.no_javascript').addClass('hidden');
        $('.javascript').removeClass('javascript');
        $(document).wrapPage($("#cog_container").html());
        if(window.location.search)
        {
            $('#cog_home_link').hide();
        }
        __check_cookies();
        svgFallback();
        initDragEvents();

        $(".tabs").tabs();

        $( "#cog_cart ul" ).droppable({
            activeClass: "ui-state-default",
            hoverClass: "ui-state-hover",
            tolerance: "pointer",
            accept: ".action",
	    activate: function(event, ui)
	    {
                $('#cog_cart').show_cart();
	    },
            drop: function( event, ui )
            {
                __follow(ui.draggable);
		$("#cog_cart").hide_cart();
            },
	    deactivate: function(event, ui)
	    {
		$('#cog_cart').hide_cart();
	    }
        });
    }

    function initDragEvents()
    {
        $('.action').draggable({
	    distance:15,
	    helper:"clone",
	    zIndex:30
        });
        $('.wiki > textarea').droppable({
               activeClass: "ui-state-default",
               hoverClass: "ui-state-hover",
               tolerance: "touch",
               accept: ".d_see_also",
               drop: function(event, ui)
               {
                   __addRefToWiki(event,ui.draggable);
               }
        });
    }

    function _cog_connected()
    {
        var session = $.cookie('cog_session');
        if(session === undefined || session == null){
            return false;
        }
        return true;
    }

    /**
     * will check if the user have a session cookie
     * and in this case, will try to log-in the
     * user.
     */
    function _try_to_log_user()
    {
        if($.cookie)
        {
            var session = $.cookie('cog_session');
            if(session === undefined || session == null)
                return false;
            else {
                var link = $( '<a class="action hidden" ' +
                              'href="?cog_method=w3session_login' +
                              '&cog_fqtn_=collorg.actor.user"></a>' );
                link.post_(true);
                return false;
            }
        }
        else
        {
            return false;
        }
    }

    function __addRefToWiki(event, item)
    {
        try{
            item = $(item.get(0));
            var area = $(event.target).get(0);
            var text = '[['
                + (item.attr('href') || item.attr('data-href')) + '|' +
                item.text() + ']]';
	    var scrollPos = area.scrollTop;
	    var strPos = 0;
	    var br = ((area.selectionStart||area.selectionStart=='0')?"ff": (
		document.selection ? "ie" : false ) );
	    if (br == "ie") {
		area.focus();
		var range = document.selection.createRange();alert(area);
		range.moveStart ('character', -(area.value.length));
		strPos = range.text.length;
	    } else if (br == "ff")
		strPos = area.selectionStart;
	    var front = (area.value).substring(0, strPos);  
	    var back = (area.value).substring(strPos, area.value.length); 
	    area.value=front+text+back;
	    strPos = strPos + text.length;
	    if (br == "ie") { 
		area.focus();
		var range = document.selection.createRange();
		range.moveStart ('character', -(area.value.length));
		range.moveStart ('character', strPos);
		range.moveEnd ('character', 0);
		range.select();
	    } else if (br == "ff") {
		area.selectionStart = strPos;
		area.selectionEnd = strPos;
		area.focus();
	    }
	    area.scrollTop = scrollPos;

        } catch(err) {
            var val = $(target).val();
            var begin = val.substring(0, target.selectionStart);
            var end = val.substring(target.selectionEnd, val.length);
            var newText = begin + toInsert + end;
            $(target).text(newText);
        }
    }

    /**
     * Manages the display of svg items and it's fallbacks if
     * the current browser do not support them.
     */
    function svgFallback()
    {
        /**
         * @return True if the current browser supports svg
         */
        // We add a [no-svg] class to the document
        // and we replace all svg items in <img> tags
        // with a png.
        if(navigator.userAgent.search("MSIE") == -1){
            return;
        }
        document.documentElement.className += ' no-svg';
        var imgs = document.getElementsByTagName('img');
        var dotSVG = /.*\.svg$/;
        for (var i = 0; i != imgs.length; ++i) {
            if (imgs[i].src.match(dotSVG)) {
                imgs[i].src = imgs[i].src.slice(0, -3) + 'png';
            }
        }
    }

    $.fn.cog_navigate = function(){
        $(document).on('keydown', function(evt) {
            var post_item;
            if($(evt.target).is(':input')){
                var target = $(evt.target);
                return;
            }
            var active_page = $('#cog_container > section.page.active');
            var article = active_page.find('article').first();
            if(evt.which == $.ui.keyCode.LEFT){
                var prev = active_page.prev();
                prev && prev.children().click();
                evt.preventDefault();
            } else if(evt.which == $.ui.keyCode.RIGHT){
                var next = active_page.next();
                if(next.length){
                    next.children().click();
                } else {
                    var post_item = active_page.find('.post_item.focus');
                    if (post_item.length) {
                        post_item.first('a').click();
                    }
                }
                evt.preventDefault();
            } else if(evt.which == $.ui.keyCode.DOWN){
                var post_item = article.find('.post_item');
                if (post_item.length) {
                    var focused = article.find('.post_item.focus');
                    if(focused.length) {
                        var next = focused.next('.post_item');
                        if(next.length){
                            focused.removeClass('focus').next()
                                .addClass('focus');
                        }
                    } else {
                        post_item.first().addClass('focus');
                    }
                }
                evt.preventDefault();
            } else if(evt.which == $.ui.keyCode.UP){
                var post_item = article.find('.post_item');
                if (post_item.length) {
                    var focused = article.find('.post_item.focus');
                    if(focused.length) {
                        var previous = focused.prev('.post_item');
                        if(previous.length){
                            focused.removeClass('focus').prev()
                                .addClass('focus');
                        }
                    } else {
                        post_item.first().addClass('focus').scroll();
                    }
                }
                evt.preventDefault();
            } else if(evt.which == $.ui.keyCode.ENTER){
                var post_item = active_page.find('.post_item.focus');
                if (post_item.length) {
                    post_item.first('a').click();
                    evt.preventDefault();
                } else {
                    $(this).click();
                }
            }
            var post_item = active_page.find('.post_item.focus');
            if(post_item.length){
                var pt = post_item.position().top;
                var ph = post_item.innerHeight();
                var milieu = article.position().top + article.innerHeight()/2;
                var pim = pt + ph/2;
                var delta = pim - milieu;
                article.scrollTop(article.scrollTop() + delta);
            }
        });
    }

    /**
     * Main function
     */
    $.fn.collorg = function()
    {
        __init();
        $(document).cog_navigate();
        $('body').data('cog_reload', '');
        $('body').post_item_links();
        $.data(document.body, 'cog_data_form', {ajax:true});

        $('.toggle').click(function(){
            var to_toggle = $(this).attr('to_toggle');
            var elt = $($(this).attr('to_toggle')) || $(this);
            elt.toggle('slow', function(){
                $(this).cog_resize();
            });
        });

        $(document).on('click',function(evt){

            $('#cog_ariadne_menu').hide();
            var target = $(evt.target)
            if(target.hasClass('ewiki') || target.hasClass('vwiki')){
                __preview_wiki(target);
                return false;
            }
            if(target.is(".page.inactive") ||
	       target.parents('.page.inactive').length){
                elt = target.is(".page.inactive") &&
		    target || target.parents(".page.inactive").first();
                var page_ref = elt.attr('id');
                elt.activatePage(page_ref);
                return false;
            } else if(target.is('#cog_ariadne_menu a')) {
                var page_ref = target.attr('page_ref');
                $('#' + page_ref).activatePage(page_ref);
                return false;
            } else if(
                target.hasClass('action') || target.parent().is('a.action')) {
                if(!target.hasClass('action')) {
                    target = target.parent();
                }
                evt.preventDefault();
                var elt = target;

                if(target.attr('trigger')) {
                    elt = $(target.attr('trigger')).trigger('click');
                    return false;
                }

                if($(elt).attr('data-form-id'))        {
                    var data_form_id = $(elt).attr('data-form-id');
                    var form = $('#'+data_form_id);
                    $(elt).attr('data-cog', $(form).form_to_json());
                    $(elt).post_();
                    return false;
                } else {
                    if(exists($(elt).attr('target'))
                       && $(elt).attr('target') != 'blank_'
                       && $(elt).is('a')) {
                        if($(elt).parent().hasClass("post_item")){
			    var post_item = $(elt).parent();
			    post_item.siblings('.clicked').removeClass('clicked');
			    post_item.addClass('clicked');
                            evt.stopImmediatePropagation();
                        }
                        if($(elt).hasClass('close')) {
                            _close($(elt));
                            evt.preventDefault();
                        } else {
			    if($(elt).parents('.post_item').length > 0) {
				var post_item = $(elt).parents(
				    '.post_item:first');
				post_item.siblings('.clicked').removeClass(
				    'clicked');
				post_item.addClass('clicked');
			    }
                            $(elt).post_();
                            return false;
                        }
                        evt.preventDefault();
                    } else if($(elt).is('a')) {
                        // no ajax if target does not exist or if it is 'blank_'
                        $(elt).attr('target', 'blank_');
                    }
                }
            } else if(target.hasClass('attachment')) {
                var data_form_id = target.attr('data-form-id');
                target.attach_(data_form_id);
                return false;
            } else if(target.hasClass('post_item')) {
		target.siblings('.clicked').removeClass('clicked');
		target.addClass('clicked');
                if (target.is('a')) return; //stop bubbling
                evt.preventDefault();
                target.siblings('.focus').removeClass('focus');
                target.addClass('focus').find('a:first').trigger('click');
                return false;
            } else if(target.parents('.post_item').length > 0) {
                var post_item = target.parents('.post_item:first');
		post_item.siblings('.clicked').removeClass('clicked');
		post_item.addClass('clicked');
                if (target.is('a')) return; //stop bubbling
                evt.preventDefault();
                post_item.siblings('.focus').removeClass('focus');
                post_item.addClass('focus').find('a:first').trigger('click');
                return false;
            } 
        });

        $(document).ajaxStop(ajax_stop);
        $(window).resize($(window).cog_resize);
        _try_to_log_user();

    };
})(jQuery)
