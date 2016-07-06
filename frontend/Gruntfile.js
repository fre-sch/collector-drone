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
        dest: 'build/coffee_js',
        ext: '.js'
      }
    },
    shell: {
        compile_index: {
            command: "cd ..; ./env/bin/python collectordrone/render.py frontend/src/html index.html frontend/build/dist/index.html"
        }
    },
    browserify: {
      dist: {
        src: 'build/coffee_js/App.js',
        dest: 'build/dist/js/dist/app.js'
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
            src: ["./**"],
            dest: "../static/"
        }
    },
    watch: {
      scripts: {
        files: [
            'Gruntfile.js',
            'static/css/drone.css',
            'static/css/theme.css',
            'src/**/*.coffee',
            'src/html/*.html'
        ],
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
  grunt.loadNpmTasks('grunt-shell');

  grunt.registerTask('default', [
      'coffee:compile',
      'browserify:dist',
      "shell:compile_index",
      "copy:static",
      "copy:dist"
  ]);

};
