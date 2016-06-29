module.exports = function(grunt) {

  // Project configuration.
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    coffee: {
      compile: {
        options: {
          bare: true
        },
        expand: true,
        flatten: true,
        src: ['src/**/*.coffee'],
        dest: 'build/',
        ext: '.js'
      }
    },
    browserify: {
      dist: {
        src: 'build/App.js',
        dest: 'build/dist/app.js'
      }
    },
    copy: {
        static: {
            expand: true,
            src: ["static/**"],
            dest: "../"
        },
        dist: {
            expand: true,
            cwd: "build/dist/",
            src: ["app.js"],
            dest: "../static/js/dist/"
        }
    },
    watch: {
      scripts: {
        files: ['Gruntfile.js', 'src/**/*.coffee'],
        tasks: ['default'],
        options: {
          spawn: false,
        },
      },
    }
  });

  grunt.loadNpmTasks('grunt-contrib-coffee');
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-contrib-copy');
  grunt.loadNpmTasks('grunt-browserify');

  grunt.registerTask('default', [
      'coffee:compile',
      'browserify:dist',
      "copy:static",
      "copy:dist"
  ]);

};
