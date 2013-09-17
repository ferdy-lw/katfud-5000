Model = require('./model')

KatFud = Model.extend(

  defaults:
    currentTime: "Unknown"
    firstFeed: "Unknown"
    nextRun: "Unknown"
    numberFeeds: 0
    lastRan: "Never"
    started: "Unknown"
    periodSec: 43200
    periodScale: 3600

  id: 'katfud'
  urlRoot: '/v1'

  runNow: ->
    @_doCmd("run_now")

  reboot: ->
    @_doCmd("reboot")

  shutdown: ->
    @_doCmd("shutdown")

  _doCmd: (cmd) ->
    $.ajax(
      url: @.url()+"/"+cmd+"?code="+$('#code').val()
      type: 'POST',
    ).always( (data, status) ->
      if data && data.status
        alert(cmd+" status: "+data.status)
      else
        alert(cmd+" status: "+status)
    )    
)

module.exports = new KatFud
