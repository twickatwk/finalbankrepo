
class Navigator extends React.Component {
    render() {
        return(
            <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
                <a id="nametxt" class="navbar-brand" href="/">The Bank We Need <span id="nametxt2">by DZAC</span></a>
                <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse" id="navbarNav">
                    <ul class="navbar-nav">
                        <li class="nav-item active">
                            <a id="linktxt" class="nav-link" href="/grants">My Vault <span class="sr-only">(current)</span></a>
                        </li>
                        <li class="nav-item">
                            <a id="linktxt" class="nav-link" href="/investors">RazFunds</a>
                        </li>
                        <li class="nav-item ">
                            <a id="linktxt" class="nav-link " href="/logout">Logout</a>
                        </li>
                    </ul>

                </div>

            </nav>
        )
    }
}

ReactDOM.render(
    <Navigator />,
    document.getElementById('navigator')
);

