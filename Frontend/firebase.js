function login(){

var userEmail = document.getElementById("username").value;
var userPass = document.getElementById("password").value;

firebase.auth().signInWithEmailAndPassword(userEmail, userPass)
.then(function(user){
	console.log("successful");
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
	firebase.auth().signOut();
}


function signup()
{
	var userEmail = document.getElementById("sign_up_username").value;
	var userPass = document.getElementById("sign_up_password").value;


	firebase
	.auth()
	.createUserWithEmailAndPassword(userEmail, userPass)
	.then( function(userResponse){
	  console.log("Successfully created user account with uid:", userResponse.uid);
	})
	.catch(function(error){
	  console.log("Error creating user:", error);
	});
}