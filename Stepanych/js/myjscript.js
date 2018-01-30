 

// Add smooth scrolling to all links in navbar + footer link
	$(document).ready(function(){
	  $().on('click', function(event) {
	    // Make sure this.hash has a value before overriding default behavior
	    if (this.hash !== "") {
	      // Prevent default anchor click behavior
	      event.preventDefault();

	      // Store hash
	      var hash = this.hash;

	      // Using jQuery's animate() method to add smooth page scroll
	      // The optional number (900) specifies the number of milliseconds it takes to scroll to the specified area
	      $('html, body').animate({
	        scrollTop: $(hash).offset().top
	      }, 900, function(){
	   
	        // Add hash (#) to URL when done scrolling (default click behavior)
	        window.location.hash = hash;
	      });
	    } // End if

	  });
	  
	 $(window).scroll(function() {
	    $(".slideanim").each(function(){
	      var pos = $(this).offset().top;

	      var winTop = $(window).scrollTop();
	        if (pos < winTop + 600) {
	          $(this).addClass("slide");
	        }
	    });
	 });
	  
	  /* Disabling fist options in Drop-down form inputs*/
	  var s, options;
	  options = $(".disable-option")
	  for (s=0; s<options.length; s++){
	  options.eq(s).children().first().attr("disabled","disabled");
		}

	/* loader function */
	/*$('.button-upload').on("click", function (event) {

		$('#loader_section').show();
		$('main').addClass('blur');
		$('aside').addClass('blur');
	    $('header').addClass('blur');
	    $('footer').addClass('blur');
	    
	});*/

	$('.button-upload').on("click", function (event) {
		
		event.preventDefault();
		event.stopPropagation();
		$('#loader_section').show();
		$('main').addClass('blur');
		$('aside').addClass('blur');
	    $('header').addClass('blur');
	    $('footer').addClass('blur');
	    _this = $(this)[0]
	    href = $(this).attr('href');
	    this2 = $(this)
	    if (_this.tagName == 'A') {
	    	setTimeout(function() { location.href = href; }, 10);
	  		}
	  	else {
	  		
	  		//alert($(this).parents("form:first")[0].id)
	  		setTimeout(function() { this2.parents("form").submit(); }, 10);
	  	}

	});

	/*var classname = document.getElementsByClassName("button-upload");

	for (var i = 0; i < classname.length; i++) {
    classname[i].addEventListener('click', loader, false);
	}*/
   	
   	function loader() {
   		
	    $('#loader_section').show()
	    $('main').addClass('blur');
		$('aside').addClass('blur');
	    $('header').addClass('blur');
	    $('footer').addClass('blur');
	    
	};
	
	$('#pic-upload').click(function() {
	    $('#loader_section').show();
	    $('main').addClass('blur');
	    $('aside').addClass('blur');
	    $('header').addClass('blur');
	    $('footer').addClass('blur');
	});	

	$("#loader_section").on("ajaxSend", function() {
	        $(this).show();
	    	}).on("ajaxStop", function() {
	        $(this).hide();
	    	}).on("ajaxError", function() {
	        $(this).hide();
	 });	
	});

