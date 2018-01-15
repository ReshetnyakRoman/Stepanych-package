// gulpfile with included stylus/autoupdate/sourcemap/nib. 

// include the required packages. 
var gulp = require('gulp');
var stylus = require('gulp-stylus');
var sourcemaps = require('gulp-sourcemaps');
var nib = require('nib');
var rupture = require('rupture');
var livereload = require('gulp-livereload');
var uglify = require('gulp-uglify');
var plumber = require('gulp-plumber');
var imagemin = require('gulp-imagemin');


function errorLog(error) {
	console.error.bind(error);
	this.emit('end');
}

// by command 'gulp' run all task in one shot

gulp.task('default',['scripts','styles','watch']);

// task for stylus compilation with nib library sorucemap and starting livereload plagins

gulp.task('styles', function () {
  	gulp.src('stylus/*.styl')
  		.pipe(plumber())
	  	.pipe(sourcemaps.init())
	    .pipe(stylus({use:[nib(), rupture()]}))	
	    .pipe(sourcemaps.write())
	    .pipe(gulp.dest('css'))
	    .pipe(livereload());
});


gulp.task('livereload', function(){
	gulp.src('*.html')
	gulp.src('*.py')
	gulp.src('html/*.html')
	gulp.src('stylus/*.styl')
		.pipe(livereload());
});

// javaScript simplification
gulp.task('scripts', function(){
	gulp.src('js/*.js')
		
		.pipe(uglify())
		.pipe(gulp.dest('static/js'));
})

// Image Task
// Compress 

gulp.task('image', function(){
	gulp.src('img/*')
		.pipe(imagemin())
		.pipe(gulp.dest('img/'))

});

// watch task for livereload and stylus compilations

gulp.task('watch', function () {
	gulp.watch('stylus/*.styl',['styles'])
	gulp.watch('js/*.js',['scripts'])
	gulp.watch('*.html',['livereload'])
	gulp.watch('html/*.html',['livereload'])
	gulp.watch('*.py',['livereload'])
	var server = livereload();
});

