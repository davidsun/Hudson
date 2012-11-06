###
$.debounce allows you to easily debounce event callbacks.
$.debounce(fn, timeout, [invokeAsap], [ctx]);
###

(->
  $ = window.jQuery
  $.extend(
    debounce: (fn, timeout, invokeAsap, ctx)->
      if arguments.length == 3 and typeof invokeAsap != 'boolean'
        ctx = invokeAsap
        invokeAsap = false
      timer = null
      return =>
        args = arguments
        ctx = ctx or this
        invokeAsap and !timer && fn.apply(ctx, args)
        clearTimeout(timer)
        timer = setTimeout(=>
          invokeAsap or fn.apply(ctx, args)
          timer = null
        , timeout)
  )
)()