/* Registred team json and randomize function */
	/* drug and drop function */
	teamlist = {'teamName':[],'set':[] }; 
	counterx = 0;

	function drag(arg, ev) {
		ev.dataTransfer.setData("text", ev.target.id);
		teamlist.teamName[counterx] = $(arg).find('span.teamName').text();
		teamlist.set[counterx] = $(arg).find('span.setNuber').text();
	
	}

	function allowDrop(ev) {
		ev.preventDefault();
	}

	function drop(ev, set) {
		ev.preventDefault();
		var data = ev.dataTransfer.getData("text");
		ev.target.appendChild(document.getElementById(data));
		teamlist.set[counterx] = set;
		counterx += 1;
	}



	/* Publish official participant list */

	function publish(arg1,arg2) {
	    myJSON = JSON.stringify(teamlist);
	    //alert(myJSON);
		    $.ajax({
			  url:'/competition/registredteams/update',
			  type:"POST",
			  data:myJSON,
			  contentType:"application/json; charset=utf-8",
			  dataType:"json",
			  success: function(data){
			    location.reload(true);
			  },
			  error: function() {
		        alert("Error");
		      }
			})
	}

	function save_team_change() {
	    myJSON = JSON.stringify(teamlist);
	    //alert(myJSON);
		    $.ajax({
			  url:'/competition//registredteams/save_update',
			  type:"POST",
			  data:myJSON,
			  contentType:"application/json; charset=utf-8",
			  dataType:"json",
			  success: function(data){
			    location.reload(true);
			  },
			  error: function() {
		        alert("Error");
		      }
			})
	}

	function highlightFinals(arg) {
			myJSON1 = JSON.stringify({'highlight':arg});
			$.ajax({
			  url:'/competition/results/highlight',
			  type:"POST",
			  data:myJSON1,
			  contentType:"application/json; charset=utf-8",
			  dataType:"json",
			  success: function(data){
			    location.reload();
			  },
			  error: function() {
		        alert('Error');
		      }
			})
	}

	function display(msg){
	$('mytest').html(msg)
	}

	function unpublish(arg1,arg2) {
	    //arg1.className = arg1.className.replace(" w3-show", " w3-hide");
		//var x = document.getElementById(arg2);
	    //x.className = x.className.replace(" w3-hide", " w3-show");
	    $.post('/competition/registredteams/unpublish', {'status':'closed'},function(data, status){
	    	if(status == 'success'){location.reload(true);}
	    });
	    /* TODO дописать  функцию для снятия финального списка с публикации*/
	}	

	function randomizeItems(items)
		{
		   var cached = items.slice(0), temp, i = cached.length, rand;
		    while(--i)
		    {
		        rand = Math.floor(i * Math.random());
		        temp = cached[rand];
		        cached[rand] = cached[i];
		        cached[i] = temp;

		    }

		    return cached;
		}
		
	function randomizeList(){
		
		var numberOfSets = $('#numberOfSets').text(), i=1;
		while( i <= numberOfSets){
			var list = document.getElementById("setul"+i);
				$(list).children().eq(0).remove();
				var nodes = list.children, n = 0;
				nodes = Array.prototype.slice.call(nodes);
			    nodes = randomizeItems(nodes);
				   	while(n < nodes.length)
				    {
				       list.appendChild(nodes[n]);
				        ++n;
				    }
			  
		i++
		$('<li draggable="true" ondragstart="drag(event)" class="helpingLi"><div class="w3-border-bottom w3-border-blue w3-padding"><div id="header" class="w3-row w3-margin-bottom"><div class="w3-col s12" ><span class="w3-small w3-text-grey">Перетащите сюда команды, которые вы хотите добавить в этот сет</span></div></div></li>').prependTo(list);
		list.style.display="block";
		}


	}	

	

