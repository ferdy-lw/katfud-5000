exports.config =
  # See docs at http://brunch.readthedocs.org/en/latest/config.html.

  # Application build path.  Default is public/
  # paths:
  #   public: ''
  paths:
    public: '../KatFud/katfud/static'

  files:
    javascripts:
      joinTo:
        'scripts/app.js': /^app/
        'scripts/vendor.js': /^vendor/
        'test/scripts/test.js': /^test(\/|\\)(?!vendor)/
        'test/scripts/vendor.js': /^test(\/|\\)(?=vendor)/
      order:
        before: [
          'vendor/scripts/console-helper.js',
          'vendor/scripts/jquery-1.9.1.js',
          'vendor/scripts/jquery-ui-1.10.3.custom.js',
          'vendor/scripts/jquery-ui-sliderAccess.js',
          'vendor/scripts/jquery-ui-timepicker-addon.js',
          'vendor/scripts/lodash.underscore-1.0.1.js',
          'vendor/scripts/backbone-1.0.0.js',
          'vendor/scripts/backbone.layoutmanager-0.8.7.js',
          'vendor/scripts/backbone.stickit-0.6.3.js',
          'vendor/scripts/foundation.js',
          'vendor/scripts/handlebars-1.0.0.js'
        ]
    stylesheets:
      joinTo:
        'styles/app.css': /^(app|vendor)/,
        'test/styles/test.css': /^test/
      order:
        before: [
          'app/views/styles/index.scss'
        ]
        # after: ['vendor/styles/helpers.css']
    templates:
      joinTo: 'scripts/app.js'

  stylus: # https://github.com/brunch/stylus-brunch#spriting
    spriting: no,
    iconPath: 'app/assets/images'
  minify: no
  modules:
    addSourceURLs: true
  # # Redo wrapper so that tests modules are automatically added.
  # modules:
  #   wrapper: (path, data, isVendor) ->
  #     if isVendor
  #       code = "#{data};\n"
  #     else
  #       path = path.replace(/\.\w+$/, '').replace(/^app\//, '')
  #       code = """
  #       window.require.define({#{JSON.stringify path}: function(exports, require, module) {
  #         #{data.replace /(\\)?\n(?!\n)/g, ($0, $1) -> if $1 then $0 else '\n  '}
  #       }});\n\n
  #       """
  #       if /^test[\\/]/.test path
  #         code += "window.require(#{JSON.stringify path});\n\n"
  #     code
