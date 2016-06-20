module.exports = function(grunt) {

  // Project configuration.
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    coffee: {
      compile: {
        options: {
          sourceMap: true,
          sourceMapDir: "../static/frontend/js/maps"
        },
        expand: true,
        flatten: true,
        cwd: 'src/',
        src: ['*.coffee'],
        dest: '../static/frontend/js/app',
        ext: '.js'
      }
    },
    watch: {
      scripts: {
        files: ['**/*.coffee'],
        tasks: ['coffee:compile'],
        options: {
          spawn: false,
        },
      },
    }
  });

  grunt.loadNpmTasks('grunt-contrib-coffee');
  grunt.loadNpmTasks('grunt-contrib-watch');

  grunt.registerTask('default', ['coffee:compile']);

};