/* All teams page */
	
	/* Редактирование информации о пользователе */	
	function edit_user_info(arg){
		var y = arg.parentElement.getElementsByTagName('input');
		var z = arg.parentElement.getElementsByTagName('select');
		var x = arg.parentElement.getElementsByTagName('button');
		for (i = 0; i < y.length; i++) {
	        y[i].disabled = y[i].remove.disabled;
			} 
		for (i = 0; i < z.length; i++) {
	        z[i].disabled = z[i].remove.disabled;
			} 
		arg.className = arg.className.replace(" w3-show-inline-block", " w3-hide");
		x[1].className = x[1].className.replace(" w3-hide", " w3-show-inline-block");
		y[0].autofocus = y[0].focus();	
	}

	function save_user_info(arg){
		var y = arg.parentElement.getElementsByTagName('input');
		var z = arg.parentElement.getElementsByTagName('select');
		var x = arg.parentElement.getElementsByTagName('button');
		for (i = 0; i < y.length; i++) {
	        y[i].setAttribute("disabled","")
			} 
		for (i = 0; i < z.length; i++) {
	        z[i].setAttribute("disabled","")
			} 
		arg.className = arg.className.replace(" w3-show-inline-block", " w3-hide");
		x[0].className = x[0].className.replace(" w3-hide", " w3-show-inline-block");
		teamID = '#'+$(arg).parent().parent().attr('id');
		TeamCompetition = $(teamID+' span.teamName').text() + $(teamID+' p.competition').text();
		
		name1x = $(teamID+' input.name1').val();
		sname1x = $(teamID+' input.sname1').val();
		year1x = $(teamID+' input.year1').val();
		club1x = $(teamID+' input.club1').val();
		male1x = $(teamID+' select.male1').val();
		phone1x = $(teamID+' input.phone1').val();
		alpSkill1x = $(teamID+' select.alpSkill1').val(); 
		climbSkill1x = $(teamID+' select.climbSkill1').val();

		name2x = $(teamID+' input.name2').val();
		sname2x = $(teamID+' input.sname2').val();
		year2x = $(teamID+' input.year2').val();
		club2x = $(teamID+' input.club2').val();
		male2x = $(teamID+' select.male2').val();
		phone2x = $(teamID+' input.phone2').val();
		alpSkill2x = $(teamID+' select.alpSkill2').val(); 
		climbSkill2x = $(teamID+' select.climbSkill2').val();
		var team = {
			name1 : name1x,
			sname1 : sname1x,
			club1 : club1x,
			year1 : year1x,
			male1 : male1x,
			phone1 : phone1x,
			alpSkill1 : alpSkill1x,
			climbSkill1 : climbSkill1x,

			name2 : name2x,
			sname2 : sname2x,
			year2 : year2x,
			club2 : club2x,
			male2 : male2x,
			phone2 : phone2x,
			alpSkill2 : alpSkill2x,
			climbSkill2 :climbSkill2x,

			keyTeamCompetition : TeamCompetition
			};
		$.post('/competition/allteams/change', team, alert('Данные сохранены'));

	}	
