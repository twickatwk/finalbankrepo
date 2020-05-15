
/* FACEBOOK CODE */

// Loads the fb js sdk part 1
(function(d, s, id) {                      // Load the SDK asynchronously
    var js, fjs = d.getElementsByTagName(s)[0];
    if (d.getElementById(id)) return;
    js = d.createElement(s); js.id = id;
    js.src = "https://connect.facebook.net/en_US/sdk.js";
    fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'facebook-jssdk'));

// Loads the fb js sdk part 2 - TODO: hide the api key in the backend
window.fbAsyncInit = function() {
    FB.init({
    appId      : '2930645783719886',
    cookie     : true,                     // Enable cookies to allow the server to access the session.
    xfbml      : true,                     // Parse social plugins on this webpage.
    version    : 'v7.0'           // Use this Graph API version for this call.
    });

    // Check the status of the login everytime when you load the sdk
    FB.getLoginStatus(function(response) {   // Called after the JS SDK has been initialized.
        statusChangeCallback(response);  // Returns the login status.
    });
};

// Callback method for inital login check
function statusChangeCallback(response) {
    // if the user is already logged in, then display the sign out btn
    if(response.status == 'connected') {
        document.getElementById('logoutbtn').style.display = "block";
    }else{
        // unhide the login btn if the user not logined yet
        document.getElementById('loginbtn').style.display = "block"
    }
    // update the status of the user
    console.log(response.status);
}

// Method to execute the login dialog
function fblogin() {
    // this is the sample code from fb to launch login dialog
    FB.login(function(response) {
            if (response.authResponse) {
                console.log('Welcome!  Fetching your information.... ');
                FB.api('/me', function(response) {
                console.log('Good to see you, ' + response.name + '.');

                // once the user is logged in, unhide the log out btn
                document.getElementById('logoutbtn').style.display = "block";
                // // update profile name to the text, once user is connected
                document.getElementById('status').innerHTML = 'Good to see you, ' + response.name + '! User id: ' + response.id;
                // hide the sign in btn once the user is connected
                document.getElementById('loginbtn').style.display = "none";
                
            });
            } else {
                console.log('User cancelled login or did not fully authorize.');
            }
    });
}


// Method to sign out of facebook
// Method that executes the fb log out
function fbLogout() {
    FB.logout(function(response) {
        // once the user is logged out, unhide the sign in btn
        document.getElementById('loginbtn').style.display = "block";
        // once the user is logged out, hide the sign out btn
        document.getElementById('logoutbtn').style.display = "none";
        
        // update status once user has logged out
        document.getElementById('status').innerHTML = "User has logged out"
    });
}

// This is the main component for the page
class Page extends React.Component {
    render() {
        return (
            <div id="loginbox">
                <LoginBox />
                <Content />
            </div>
        )
    }
}

class LoginBox extends React.Component {
    render() {
        return(
            <div class="row">
                <div class="col">
                    <div class="card" >
                        <img src="static/assets/bankimg.jpg" class="card-img-top" />
                        <div class="card-body">
                            <h5 class="card-title">The Bank You Need</h5>
                            <p class="card-text">Find Grants, Get Loans, And Crowdsource Funds</p>
                            <div onClick={fblogin} id="loginbtn" class="btn btn-primary">Login With Facebook</div>
                            <div onClick={fbLogout} id="logoutbtn" class="btn btn-primary">Log out</div>
                        </div>
                    </div>
                </div>
            </div>
        )
    }
}

class Content extends React.Component {
    render() {
        return(
            <div id="status"></div>
        )
    }
}

ReactDOM.render(
    <Page />,
    document.getElementById('root')
);