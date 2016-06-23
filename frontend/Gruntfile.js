module.exports = function(grunt) {

  // Project configuration.
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    coffee: {
      app: {
        options: {
          join: true,
          sourceMap: true,
          sourceMapDir: "../static/frontend/js/"
        },
        files: {
          '../static/frontend/js/app.js': [
            'src/__lib__.coffee',
            'src/filtered-collection.coffee',
            'src/blueprint-model.coffee',
            'src/material-model.coffee',
            'src/blueprints-filter.coffee',
            'src/materials-filter.coffee',
            'src/blueprint-collection.coffee',
            'src/blueprint-view.coffee',
            'src/material-collection.coffee',
            'src/material-view.coffee',
            'src/pager.coffee',
            'src/blueprints-collection-view.coffee',
            'src/materials-collection-view.coffee',
            'src/inventory.coffee',
            'src/tracking.coffee',
            'src/track-tab-view.coffee',
            'src/resource-tabs.coffee',
            'src/app-view.coffee',
            'src/__init__.coffee'
          ]
        }
      }
    },
    watch: {
      scripts: {
        files: ['Gruntfile.js', '**/*.coffee'],
        tasks: ['default'],
        options: {
          spawn: false,
        },
      },
    }
  });

  grunt.loadNpmTasks('grunt-contrib-coffee');
  grunt.loadNpmTasks('grunt-contrib-watch');

  grunt.registerTask('default', ['coffee:app']);

};