/* Delete functions */	
	
	function assign_id(arg){
		arg.parentElement.setAttribute("id","delete");
	}

	function delete_element_modal(arg){
		document.getElementById(arg).style.display = "none";
		var teamID = $('li#delete span.teamName').text() + $('li#delete p.competition').text();
		$.get('/competition/allteams/delete/'+teamID);
		var y = document.getElementById('delete').parentElement;
		var x = document.getElementById('delete');
		y.removeChild(x);
		
	}

	function delete_archive_modal(arg){
		document.getElementById(arg).style.display = "none";
		var teamID = $('div#delete p.competitionName').text();
		$.post('/competition/admin/delete-archive', {competitionName : teamID});
		var y = document.getElementById('delete').parentElement;
		var x = document.getElementById('delete');
		y.removeChild(x);
		
	}
	function delete_team_modal(arg){
		document.getElementById(arg).style.display = "none";
		var teamID = $('li#delete span.teamName').text() + $('#competition').text();
		$.get('/competition/allteams/delete/'+teamID);
		var y = document.getElementById('delete').parentElement;
		var x = document.getElementById('delete');
		y.removeChild(x);
		
	}


	function delete_user_modal(arg){
		document.getElementById(arg).style.display = "none";
		var teamID = $('li#delete div.name').text() + $('li#delete div.sname').text()+$('li#delete div.year').text();
		//alert(teamID);
		$.post('/competition/allmembers/delete', {keyNameSnameYear : teamID});
		var y = document.getElementById('delete').parentElement;
		var x = document.getElementById('delete');
		y.removeChild(x);
		
	}

	function delete_volonteer_modal(arg){
		document.getElementById(arg).style.display = "none";
		//var teamID = $('li#delete div.name').text() + $('li#delete div.sname').text();
		//alert(teamID);
		$.post('/competition/volunteers/delete', {name : $('li#delete div.name').text(), sname : $('li#delete div.sname').text() } );
		var y = document.getElementById('delete').parentElement;
		var x = document.getElementById('delete');
		y.removeChild(x);
		
	}

	function delete_element(){
		var y = document.getElementById('delete').parentElement;
		var x = document.getElementById('delete');
		y.removeChild(x);
	}

	function delete_doc(){
		docName = $('#delete div.name').text()
		$.post('/site/docs/delete', {name : docName} );
		var y = document.getElementById('delete').parentElement;
		var x = document.getElementById('delete');
		y.removeChild(x);
	}

	function delete_rules(arg){
		//docName = $('#delete div.name').text()
		$.post('/info/rules/delete', {nameRus : arg} );
		var y = document.getElementById('delete').parentElement;
		var x = document.getElementById('delete');
		y.removeChild(x);
	}

	function delete_contact(arg){
		$.post('/contacts/delete', {fullName : arg} );
		var y = document.getElementById('delete').parentElement;
		var x = document.getElementById('delete');
		y.removeChild(x);
	}	

	function delete_article(arg){
		$.post('/media/press/delete', {url : arg} );
		var y = document.getElementById('delete').parentElement;
		var x = document.getElementById('delete');
		y.removeChild(x);
	}

	function delete_video(arg){
		$.post('/media/video/delete', {description : arg} );
		var y = document.getElementById('delete').parentElement;
		var x = document.getElementById('delete');
		y.removeChild(x);
	}	
	
	function delete_sponsor(arg){
		$.post('/info/sponsors/delete', {sponsorName : arg} );
		var y = document.getElementById('delete').parentElement;
		var x = document.getElementById('delete');
		y.removeChild(x);
	}

	function delete_gallery(arg){
		$.post('/media/photo/delete', {galleryID : arg} );
		var y = document.getElementById('delete').parentElement;
		var x = document.getElementById('delete');
		y.removeChild(x);
	}

	function delete_photo(arg0, arg){
		$.post('/media/photo/delete_photo', { photoID : arg} );
		//var y = document.getElementById('delete').parentElement;
		//var x = document.getElementById('delete');
		//y.removeChild(x);
		//window.removeEventListener('scroll',function(){})
		$(arg0).parent().remove()
		$('.photo' + arg).remove()
		//arg0.parentElement.style.visibility = "hidden"
		setTimeout( function(){ xxx._closeSlideshow(); xxx = new CBPGridGallery( document.getElementById( 'grid-gallery' ) ); }, 35)
		//xxx.isSlideshowVisible = false
		//setTimeout( function(){ xxx._openSlideshow(2); xxx._closeSlideshow(); }, 70)
		
	}	

	function delete_post_photo(arg0, arg){
		$.post('/news/edit/delete_post_photo', { photoID : arg} );
		$(arg0).parent().remove()
		$('.photo' + arg).remove()
		setTimeout( function(){ yyy._closeSlideshow(); yyy = new CBPGridGallery( document.getElementById( 'grid-gallery' ) ); }, 35)
		
	}	

	function hide_slideshow(){
		$('#grid-gallery').removeClass('.slideshow-open');	
		$('.slideshow li.show').removeClass('.show');	
		$('.slideshow li.current').removeClass('.current');
	}

	function delete_route(){
		routeNuber1 = $('#delete div.routeNuber').text()
		$.post('/competition/routes/delete', {routeNuber : routeNuber1});
		var y = document.getElementById('delete').parentElement;
		var x = document.getElementById('delete');
		y.removeChild(x);
	}
	
	function delete_logo(arg0, arg){
		$.post('/site/admin/delete_logo', { logoID : arg} );
		$(arg0).parent().remove()
	}

	function make_logo_active(arg){
		$.post('/site/admin/make_logo_active', { logoID : arg}, function(){
			    location.reload(true);} );
	}


	function check_icon(arg){
		$('#add_page .fa-check-circle').hide()
		$(arg).children("i.fa-check-circle").show()
	}

	function delete_page(arg0, arg1){
		$.post('/site/admin/delete_page', { pageID : arg1 } );
		$(arg0).parent().remove()
	}

	function get_route_info(routeNuber){
		//$('#add_route_result img').attr("src",)
		$.get('/competition/routes/info/'+routeNuber, 
			function(data, status){
        		//alert("Data: " + data + "\nStatus: " + status);
    			$('#routeName1').text('Трасса №'+data.routeNuber+' "'+data.name+'"');
    			$('#routeNuber1').val(data.routeNuber);
    			$('#routeNuber1').attr("type", "hidden");
    			$('#routeIMG').attr("src", data.picURL);

    			
    		});

		
	}


	function myselect(level){
					$("select").css("border","red solid 1px")

					}

