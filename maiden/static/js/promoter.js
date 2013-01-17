
(function(){

	function microAjax(B,A){this.bindFunction=function(E,D){return function(){return E.apply(D,[D])}};this.stateChange=function(D){if(this.request.readyState==4){this.callbackFunction(this.request.responseText)}};this.getRequest=function(){if(window.ActiveXObject){return new ActiveXObject("Microsoft.XMLHTTP")}else{if(window.XMLHttpRequest){return new XMLHttpRequest()}}return false};this.postBody=(arguments[2]||"");this.callbackFunction=A;this.url=B;this.request=this.getRequest();if(this.request){var C=this.request;C.onreadystatechange=this.bindFunction(this.stateChange,this);if(this.postBody!==""){C.open("POST",B,true);C.setRequestHeader("X-Requested-With","XMLHttpRequest");C.setRequestHeader("Content-type","application/x-www-form-urlencoded");C.setRequestHeader("Connection","close")}else{C.open("GET",B,true)}C.send(this.postBody)}};

	var supports3DTransforms = 'WebkitPerspective' in document.body.style ||
								'MozPerspective' in document.body.style ||
								'msPerspective' in document.body.style ||
								'OPerspective' in document.body.style ||
								'perspective' in document.body.style;

	var mainContainer = document.querySelector( '.main-container' );

	var pageHeight = Math.max(
		Math.max( document.body.scrollHeight, document.documentElement.scrollHeight ),
		Math.max( document.body.offsetHeight, document.documentElement.offsetHeight ),
		Math.max( document.body.clientHeight, document.documentElement.clientHeight )
	);

	// Don't bother loading if 3D transforms aren't supported
	if( supports3DTransforms && mainContainer && pageHeight < window.innerHeight * 1.1 ) {

		microAjax( 'http://hakim.se/assets/promoter/promoter.css', function ( styleData ) {
			microAjax( 'http://hakim.se/assets/promoter/promoter.html', function ( contentsData ) {

				var style = document.createElement( 'style' );
				style.setAttribute( 'type', 'text/css' );
				style.innerHTML = styleData;
				document.getElementsByTagName( 'head' )[0].appendChild( style );

				var meny = document.createElement( 'div' );
				meny.setAttribute( 'class', 'meny' );
				meny.style.display = 'none';
				meny.innerHTML = contentsData;
				document.body.appendChild( meny );

				var arrow = document.createElement( 'div' );
				arrow.setAttribute( 'class', 'meny-arrow' );
				arrow.innerHTML = 'More Experiments <span>&#x25BC;</span>';
				document.body.appendChild( arrow );

				var cover = document.createElement( 'div' );
				cover.setAttribute( 'class', 'cover' );
				mainContainer.appendChild( cover );

				mainContainer.className += ' meny-contents';

				/*!
				 * meny 0.4
				 * http://lab.hakim.se/meny
				 * MIT licensed
				 *
				 * Created by Hakim El Hattab, http://hakim.se
				 */
				(function(){var meny=document.querySelector(".meny");if(!meny||!meny.parentNode)return;var menyWrapper=meny.parentNode;menyWrapper.className+=" meny-wrapper";var indentX=menyWrapper.offsetLeft,activateX=40,deactivateX=meny.offsetWidth||300,touchStartX=null,touchMoveX=null,isActive=false,isMouseDown=false;var supports3DTransforms="WebkitPerspective"in document.body.style||"MozPerspective"in document.body.style||"msPerspective"in document.body.style||"OPerspective"in document.body.style||"perspective"in
				document.body.style;document.addEventListener("mousedown",onMouseDown,false);document.addEventListener("mouseup",onMouseUp,false);document.addEventListener("mousemove",onMouseMove,false);document.addEventListener("touchstart",onTouchStart,false);document.addEventListener("touchend",onTouchEnd,false);if(!supports3DTransforms)document.documentElement.className+=" meny-no-transform";document.documentElement.className+=" meny-ready";function onMouseDown(event){isMouseDown=true}function onMouseMove(event){if(!isMouseDown){var x=
				event.clientX-indentX;if(x>deactivateX)deactivate();else if(x<activateX)activate()}}function onMouseUp(event){isMouseDown=false}function onTouchStart(event){touchStartX=event.touches[0].clientX-indentX;touchMoveX=null;if(isActive||touchStartX<activateX)document.addEventListener("touchmove",onTouchMove,false)}function onTouchMove(event){touchMoveX=event.touches[0].clientX-indentX;if(isActive&&touchMoveX<touchStartX-activateX){deactivate();event.preventDefault()}else if(touchStartX<activateX&&touchMoveX>
				touchStartX+activateX){activate();event.preventDefault()}}function onTouchEnd(event){document.addEventListener("touchmove",onTouchMove,false);if(touchMoveX===null)if(touchStartX>deactivateX)deactivate();else if(touchStartX<activateX*2)activate()}function activate(){if(isActive===false){isActive=true;document.documentElement.className=document.documentElement.className.replace(/\s+$/gi,"")+" meny-active"}}function deactivate(){if(isActive===true){isActive=false;document.documentElement.className=document.documentElement.className.replace("meny-active",
				"")}}})();

			});
		});

	}

})();

