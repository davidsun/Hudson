###
add tips when user input '@'
Usage: $('input').atTips()
###

(->
  class AtTips
    constructor: (@el, @options={})->
      defaults =
        debounce: 150
        api: '/users/contact/%s'
        items: 8
        menu: '<ul class="typeahead dropdown-menu"></ul>'
        item: '<li><a href="#"></a></li>'
        minLength: 0
        wrapper: '<div class="at-tips-wrapper"></div>'

      @options = $.extend({}, defaults, @options)

      @$el = $(el)
      
      @matcher = @options.matcher or @matcher
      @sorter = @options.sorter or @sorter
      @highlighter = @options.highlighter or @highlighter
      @updater = @options.updater or @updater

      @$menu = $(@options.menu).appendTo('body')
      @$wrapper = $(@options.wrapper).appendTo('body')
      #.css(
      #    position: 'absolute'
      #    overflow: 'hidden'
      #    'z-index': -9999
      #    left: @$el.offset().left
      #    top: @$el.offset().top
      #    height: @$el.outerHeight()
      #    width: @$el.outerWidth()
      #    'line-height': @$el.css('line-height')
      #    'padding': @$el.css('padding')
      #    'font-size': @$el.css('font-size')
      #  )
      @shown = false
      @listen()

    source: (query, callback)=>
      url = @options.api.replace('%s', encodeURIComponent(query))
      $.getJSON(url, (data)=>
        callback(data.contacts)
      )

    listen: ->
      @$el.on('blur', $.proxy(@onBlur, @))
          .on('keypress', $.proxy(@onKeypress, @))
          .on('keyup', $.proxy(@onKeyup, @))
      if $.browser.chrome or $.browser.webkit or $.browser.msie
        @$el.on('keydown', $.proxy(@onKeydown, @))

      @$menu.on('click', $.proxy(@onClick, @))
            .on('mouseenter', 'li', $.proxy(@onMouseenter, @))

     getCursor: ->
      rangeData =
        start: 0
        end: 0
        text: ""   
      if typeof(@el.selectionStart) == "number" #W3C
        rangeData.start = @el.selectionStart
        rangeData.end = @el.selectionEnd
        rangeData.text = @el.value.substring(0, @el.selectionStart)
      else if document.selection #IE
        # TODO: support IE
        $.noop()
      rangeData

    onBlur: =>
      setTimeout(=>
        @hide()
      , 150)

    onKeydown: (e)=>
      @suppressKeyPressRepeat = !~$.inArray(e.keyCode, [40,38,9,13,27])
      @move(e)

    onKeypress: (e)=>
      if @suppressKeyPressRepeat then return
      @move(e)
    
    onKeyup: (e)=>
      switch e.keyCode
        when 40, 38 # down, up
          break
        when 9, 13 # tab, enter
          if not @shown then return
          @select()
        when 27, 32 # escape
          if not @shown then return
          @hide()
        else
          # TODO: use debounce event
          @lookup()
      e.stopPropagation()
      e.preventDefault()

    onClick: (e)=>
      e.stopPropagation()
      e.preventDefault()
      @select()

    onMouseenter: (e)=>
      @$menu.find('.active').removeClass('active')
      $(e.currentTarget).addClass('active')

    show: =>
      @$wrapper.css(
        position: 'absolute'
        overflow: 'hidden'
        'z-index': -9999
        left: @$el.offset().left
        top: @$el.offset().top
        height: @$el.outerHeight()
        width: @$el.outerWidth()
        'line-height': @$el.css('line-height')
        'padding': @$el.css('padding')
        'font-size': @$el.css('font-size')
      )
      pos = $.extend({}, $('cite', @$wrapper).offset(), {
        height: parseFloat(@$wrapper.css('line-height').replace('px', ''))
      })

      @$menu.css(
        top: pos.top + pos.height
        left: pos.left
      )

      @$menu.show()
      @shown = true
      @

    hide: =>
      @$menu.hide()
      @$wrapper.html('')
      @shown = false
      @

    lookup: =>
      @cursor = @getCursor().start
      text = @$el.val()
      @at = text.lastIndexOf('@', @cursor)
      if @at == -1 then return @
      @query = text.substring(@at + 1, @cursor)
      if @query.indexOf(' ') != -1 then return @
      tmp = (text.substring(0, @at) + text.substring(@at).replace('@', '<cite>@</cite>')).replace('\n', '<br/>')
      @$wrapper.html(tmp)
      if @options.minLength > 0 and (not @query or @query.length < @options.minLength)
        return if @shown then @hide() else @
      items = if $.isFunction(@source) then @source(@query, $.proxy(@process, @)) else @source
      return if items then @process(items) else @

    select: =>
      # TODO: use @
      val = @$menu.find('.active').attr('data-value')
      @$el.val(@updater(val)).change()
      return @hide()

    updater: (item)=>
      text = @$el.val()
      text.substring(0, @at) + "@#{item} " + text.substring(@cursor)

    process: (items)=>
      items = $.grep(items, (item)=>
        @matcher(item)
      )
      items = @sorter(items)

      if items.length == 0
        return if @shown then @hide() else @
      return @render(items[0..@options.items]).show()

    matcher: (item)=>
      ~item.toLowerCase().indexOf(@query.toLowerCase())

    sorter: (items)=>
      beginswith = []
      caseSensitive = []
      caseInsensitive = []
      while item = items.shift()
        if item.toLowerCase().indexOf(this.query.toLowerCase()) == 0 then beginswith.push(item)
        else if ~item.indexOf(this.query) then caseSensitive.push(item)
        else caseInsensitive.push(item)
      beginswith.concat(caseSensitive, caseInsensitive)

    highlighter: (item)=>
      query = @query.replace(/[\-\[\]{}()*+?.,\\\^$|#\s]/g, '\\$&')
      return item.replace(new RegExp('(' + query + ')', 'ig'), ($1, match)=>
        return "<strong>#{match}</strong>"
      )

    render: (items)=>
      items = $(items).map((i, item)=>
        i = $(@options.item).attr('data-value', item)
        i.find('a').html(@highlighter(item))
        i[0]
      )

      items.first().addClass('active')
      @$menu.html(items)
      @

    next: =>
      active = @$menu.find('.active').removeClass('active')
      next = active.next()
      if not next.length then next = $(@$menu.find('li')[0])
      next.addClass('active')
      
    prev: =>
      active = @$menu.find('.active').removeClass('active')
      prev = active.prev()
      if (not prev.length) then prev = @$menu.find('li').last()
      prev.addClass('active')

    move: (e)=>
      if not @shown then return
      switch e.keyCode
        when 9, 13, 27 # tab, enter, escape
          e.preventDefault()
        when 38 # up
          e.preventDefault()
          @prev()
        when 40 # down
          e.preventDefault()
          @next()
      e.stopPropagation()


  $ = window.jQuery
  $.fn.atTips = (option)->
    @each(->
      $this = $(@)
      data = $this.data('atTips')
      options = typeof option == 'object' && option
      if not data then $this.data('atTips', (data = new AtTips(@, options)))
      if typeof option == 'string' then data[option]()
    )
  $.fn.atTips.Constructor = AtTips
)()