/* Tab switch function*/
	function openTab(evt, tabName) {
	  var i, x, tablinks;

	  x = document.getElementsByClassName("teamlist");
	  
	  for (i = 0; i < x.length; i++) {
	     x[i].style.display = "none";
	  }

	  tablinks = document.getElementsByClassName("tablink");
	  
	  for (i = 0; i < x.length; i++) {
	     tablinks[i].className = tablinks[i].className.replace(" w3-border-blue", "");
	     tablinks[i].className = tablinks[i].className.replace(" w3-blue-l4", "");
	     tablinks[i].className = tablinks[i].className += " w3-text-grey";
	  }

	  document.getElementById(tabName).style.display = "block";
	  evt.currentTarget.firstElementChild.className += " w3-border-blue";
	  evt.currentTarget.firstElementChild.className += " w3-blue-l4";
	}

	//Toogle function

	function toogle(show, hide,tabName){
		//(то что показываем, то что скрываем, id вкалдки которую выделяем синим)
	var i, x, tablinks;

		$("input").each(function(){
			$(this).val('');
			ul = document.getElementsByClassName("ul-filter");
		    	for (n = 0; n < ul.length; n++) {		    	
				    li = ul[n].getElementsByTagName("li");
				    for (i = 0; i < li.length; i++) {
				            li[i].style.display = "block";
					}   
		    	}

		})
        $("#"+hide).hide("slow");
        $("#"+show).show("slow");
        $(".tablink").removeClass("w3-border-blue w3-blue-l4");
        $(".tablink").addClass(" w3-text-grey");
        $("#"+tabName).addClass("w3-border-blue w3-blue-l4");

	
    };

	/*filter fucntion*/
		function myFilter(x) {
		    var input, filter, ul, li, i, n;
		    input = document.getElementsByClassName("input-filter");
		    filter = input[x].value.toUpperCase();
		    ul = document.getElementsByClassName("ul-filter");
		    	for (n = 0; n < ul.length; n++) {		    	
				    
				    li = ul[n].getElementsByTagName("li");
				    
				    for (i = 0; i < li.length; i++) {
				        
				        if (li[i].innerHTML.toUpperCase().indexOf(filter) > -1) {
				            li[i].style.display = "";
				        } 
				        else {
				            li[i].style.display = "none";
				      	}
					}   
		    	}
		}


		function tableFilter(x,y) {
		    var input, filter, table, tr, i, n, y;
		    
		    input = document.getElementsByClassName("input-filter")
		    filter = input[x].value.toUpperCase();
		    table = document.getElementsByTagName("table");
			tr = table[y].getElementsByTagName("tr");
			    
			    for (i = 3; i < tr.length; i++) {
			        if (tr[i].innerHTML.toUpperCase().indexOf(filter) > -1) {
			            tr[i].style.display = "";
			        } 
			        else {
			            tr[i].style.display = "none";
			      	}
				}   
		}


/* accordion function */
	function blocks(id) {
	    var x = document.getElementById(id);

	    if (x.className.indexOf("w3-show") == -1) {
	        x.className += " w3-show";
	    } 
	    else { 
	        x.className = x.className.replace(" w3-show", "");
	    }
	}

	function comanddelete() {
		    this.parentElement.style.display = 'none';
	}

