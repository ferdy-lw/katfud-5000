View = require('../view').View
template = require('./templates/index')
katFud = require('models/katfud')

timeConvert = (time) ->
  _.isNumber(time) && new Date(time*1e3) || time 

datepickerConvert = (time) ->
  if _.isNumber(time)
    date = new Date(time*1e3)
    $.datepicker.formatDate("mm/dd/yy ", date)+date.getHours()+":"+date.getMinutes()
  else
    time

Backbone.Stickit.addHandler(
  selector: 'input[data-datetimepicker]'
  initialize: ($el, model, options) ->
    $el.datetimepicker(
      parse: 'loose'
      hourGrid: 4
      minuteGrid: 10
      addSliderAccess: true
      sliderAccessArgs: 
        touchonly: false
    ) 
)

module.exports = View.extend(
  template: template

  bindings:
    '#fud-url':
      observe : 'fudUrl'
      update: ($el, val) ->
        $el.text(val)
        $el.attr("href",val)

    '#currentTime': 
      observe: 'currentTime'
      onGet: timeConvert

    '#nextRun':
      observe: 'nextRun'
      onGet: timeConvert
      afterUpdate: ($el) ->
        $el.fadeOut(500, ->
          $(this).fadeIn(500)
        )

    '#lastRan':       
      observe: 'lastRan'
      onGet: timeConvert

    '#started':
      observe: 'started'
      onGet: timeConvert

    '#numberFeeds': 'numberFeeds'

    '#firstFeed': 
      observe: 'firstFeed'
      updateModel: false
      onGet: datepickerConvert

    '#period':
      observe: 'periodSec'
      updateModel: false
      onGet: (periodSec) ->
        periodSec/@model.get('periodScale')

    '#periodScale':
      observe: 'periodScale'
      updateModel: false
      selectOptions:
        collection: ->
          [{value: 3600, label: "Hour"}, {value: 60, label: "Min"}, {value: 1, label: "Sec"}]

  initialize: ->
    @model = katFud

    @_updateModel()

    window.setInterval( =>
      @_updateModel()
    , 60000)
  
  afterRender: ->
    @stickit()

  events: 
    'click [data-run]': 'runNow'
    'click [data-reboot]': 'reboot'
    'click [data-shutdown]': 'shutdown'
    'click [data-settings]': 'settings'
    'click [data-cancel-settings]': (event) ->
      event.preventDefault()
      @updateSettings(true)

  runNow: ->
    ret = @model.runNow().always( =>
      @_updateModel()
    )
    ret

  reboot: ->
    @model.reboot()

  shutdown: ->
    @model.shutdown()

  settings: (event) ->
    event.preventDefault()
    firstFeed = @.$('#firstFeed').val()
    period = @.$('#period').val()
    periodScale = Number(@.$('#periodScale option:selected').val())

    if _.isEmpty(firstFeed)
      return alert("You must enter a date for the first feed")

    if _.isEmpty(period)
      return alert("You must enter a period time")

    firstFeed = new Date(firstFeed)
    if firstFeed < new Date()
      return alert("You must enter a date after today")

    @model.save(
      firstFeed: firstFeed.getTime()/1e3
      periodSec: period*periodScale
      periodScale: periodScale
      code: $('#code').val()
    ,
      success: =>
        @_updateModel()
        alert("Saved settings")
      error: (model, xhr) -> 
        alert("Failed to save! "+xhr.statusText)
    )
  
  updateSettings: (force) ->
      # Should really just update the model and the view should change?
      @.$('#firstFeed').val(datepickerConvert(@model.get('firstFeed'))) if force or _.isEmpty(@.$('#firstFeed').val())
      @.$('#period').val(@model.get('periodSec')/@model.get('periodScale')) if force or _.isEmpty(@.$('#period').val())
      @.$('#periodScale').val(@model.get('periodScale')) # This ALWAYS overwrites the scale!
    
  _updateModel: ->
    @model.fetch().
      done( => 
        @updateSettings()
      )

)
