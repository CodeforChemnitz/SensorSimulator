module.exports = function(grunt) {
    grunt.initConfig({
        htmlmin: {
            dist: {
                options: {
                    removeComments: true,
                    collapseWhitespace: true
                },
                files: {
                    'static/index.html': 'src/html/setup.html'

                }
            }
        },
        jshint: {
            files: ['Gruntfile.js'],
            options: {
                globals: {
                    jQuery: true
                }
            }
        },
        pkg: grunt.file.readJSON('package.json'),
        uglify: {
            options: {
                mangleProperties: true,
                reserveDOMCache: true
            },
            build: {
                files: {
                    'static/output.min.js': [
                        'src/js/dom_selector.js',
                        'src/js/template.js',
                        'src/js/xhr.js',
                        'src/js/main.js'
                    ]
                }
            }
        },
        watch: {
            html: {
                files: [
                    'src/html/setup.html'
                ],
                tasks: ['htmlmin']
            },
            js: {
                files: [
                    '<%= jshint.files %>',
                    'src/js/*.js'
                ],
                tasks: ['jshint', 'uglify']
            }
        }
        
        
    });

    grunt.loadNpmTasks('grunt-contrib-htmlmin');
    grunt.loadNpmTasks('grunt-contrib-jshint');
    grunt.loadNpmTasks('grunt-contrib-uglify');
    grunt.loadNpmTasks('grunt-contrib-watch');

    grunt.registerTask('default', ['jshint', 'uglify']);
};