/* Save in Data base and Make Random list of Participant */

	function SaveAndRandom() {}



/* Change user in Team office */
	function change_user(arg0, secondname,name,birthyear,club,alp_level,climb_level,male,change_user_next,save_change_user){
		var arg0, x,y;
		/* 1. Прячем  копку Изменить выбранного пользоватея и показываем кнопку Сохранить*/
		arg0.className = arg0.className.replace(" w3-show", " w3-hide");
		x = document.getElementById(save_change_user);
		x.className = x.className.replace(" w3-hide", " w3-show");
		/* 2. Прячем кнопку Изменить у второго пользователя */
		y = document.getElementById(change_user_next);
		y.className = y.className.replace(" w3-show", " w3-hide");
		/* 3. Активируем поля ввода у выбранного пользователя */
		document.getElementById(secondname).disabled = document.getElementById(secondname).remove.disabled;
		document.getElementById(secondname).autofocus = document.getElementById(secondname).focus();
		document.getElementById(name).disabled = document.getElementById(name).remove.disabled;
		document.getElementById(birthyear).disabled = document.getElementById(birthyear).remove.disabled;
		document.getElementById(club).disabled = document.getElementById(club).remove.disabled;
		document.getElementById(alp_level).disabled = document.getElementById(alp_level).remove.disabled;
		document.getElementById(climb_level).disabled = document.getElementById(climb_level).remove.disabled;
		document.getElementById(male).disabled = document.getElementById(male).remove.disabled;
		
	}


	function save_change_user(arg,secondname,name,birthyear,club,alp_level,climb_level,male,myForm){
		/* 1 блокируем поля ввода */
		document.getElementById(secondname).disabled = document.getElementById(secondname).remove.disabled;
		document.getElementById(name).disabled = document.getElementById(name).remove.disabled;
		document.getElementById(birthyear).disabled = document.getElementById(birthyear).remove.disabled;
		document.getElementById(club).disabled = document.getElementById(club).remove.disabled;
		document.getElementById(alp_level).disabled = document.getElementById(alp_level).remove.disabled;
		document.getElementById(climb_level).disabled = document.getElementById(climb_level).remove.disabled;
		document.getElementById(male).disabled = document.getElementById(male).remove.disabled;
		document.getElementById(myForm).submit();
		/* 2 убираем кнопку Сохранить*/
		arg.className = arg.className.replace(" w3-show", " w3-hide");
		}
	
/* Competition administration page */
	
	/*Open/Close competition block*/

		function open_competition(arg1, arg2) {
			/* меняем нкопку открыть соревнования на кнопку закрыть соревнования */	
		    arg1.className = arg1.className.replace(" w3-show", " w3-hide");
			var x = document.getElementById(arg2);
		    x.className = x.className.replace(" w3-hide", " w3-show");
		    /* меняем статус кнопки "открыть регистрацию" на активный */
		    var y = document.getElementById('controls');
		    y.className = y.className.replace(" w3-disabled", "");
		    y.setAttribute("disabled","");
		    document.getElementById('controls_tooltip').className = document.getElementById('controls_tooltip').className.replace("my-tooltip-text-2", " w3-hide");
			}

		    /*TODO дописать функцию которая будет обнулять Обнуляет все БД типа current */
		

		function close_competition(arg1, arg2) {
		    arg1.className = arg1.className.replace(" w3-show", " w3-hide");
			var x = document.getElementById(arg2);
		    x.className = x.className.replace(" w3-hide", " w3-show");
		   	var y = document.getElementById('controls');
		    y.className += " w3-disabled";
		    y.setAttribute("disabled","disabled");
		    document.getElementById('controls_tooltip').className = document.getElementById('controls_tooltip').className.replace(" w3-hide", " my-tooltip-text-2");
		    
		    /*Обнуляем значения в модальном окне*/
		    var set_inputs = document.getElementsByTagName('input');
			for (n=1; n<set_inputs.length; n++) {
				set_inputs[n].className = set_inputs[n].className.replace(" w3-show", " w3-hide");
			}
			document.getElementById('set_description').className = document.getElementById('set_description').className.replace(" w3-show", " w3-hide");
		    var set_selection = document.getElementById('number_of_sets');
		    set_selection.value = '0';
		    /*TODO Дописать  функцию для снятия финального списка с публикации*/
		}	

		function set_description(){
			var x = document.getElementById('number_of_sets').value;
			var set_inputs = document.getElementsByClassName('input-filter')
			for (n=0; n<set_inputs.length; n++) {
				set_inputs[n].className = set_inputs[n].className.replace(" w3-show", " w3-hide");
			}
			for (i=0; i<=x; i++) {
				set_inputs[i].className = set_inputs[i].className.replace(" w3-hide", " w3-show");
			}
			set_inputs[0].autofocus = set_inputs[0].focus();
			document.getElementById('set_description').className = document.getElementById('set_description').className.replace(" w3-hide", " w3-show");
		}
	



