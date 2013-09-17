var View = require('./view').View;
var template = require('./templates/home-layout');

module.exports = View.extend({
  template: template,
  id: 'layout',

  initialize: function() {
    this.on('route', function(route) {
      this.renderContent(route);
    }, this);

  },
  renderContent: function(ContentView) {
    ContentView = ContentView || require('./katfud/index');
    var content = new ContentView();
    this.setView('#content', content).render();
  }
});
