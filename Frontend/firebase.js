  // Set the configuration for your app
  // TODO: Replace with your project's config object
  // Get a reference to the database service
  


function login(){

var userEmail = document.getElementById("username").value;
var userPass = document.getElementById("password").value;

firebase.auth().signInWithEmailAndPassword(userEmail, userPass)
.then(function(user){
	document.getElementById("success").innerHTML = "Login Successful";
	document.getElementById("Usr_name").innerHTML = "Hi "+userEmail.match(/^([^@]*)@/)[1];;
	document.getElementById("Usr_name").style.display="block";
	document.getElementById("nav_login").onclick = "logout()";
	document.getElementById("login_form").style.display="none";
	document.getElementById("logout_form").style.display="block";
	document.getElementById("signup-box-link").innerHTML = "Logout";
	document.getElementById("nav_login").innerHTML = "Logout";

	console.log("successful",user.uid);
})
.catch(function(error) {
	// Handle Errors here.
	var errorCode = error.code;
	var errorMessage = error.message;

	window.alert("Error : " + errorMessage);

	// ...
});

}
      
function logout(){
	firebase.auth().signOut().then(function(user){
		console.log("logged out");
		// document.getElementById("success").innerHTML = "........";
		// document.getElementById("Usr_name").style.display="none";
		// document.getElementById("login_form").style.display="block";
		// document.getElementById("logout_form").style.display="none";
		// document.getElementById("signup-box-link").innerHTML = "Logout";
		// document.getElementById("nav_login").innerHTML = "Logout";
		// document.getElementById("nav_login").onclick = "nav_login()";
	});
}


function signup()
{
	var userEmail = document.getElementById("sign_up_username").value;
	var userPass = document.getElementById("sign_up_password").value;
	var confirmPass = document.getElementById("confirm_password").value;

	if(userPass!=confirmPass){
		alert("makesure password is same")
	}
	else{
		firebase
		.auth()
		.createUserWithEmailAndPassword(userEmail, userPass)
		.then(function(userResponse){
			alert("dasjfhd");
		console.log("Successfully created user account with uid:", userResponse.uid);
		})
		.catch(function(error){
		console.log("Error creating user:", error);
		});
	}
	
}


function report()
{
	firebase.auth().onAuthStateChanged(function(user) {
	if (user) {
	// User is signed in.
		alert("dasf");
		console.login("user logged in")	;
	} else {
	// No user is signed in.
		console.login("not login");
	}
	});
	var plate_no = document.getElementById("plate_no").value;

	console.log(plate_no.slice(2,4));
	// const dbrefstate = database.ref().child('KA')

	var ref = firebase.database().ref(plate_no.slice(0,2)+"/"+plate_no.slice(2,4)+"/"+plate_no.slice(4,6)+"/"+plate_no.slice(6,10));

	// for updating the value
	ref.update({
		"stolen":"yes"
	});
	// for viewing
	ref.on("value", function(snapshot) {
	   console.log(snapshot.val());
	}, function (error) {
	   console.log("Error: " + error.code);
	});	
}