/* Qualification and Final results Page */

	function edit_results(arg){
		$(arg).parent().parent().attr('id', 'change');
		var y = arg.parentElement.parentElement.getElementsByTagName('input');
		var z = arg.parentElement.parentElement.getElementsByTagName('select');
		var x = arg.parentElement.parentElement.getElementsByTagName('button');
		for (i = 0; i < y.length; i++) {
	        y[i].disabled = y[i].remove.disabled;
			} 
		for (i = 0; i < z.length; i++) {
	        z[i].disabled = z[i].remove.disabled;
			} 
		arg.className = arg.className.replace(" w3-show-inline-block", " w3-hide");
		x[1].className = x[1].className.replace(" w3-hide", " w3-show-inline-block");
		y[0].autofocus = y[0].focus();	
	}

	function save_results(arg){
		var y = arg.parentElement.parentElement.getElementsByTagName('input');
		var z = arg.parentElement.parentElement.getElementsByTagName('select');
		var x = arg.parentElement.parentElement.getElementsByTagName('button');
		for (i = 0; i < y.length; i++) {
	        y[i].setAttribute("disabled","")
			} 
		for (i = 0; i < z.length; i++) {
	        z[i].setAttribute("disabled","")
			} 
		arg.className = arg.className.replace(" w3-show-inline-block", " w3-hide");
		x[0].className = x[0].className.replace(" w3-hide", " w3-show-inline-block");
		
		teamID = '#'+$(arg).parent().parent().attr('id');
		routes = $(teamID+' td.routes');
		team = {
			'competition': $('#competition').text(),
			'teamName': $(teamID + ' span.teamName').text(),
			'routeScoreFinal': $(teamID + ' input.routeScoreFinal').val(),
			'teamStatus': $(teamID + ' select.teamStatus').val()
		};
		for (i=0; i<routes.length; i++){
			routeNuber = routes.eq(i).find('span.routeNuber').text();
			team['routeTimeSec'+routeNuber] = routes.eq(i).find('input.min').val()*60+routes.eq(i).find('input.sec').val()*1;
		}
		myJSON = JSON.stringify(team);
	    //alert(myJSON);
		    $.ajax({
			  url:'/competition/results/update',
			  type:"POST",
			  data:myJSON,
			  contentType:"application/json; charset=utf-8",
			  dataType:"json",
			  success: function(data){
			    alert('Изменения сохранены');
			    //location.reload(true);
			  },
			  error: function() {
			  	alert('Ошибка')
			  	//location.reload(true);
		      }
			})

		$(arg).parent().parent().removeAttr('id');

		/* TODO Дописать функцию отправки измененных данных на сервер */
	}

	
	function save_and_refresh(){
		/* TODO дописать функцию сохранения измененных результатов на сервере и обновления странички с Управление результатом */

	}

	function downloadxls(){
		/* TODO написать функцию для скачивания протоколов в формате xls*/
	}

	
	/* disabling the first elements in drow-down elements in Form */

